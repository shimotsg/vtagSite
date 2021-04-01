# 2/27/2020
# geoffrey shimotsu
# an object to use musicbrainz lib
import musicbrainzngs


class mbQuery:
    def __init__(self, users_artist):
        # vars to use library functionality
        self.artist = users_artist
        self.album = ''
        self.artist_mbid = ''
        self.selected_album_mbid = ''
        self.release_mbid = ''
        self.selected_album_mbid_trklisting = ''
        self.MB_queryResult = {}
        self.MB_track_listing = {}
        self.limit = 500
        # authentication for mb web service
        self.agentAuth = musicbrainzngs.set_useragent(
            "audacityVinylTag",
            "0.1",
            "shimotsg@protonmail.com",
        )

    # this returns the top 25 album results as list of dicts from MB search using input string
    def with_input_browse_recordings(self):

        tmp = musicbrainzngs.search_artists(self.artist)
        self.artist_mbid = tmp['artist-list'][0]['id']
        self.MB_queryResult = musicbrainzngs.browse_releases(artist=self.artist_mbid, release_type="album", limit=self.limit)

    # this returns tracks from the album as list of dicts
    def show_tracks(self):
        for items in self.MB_queryResult['release-list']:
            if items.get('title') == self.album:
                self.release_mbid = items.get('id')
        self.MB_track_listing = musicbrainzngs.browse_recordings(release=self.release_mbid, limit=self.limit)

    # this writes out to the text file formatted for audacity label track
    def write_label_track(self):
        label_ver = 0
        label_text = f"label_text{label_ver}.txt"
        track_length_list = []
        track_title_list = []
        for track in self.MB_track_listing['recording-list']:
            track_length_list.append(track['length'])
            track_title_list.append(track['title'])
        # vars for track length running total
        # track length is in milliseconds
        track_tmp = 0.0
        # open file for writing
        f = open(label_text, "w")
        # iterate through both lists
        for i, j in zip(track_length_list, track_title_list):
            track_len = float(i)
            track_reg_start = track_tmp
            track_reg_end = track_reg_start + track_len
            track_tmp = track_reg_end
            # converting to seconds here
            tmp_line = f'{track_reg_start / 1000}\t{track_reg_end / 1000}\t{j}\n'
            # write line to file
            f.write(tmp_line)

        # close the txt file
        f.close()