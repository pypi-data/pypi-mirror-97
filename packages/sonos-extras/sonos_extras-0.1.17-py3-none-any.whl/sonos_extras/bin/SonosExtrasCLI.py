#!/usr/bin/python

import sys

def main(raw_args=None):
    from .. import SonosExtrasCliHelper, __version__
    # import sonos_extras
    
    import argparse
    import os
    
    try:
        default_sonos_ip = os.environ["SONOS_EXTRAS_IP"]
    except:
        default_sonos_ip = ""
    
    #########################################
    ##### defining command line parsers #####
    #########################################
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--speaker-ip', type=str,
        help='IP of the speaker to connect to. Also can be set as SONOS_EXTRAS_IP environment variable', 
        default=default_sonos_ip)

    mainSubCommandParser = parser.add_subparsers(title="sub-commands", 
        description="Valid sub-commands. Use -h for each sub-commands to get detailed help.", 
        dest="sub_command")
    mainSubCommandParser.add_parser("version", aliases=["ver"], help="Print the current version.")
    mainSubCommandParser.add_parser("current", aliases="c", help="Print the current status, and playback item, if available.")
    mainSubCommandParser.add_parser("play", aliases="p", help="Play.")
    mainSubCommandParser.add_parser("pause", aliases="p", help="Pause.")
    mainSubCommandParser.add_parser("stop", aliases="s", help="Stop.")
    mainSubCommandParser.add_parser("playlists", aliases=["pls"], help="List sonos playlists.")

    volume_commandParser = mainSubCommandParser.add_parser("volume", aliases="v", help="Get/set the volume")
    volume_commandParser.add_argument("n", nargs="?", help="Value between 0 and 100 to set/increase/decrease the volume by.")
    volume_commandParser.add_argument("-f", "--force", action="store_true", help="Force volume change more than specified threshold without confirmation.")
    volume_group = volume_commandParser.add_mutually_exclusive_group()
    volume_group.add_argument("-u", "--up"  , action="store_const", const="+1"  , dest="action", help="Increase volume by n")
    volume_group.add_argument("-d", "--down", action="store_const", const="-1", dest="action", help="Decrease volume by n")

    line_in_commandParser       = mainSubCommandParser.add_parser("line_in", aliases=["li"], help="Select LineIn for playback.")
    line_in_commandParser.add_argument("n", nargs="?", type=int, default=0, help="LineIn number to select.")

    stop_after_commandParser    = mainSubCommandParser.add_parser("stop_after", aliases=["sa"], help="Stop after the current/future track(s).")
    stop_after_commandParser.add_argument("n", nargs="?", type=int, default=1, help="Stop after n-th track, including the current track.")

    resume_queue_commandParser  = mainSubCommandParser.add_parser("resume_queue", aliases=["rq"], help="Resume playback from the given index of the current queue.")
    resume_queue_commandParser.add_argument("n", nargs="?", type=int, default=1, help="Track index in the current queue.")

    print_queue_commandParser   = mainSubCommandParser.add_parser("queue", aliases="q", help="Print the current queue.")
    print_queue_commandParser.add_argument("i", nargs="?", type=int, default=1, help="Track index to start printing the queue from.")
    print_queue_commandParser.add_argument("n", nargs="?", type=int, default=0, help="Number of tracks to print from the queue. Defaults to 0, which means all remaining.")
    
    args = parser.parse_args(raw_args)
    # print(args)

    #########################################
    #####              Main             #####
    #########################################
    client = SonosExtrasCliHelper(args.speaker_ip)

    if   args.sub_command in ["current", "c"]:
        print(client.get_current_status())
    elif args.sub_command in ["version", "ver"]:
        print(__version__)
    elif args.sub_command in ["queue", "q"]:
        client.print_queue(args.i, args.n)
    elif args.sub_command in ["volume", "v"]:
        if args.action != None:
            n = int(args.n) if args.n else 3
            client.safe_set_volume(client.volume + (int(args.action) * n), args.force)
        elif args.n:
            client.safe_set_volume(int(args.n), args.force)
        print(client.volume)
    elif args.sub_command == "p":
        if client.get_current_transport_info()['current_transport_state'] in ["STOPPED", "PAUSED_PLAYBACK"]:
            client.play()
        else:
            client.pause()
    elif args.sub_command == "play":
        client.play()
    elif args.sub_command == "pause":
        client.pause()
    elif args.sub_command in ["stop", "s"]:
        client.stop()
    elif args.sub_command in ["stop_after", "sa"]:
        client.stop_after(args.n)
        print(client.get_current_status())
    elif args.sub_command in ["line_in", "li"]:
        client.switch_to_line_in(list(client.all_zones)[args.n])
        client.play()
    elif args.sub_command in ["resume_queue", "rq"]:
        client.play_from_queue(args.n - 1)
    elif args.sub_command == "add_uri_to_queue":
        uri ='x-file-cifs:' + args.uArgs[0]
        position = client.add_uri_to_queue(uri, args.uArgs[1] if len(args.uArgs) > 1 else 0)
        print(position, '|', uri)
    elif args.sub_command in ["playlists", "pls"]:
        print(client.playlists())
    elif args.sub_command == "playlist":
        client.playlist(args.uArgs[0] if args.uArgs else "")

if __name__ == "__main__":
    main()