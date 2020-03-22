import asyncio
import random
import socket
import string
import time
from collections import OrderedDict
from contextlib import closing


async def wait_host_port(host, port, duration=10, delay=2):
    """Repeatedly try if a port on a host is open until duration seconds passed

    from: https://gist.github.com/betrcode/0248f0fda894013382d7#gistcomment-3161499

    :param str host: host ip address or hostname
    :param int port: port number
    :param int/float duration: Optional. Total duration in seconds to wait, by default 10
    :param int/float delay: Optional. Delay in seconds between each try, by default 2
    :return: awaitable bool
    """
    tmax = time.time() + duration
    while time.time() < tmax:
        try:
            _reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=5)
            writer.close()
            await writer.wait_closed()
            return True
        except:
            if delay:
                await asyncio.sleep(delay)
    return False


def get_free_port():
    """
    pick a free port number
    :return int: port number
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def random_str(len=16):
    """生成小写字母和数组组成的随机字符串

    :param int len: 字符串长度
    """
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(len))


def run_as_function(gen):
    res = None
    while 1:
        try:
            res = gen.send(res)
        except StopIteration as e:
            if len(e.args) == 1:
                return e.args[0]
            return


async def to_coroutine(gen):
    res = None
    while 1:
        try:
            c = gen.send(res)
            res = await c
        except StopIteration as e:
            if len(e.args) == 1:
                return e.args[0]
            return


class LRUDict(OrderedDict):
    """
    Store items in the order the keys were last recent updated.

    The last recent updated item was in end.
    The last furthest updated item was in front.
    """

    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        self.move_to_end(key)