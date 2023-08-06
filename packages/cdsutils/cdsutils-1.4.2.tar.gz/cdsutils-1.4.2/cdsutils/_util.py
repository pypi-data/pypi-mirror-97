

def split_channel(channel):
    """Split channel into <IFO>:<SYS> and everything else."""
    if channel[0] == ':':
        channel = channel[1:]
    return channel.split('-', 1)


def split_channel_ifo(channel):
    """Split channel into <IFO>: and everything else."""
    if channel[0] == ':':
        return None, channel[1:]
    elif ':' in channel:
        return channel.split(':', 1)
    else:
        return None, channel
