from soco import SoCo
import dateutil.parser
import time
import sys

class SonosExtras(SoCo):
    def isPlaying(self) -> bool:
        return self.get_current_transport_info()["current_transport_state"] == "PLAYING"

    def stop_after(self, songs):
        if self.isPlaying():
            while songs >= 1:
                if songs > 1:
                    print("\rStopping afer " + songs.__str__() + " songs...", end = '         \r\n', flush=True)
                else:
                    print("\rStopping afer current song ...", end = '         \r\n', flush=True)
                time.sleep(3)
                if self.WaitPollCurrentTrackTillEnd(early=1) == False:
                    return 1
                songs -= 1
            print()
            self.pause()
        else:
            print("Nothing is playing!!")

    def WaitPollCurrentTrackTillEnd(self, quiet = False, early=0):
        remainingSeconds = self._curr_track_remaining_secs() - early
        recheck_counter = 0
        while remainingSeconds > 0:
            try:
                if not quiet:
                    print("\rWainting for the song to end in " + remainingSeconds.__str__(), end = '    ', flush=True)
                remainingSeconds -= 1
                time.sleep(1)
                recheck_counter += 1
                # resync the remaining time every 10 seconds
                if recheck_counter == 10:
                    recheck_counter = 0
                    if self.isPlaying() == False:
                        print("\nPlayback has stopped before reaching the end-target!")
                        return False
                    remainingSeconds = self._curr_track_remaining_secs() - early
            except KeyboardInterrupt:
                if not quiet:
                    print("\nCancelled by user!")
                return False
        return True

    def _curr_track_remaining_secs(self):
        current_track = self.get_current_track_info()
        position = dateutil.parser.parse(current_track['position'])
        duration = dateutil.parser.parse(current_track['duration'])
        remainingSeconds = (duration - position).seconds
        return remainingSeconds

class SonosExtrasCliHelper(SonosExtras):
    volume_increase_confirmation_threshold = 20

    def safe_set_volume(self, requested_volume, forced=False):
        current_volume = self.volume
        user_response = "No"
        if requested_volume - current_volume > self.volume_increase_confirmation_threshold and not forced:
            print("Are you sure you want to set volume from {current_volume} to {requested_volume}?")
            user_response = input()
            user_response = user_response.upper()
        if forced == True or user_response == "Y" or user_response == "YES" or not requested_volume - current_volume > self.volume_increase_confirmation_threshold:
            self.volume = requested_volume

    def print_queue(self, starting_index = 1, number_of_tracks = 0):
        result = []
        count = starting_index
        array_starting_index = starting_index - 1

        batches = max(100, number_of_tracks)
        queue = self.get_queue(array_starting_index, batches)

        if number_of_tracks == 0:
            return_rest = True
            tracks_to_return = queue.total_matches - ( starting_index - 1 )
        else:
            return_rest = False
            tracks_to_return = number_of_tracks

        line = "Total " + queue.total_matches.__str__() + " items in queue:"
        result.append(line)
        print(line)
        returned_matches = 0

        while (tracks_to_return > returned_matches and queue.number_returned > 0) :
            for item in queue:
                try:
                    item_dict = item.__dict__
                    item_dict["uri"] = item_dict["resources"][0].__str__()
                    if "creator" in item_dict.keys():
                        item_dict["artist"] = item_dict["creator"]
                    else:
                        item_dict["artist"] = "N/A"
                    if 'album' in item_dict.keys():
                        item_dict["album"] = item_dict["album"]
                    else:
                        item_dict["album"] = "N/A"
                    if "metadata" in item_dict.keys():
                        if "title" in item_dict['metadata'].keys():
                            item_dict["title"] = item_dict['metadata']["title"]
                    item_dict["mycount"] = count
                    # print(item_dict)
                    line = self.track_info_string(item_dict)
                    result.append(line)
                    print(line)
                    count += 1
                    returned_matches += 1
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                if tracks_to_return == returned_matches:
                    break
            queue = self.get_queue(returned_matches + array_starting_index)
        return result

    def get_current_status(self):
        transport_info = self.get_current_transport_info().__str__() + "\n"
        current_track = self.get_current_track_info()
        timestamp = current_track['position'] + '  /  ' + current_track['duration'] + "\n"
        return(transport_info + timestamp + self.track_info_string(current_track))

    def track_info_string(self, track):
        line = ''
        if "playlist_position" in track.keys():
            line = track["playlist_position"] + " | "
        else:
            line = track["mycount"].__str__() + " | "
        if track["artist"]  != '': line = line + track["artist"] + " | "
        if track["album"]   != '': line = line + track["album"] + " | "
        if track["title"]   != '': line = line + track["title"] + " | "
        if track["uri"]   != '': line = line + track["uri"]
        return(line)

    def playlists(self):
        allLists = self.get_sonos_playlists()
        result = []
        for ourList in allLists:
            result.append(ourList.item_id + " | " + ourList.title)
        result.append("Total: " + allLists.number_returned.__str__())
        return "\n".join(result)

    def playlist(self, title):
        try:
            ourList = self.get_sonos_playlist_by_attr('title', title)
        except ValueError:
            try:
                ourList = self.get_sonos_playlist_by_attr('item_id', title)
            except ValueError:
                print("No playlist matched " + title)
                return

        print("playlist " + title + " exists")
