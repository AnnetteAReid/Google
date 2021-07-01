"""A video player class."""
import random
from .video_library import VideoLibrary
from  src.video_playlist import Playlist


class VideoPlayer:
    """A class used to represent a Video Player."""


    def __init__(self):
        self._video_library = VideoLibrary()
        self.playing_video = None
        self.video_paused = False
        self.playlists = []
        self.playlist_names = []

    def sorted_videos(self):
        videos = self._video_library.get_all_videos()
        ordered = sorted(videos, key=lambda x: x.title, reverse=False)
        return ordered


    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        videos = self.sorted_videos()

        for video in videos:
            if video.flagged:
                if len(video.tags) == 0:
                    print(f"{video.title} ({video.video_id}) [] - FLAGGED (reason: {video.flagged_reason})")
                else:
                    print(
                        f"{video.title} ({video.video_id}) [{video.tags[0]} {video.tags[1]}] - FLAGGED (reason: {video.flagged_reason})")
            else:
                if len(video.tags) == 0:
                    print(f"{video.title} ({video.video_id}) []")
                else:
                    print(f"{video.title} ({video.video_id}) [{video.tags[0]} {video.tags[1]}]")



    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot play video: Video does not exist")
        else:
            if video.flagged == True:
                print(f"Cannot play video: Video is currently flagged (reason: {video.flagged_reason})")
            else:
                if self.playing_video != None:
                    print(f"Stopping video: {self.playing_video.title}")
                print(f"Playing video: {video.title}")
                self.playing_video = video
                self.video_paused = False


    def stop_video(self):
        """Stops the current video."""
        if self.playing_video == None:
            print("Cannot stop video: No video is currently playing")
        else:
            print(f"Stopping video: {self.playing_video.title}")
            self.playing_video = None

    def play_random_video(self):
        """Plays a random video from the video library."""
        unflagged = []
        for video in self.sorted_videos():
            if video.flagged == False:
                unflagged.append(video)
        if len(unflagged) == 0:
            print("No videos available")
        else:
            random_video = random.choice(unflagged)

            if self.playing_video != None:
                self.stop_video()
            print(f"Playing video: {random_video.title}")
            self.playing_video = random_video
            self.video_paused = False

    def pause_video(self):
        """Pauses the current video."""
        if self.playing_video == None:
            print("Cannot pause video: No video is currently playing")
        elif self.video_paused == True:
            print(f"Video already paused: {self.playing_video.title}")
        else:
            print(f"Pausing video: {self.playing_video.title}")
            self.video_paused = True

    def continue_video(self):
        """Resumes playing the current video."""
        if self.playing_video == None:
            print("Cannot continue video: No video is currently playing")
        elif self.video_paused == True:
            print(f"Continuing video: {self.playing_video.title}")
            self.video_paused = False
        else:
            print("Cannot continue video: Video is not paused")



    def show_playing(self):
        """Displays video currently playing."""
        if self.playing_video == None:
            print("No video is currently playing")
        else:
            if self.video_paused == True:
                print(f"Currently playing: {self.playing_video.title} ({self.playing_video.video_id}) [{self.playing_video.tags[0]} {self.playing_video.tags[1]}] - PAUSED")
            else:
                print(f"Currently playing: {self.playing_video.title} ({self.playing_video.video_id}) [{self.playing_video.tags[0]} {self.playing_video.tags[1]}]")


    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if playlist_name.lower() in self.playlist_names:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self.playlists.append(Playlist(playlist_name.lower()))
            self.playlist_names.append(playlist_name)
            print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """


        if playlist_name.lower() not in [name.lower() for name in self.playlist_names]:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
        elif self._video_library.get_video(video_id) == None:
            print(f"Cannot add video to {playlist_name.lower()}: Video does not exist")
        else:
            video = self._video_library.get_video(video_id)
            index = [name.lower() for name in self.playlist_names].index(playlist_name.lower())

            if video in self.playlists[index].videos:
                print(f"Cannot add video to {playlist_name.lower()}: Video already added")
            elif video.flagged:
                print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {video.flagged_reason})")

            else:
                self.playlists[index].add_video(video)

                print(f"Added video to {playlist_name}: {self._video_library.get_video(video_id).title}")

    def show_all_playlists(self):
        """Display all playlists."""
        if len(self.playlists) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            sortedlist = self.playlist_names
            sortedlist.sort()
            for name in sortedlist:
                print(name)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """


        if playlist_name.lower() in [name.lower() for name in self.playlist_names]:
            print(f"Showing playlist: {playlist_name}")
            index = [name.lower() for name in self.playlist_names].index(playlist_name.lower())
            playlist = self.playlists[index]
            if len(playlist.videos) == 0:
                print("No videos here yet")
            else:
                for video in playlist.videos:
                    if video.flagged:
                        if len(video.tags) == 0:
                            print(f"{video.title} ({video.video_id}) [] - FLAGGED (reason: {video.flagged_reason})")
                        else:
                            print(f"{video.title} ({video.video_id}) [{video.tags[0]} {video.tags[1]}] - FLAGGED (reason: {video.flagged_reason})")
                    else:

                        if len(video.tags) == 0:
                            print(f"{video.title} ({video.video_id}) []")
                        else:
                            print(f"{video.title} ({video.video_id}) [{video.tags[0]} {video.tags[1]}]")
        else:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        video = self._video_library.get_video(video_id)
        if video == None:
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
        elif playlist_name.lower() in [name.lower() for name in self.playlist_names]:
            index = [name.lower() for name in self.playlist_names].index(playlist_name.lower())
            playlist = self.playlists[index]
            if video in playlist.videos:
                playlist.remove_video(video)
                print(f"Removed video from {playlist_name}: {video.title}")
            else:
                print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
        else:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() in [name.lower() for name in self.playlist_names]:
            index = self.playlist_names.index(playlist_name.lower())
            playlist = self.playlists[index]
            playlist.clear_playlist()
            print(f"Successfully removed all videos from {playlist_name}")
        else:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")


    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name in self.playlist_names:
            index = self.playlist_names.index(playlist_name)
            self.playlists.remove(self.playlists[index])
            self.playlist_names.remove(playlist_name)
            print(f"Deleted playlist: {playlist_name}")
        else:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """

        videos = self._video_library.get_all_videos()
        included_videos = []
        for video in videos:
            if search_term in video.title or search_term in video.video_id and video.flagged == False:
                included_videos.append(video)
        if len(included_videos) == 0:
            print(f"No search results for {search_term}")
        else:
            print(f"Here are the results for {search_term}:")
            for count,vid in enumerate(included_videos):
                if len(vid.tags) == 0:
                    print(f"{count+1}) {vid.title} ({vid.video_id}) []")
                else:
                    print(f"{count+1}) {vid.title} ({vid.video_id}) [{vid.tags[0]} {vid.tags[1]}]")
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            choice = input()
            try:
                choice = int(choice)

                if choice >= 0 and choice <= len(included_videos):
                    print(f"Playing video: {included_videos[choice-1].title}")
            except ValueError:
                pass




    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """

        videos = self._video_library.get_all_videos()
        included_videos = []
        for video in videos:
            if video_tag in video.tags and video.flagged == False:
                included_videos.append(video)
        if len(included_videos) == 0:
            print(f"No search results for {video_tag}")
        else:
            print(f"Here are the results for {video_tag}:")
            for count, vid in enumerate(included_videos):
                if len(vid.tags) == 0:
                    print(f"{count + 1}) {vid.title} ({vid.video_id}) []")
                else:
                    print(f"{count + 1}) {vid.title} ({vid.video_id}) [{vid.tags[0]} {vid.tags[1]}]")
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            choice = input()
            try:
                choice = int(choice)

                if choice >= 0 and choice <= len(included_videos):
                    print(f"Playing video: {included_videos[choice - 1].title}")
            except ValueError:
                pass

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot flag video: Video does not exist")
        elif video.flagged:
            print("Cannot flag video: Video is already flagged")
        else:
            if self.playing_video == video:
                self.stop_video()
            if flag_reason =="":
                video.flag("Not supplied")
                print(f"Successfully flagged video: {video.title} (reason: Not supplied)")
            else:
                video.flag(flag_reason)
                print(f"Successfully flagged video: {video.title} (reason: {flag_reason})")



    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot remove flag from video: Video does not exist")
        elif video.flagged:
            video.unflag()
            print(f"Successfully removed flag from video: {video.title}")
        else:
            print(f"Cannot remove flag from video: Video is not flagged")

