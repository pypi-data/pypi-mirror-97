import pychromecast
import requests


class Chromecast:
    def __init__(self, cast):
        self.cast = cast
        self.mc = cast.media_controller
        self.friendly_name = cast.device.friendly_name
        print("instance", self.cast)

    def quit_app(self):
        self.cast.quit_app()

    def status(self):
        _status = self.cast.status
        _mc = self.cast.media_controller

        return {
            'is_active_input': _status.is_active_input,
            'volume_level': _status.volume_level,
            'volume_muted': _status.volume_muted,
            'title': _mc.title,
            'duration': _mc.duration,
        }

    def increase_volume(self):
        return self.cast.volume_up()

    def decrease_volume(self):
        return self.cast.volume_down()

    def mute(self):
        self.cast.set_volume_muted(True)

    def unmute(self):
        self.cast.set_volume_muted(False)

    def play(self, url, content_type=None):
        if not content_type:
            content_type = requests.head(url).headers['content-type']
        self.mc.play_media(url, content_type)

    def partial_seek(self, delta):
        self.seek(self.mc.status.adjusted_current_time + delta)

    def seek(self, pos):
        self.mc.seek(pos)

    def stop(self):
        self.mc.stop()

    def pause(self):
        if self.mc.is_paused:
            self.mc.play()
        else:
            self.mc.pause()


def get_chromecasts():
    return {
        str(cast.uuid): Chromecast(cast)
        for cast in pychromecast.get_chromecasts()}
