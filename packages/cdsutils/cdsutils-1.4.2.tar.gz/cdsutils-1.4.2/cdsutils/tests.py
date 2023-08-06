import unittest
import os
import time
import multiprocessing
from collections import defaultdict

from ezca import Ezca
from ezca.emulators import const as emu_const
from ezca.emulators.ligofilter import start_emulator

from .step import Step, step
from .servo import Servo, servo

##################################################

os.environ['EPICS_CAS_INTF_ADDR_LIST'] = "localhost"
os.environ['EPICS_CAS_SERVER_PORT'] = "58800"
os.environ['EPICS_CA_ADDR_LIST'] = "localhost:58800"

##################################################

emulator_proc = None

def setUpModule():
    global emulator_proc
    emulator_proc = multiprocessing.Process(target=start_emulator)
    emulator_proc.start()

def tearDownModule():
    global emulator_proc
    emulator_proc.terminate()
    emulator_proc.join()


class TestStep(unittest.TestCase):
    def setUp(self):
        self.ezca = Ezca(ifo=emu_const.TEST_IFO_NAME,
                         prefix=emu_const.TEST_SUBSYS_NAME+'-'+emu_const.TEST_FILTER_NAME)

    def test_linear_up(self):
        self.ezca['GAIN'] = 0
        step(self.ezca, 'GAIN', '+1,10')
        self.assertEqual(self.ezca.read('GAIN', use_monitor=False),
                         10)

    def test_linear_up1(self):
        self.ezca['GAIN'] = 0
        step(self.ezca, 'GAIN', '1,10')
        self.assertEqual(self.ezca.read('GAIN', use_monitor=False),
                         10)

    def test_linear_down(self):
        self.ezca['GAIN'] = 0
        step(self.ezca, 'GAIN', '-1,10')
        self.assertEqual(self.ezca.read('GAIN', use_monitor=False),
                         -10)

    def test_geometric_up(self):
        self.ezca['GAIN'] = 1
        step(self.ezca, 'GAIN', '*4,3')
        self.assertEqual(self.ezca.read('GAIN', use_monitor=False),
                         64)

    def test_geometric_down(self):
        self.ezca['GAIN'] = 64
        step(self.ezca, 'GAIN', '/2,4')
        self.assertEqual(self.ezca.read('GAIN', use_monitor=False),
                         4)

    def test_db_up(self):
        self.ezca['GAIN'] = 2
        step(self.ezca, 'GAIN', '+20db,3')
        self.assertEqual(self.ezca.read('GAIN', use_monitor=False),
                         2000)

    def test_db_up1(self):
        self.ezca['GAIN'] = 2
        step(self.ezca, 'GAIN', '20db,3')
        self.assertEqual(self.ezca.read('GAIN', use_monitor=False),
                         2000)

    def test_db_down(self):
        self.ezca['GAIN'] = 1000
        step(self.ezca, 'GAIN', '-20db,4')
        self.assertEqual(self.ezca.read('GAIN', use_monitor=False),
                         0.1)

    def test_multistep(self):
        self.ezca['GAIN'] = 1000
        step(self.ezca, 'GAIN', '-20db,4')
        self.assertEqual(self.ezca.read('GAIN', use_monitor=False),
                         0.1)

    def test_multichannel(self):
        self.ezca['GAIN'] = 0
        self.ezca['OFFSET'] = 0
        step(self.ezca, 'GAIN', '-1,10', 'OFFSET', '+2,3')
        self.assertEqual(self.ezca.read('GAIN', use_monitor=False),
                         -10)
        self.assertEqual(self.ezca.read('OFFSET', use_monitor=False),
                         6)

    def test_time_step(self):
        self.ezca['GAIN'] = 0
        time_step = 0.01
        nsteps = 100
        dt = time_step * nsteps
        t0 = time.time()
        step(self.ezca, 'GAIN', '1,%d' % nsteps, time_step=time_step)
        t1 = time.time()
        t1e = t0 + dt
        ep = 0.1
        print('t1-t0={}s, {}s expected ({}s margin)'.format(
            t1-t0, time_step*nsteps, ep))
        self.assertTrue(t1e - ep <= t1 <= t1e + ep)

    def test_time_step1(self):
        self.ezca['GAIN'] = 0
        time_step = 0.1
        nsteps = 10
        dt = time_step * nsteps
        t0 = time.time()
        step(self.ezca, 'GAIN', '1,%d' % nsteps, time_step=time_step)
        t1 = time.time()
        t1e = t0 + dt
        ep = 0.1
        print('t1-t0={}s, {}s expected ({}s margin)'.format(
            t1-t0, time_step*nsteps, ep))
        self.assertTrue(t1e - ep <= t1 <= t1e + ep)


class TestServo(unittest.TestCase):
    def setUp(self):
        self.ezca = Ezca(ifo=emu_const.TEST_IFO_NAME,
                         prefix=emu_const.TEST_SUBSYS_NAME)

    def test_single(self):
        self.ezca['FILTER_OFFSET'] = 0
        servo(self.ezca, 'FILTER_OFFSET', setpoint=10, timeout=10)
        self.assertTrue(abs(self.ezca['FILTER_OFFSET'] - 10) < 0.01)

    def test_readback(self):
        self.ezca['FILTER_INMON'] = 0
        self.ezca['FILTER_EXCMON'] = 0
        self.ezca['FILTER_GAIN'] = 1
        servo(self.ezca,
              control='FILTER_EXCMON',
              readback='FILTER_OUTMON', setpoint=10, timeout=10)
        self.assertTrue(abs(self.ezca['FILTER_OUTMON'] - 10) < 0.01)

    def test_common(self):
        self.ezca['FILTER_INMON'] = 0
        self.ezca['FILTER_EXCMON'] = 0
        self.ezca['FILTER_GAIN'] = 1
        self.ezca.get_LIGOFilter('FILTER').turn_on('INPUT')
        servo(self.ezca,
              control='FILTER_INMON',
              control2='FILTER_EXCMON',
              gain2=1,
              readback='FILTER_OUTMON', setpoint=10, timeout=10)
        self.assertTrue(abs(self.ezca['FILTER_OUTMON'] - 10) < 0.01)
        self.assertTrue(abs(self.ezca['FILTER_INMON'] - 5) < 0.01)
        self.assertTrue(abs(self.ezca['FILTER_EXCMON'] - 5) < 0.01)

    def test_differential(self):
        self.ezca['FILTER_INMON'] = 0
        self.ezca['FILTER_EXCMON'] = 0
        self.ezca['FILTER_GAIN'] = 1
        self.ezca.get_LIGOFilter('FILTER').turn_on('INPUT')
        servo(self.ezca,
              control='FILTER_INMON',
              control2='FILTER_EXCMON',
              gain2=1,
              readback='FILTER_OUTMON', setpoint=10, timeout=10)
        self.assertTrue(abs(self.ezca['FILTER_OUTMON'] - 10) < 0.01)
        self.assertTrue(abs(self.ezca['FILTER_INMON'] - 5) < 0.01)
        self.assertTrue(abs(self.ezca['FILTER_EXCMON'] - 5) < 0.01)

##################################################

if __name__ == '__main__':
    unittest.main(verbosity=5, failfast=False, buffer=True)
