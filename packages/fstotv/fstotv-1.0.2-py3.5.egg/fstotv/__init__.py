import sys
import time
import socket
import tty
import termios
from threading import Thread

from bottle import get, static_file, run
from .devices import get_devices


def get_ch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


@get('/movie')
def movie():
    return static_file(sys.argv[1], './')


def run_server():
    run(host="0.0.0.0", port=2015)


def start():
    ip = socket.gethostbyname(socket.gethostname())
    t = Thread(target=run_server)
    t.daemon = True
    t.start()
    print("waiting for discover chromecast")
    devices = get_devices()
    # take first device
    device = devices[next(devices.__iter__())]
    print("discovered", device.friendly_name)
    if not device.cast.is_idle:
        device.quit_app()
        print("kicked")
        time.sleep(5)
    device.play("http://%s:2015/movie" % ip)
    device.mc.block_until_active()

    while True:
        letter = get_ch()

        if letter in [' ', 'p']:
            device.pause()
            print("pause")

        elif letter in ['d']:
            print("%.2f / %.2f" % (
                device.cast.media_controller.status.adjusted_current_time,
                device.cast.media_controller.status.duration))

        elif letter in ['+', '=']:
            print("increase volume")
            device.increase_volume()

        elif letter in ['-']:
            print("decrease volume")
            device.decrease_volume()

        elif letter in ['n']:
            print("seek -30")
            device.partial_seek(-30)

        elif letter in ['m']:
            print("seek 30")
            device.partial_seek(30)

        elif letter in ['j']:
            print("seek -600")
            device.partial_seek(-600)

        elif letter in ['k']:
            print("seek 600")
            device.partial_seek(600)

        elif letter in ['x']:
            device.quit_app()
            print("close")
            exit()
        else:
            print("press x to exit")


if __name__ == "__main__":
    start()
