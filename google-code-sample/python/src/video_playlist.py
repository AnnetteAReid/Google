"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, name):
        self._name = name
        self._videos = []

    @property
    def name(self) -> str:
        """Returns the title of a video."""
        return self._name

    @property
    def videos(self) -> str:
        """Returns the title of a video."""
        return self._videos

    def add_video(self, video):
        self.videos.append(video)

    def remove_video(self,video):
        self.videos.remove(video)

    def clear_playlist(self):
        self.videos.clear()