import sh, os, time, re
from sonos_extras.module import SonosExtrasCliHelper
from sonos_extras.bin import SonosExtrasCLI

client = SonosExtrasCliHelper(os.environ["SONOS_EXTRAS_IP"])
PipenvPython = sh.pipenv.run.python

def setup_module():
    """ setup any state specific to the execution of the given class (which
    usually contains tests).
    """

def teardown_module():
    """ teardown any state that was previously setup with a call to
    setup_class.
    """

def run_command(args, inputs=""):
    result = PipenvPython("-m", "sonos_extras.bin.SonosExtrasCLI", args, _in=inputs)
    return result.__str__()

def run_command_get_digits(args, inputs=""):
    reDigits = re.compile(r"^(\d+)\n")
    cRes = run_command(args, inputs)
    return int(reDigits.match(cRes).group(1))

#################
##### TESTS #####
#################
def test_print_current_status():
    run_command(["current"])
    run_command(["c"])

def test_get_volume():
    v1 = run_command_get_digits(["volume"])
    v2 = run_command_get_digits(["v"])
    assert v1 == v2
    assert v1 in range(101)

def test_set_volume():
    current_volume = run_command_get_digits(["v"])
    vol = run_command_get_digits(["v", (current_volume - 1).__str__()])
    assert vol == current_volume - 1
    vol = run_command_get_digits(["volume", current_volume.__str__()])
    assert vol == current_volume

def test_volume_up_down():
    saved_volume = run_command_get_digits(["v"])
    vol1 = run_command_get_digits(["v", "--up"])
    assert int(vol1) > saved_volume
    vol2 = run_command_get_digits(["v", "--down"])
    assert int(vol2) == saved_volume

def test_volume_u_d():
    saved_volume = run_command_get_digits(["v"])
    vol1 = run_command_get_digits(["v", "-u"])
    assert vol1 > saved_volume
    vol2 = run_command_get_digits(["v", "-d"])
    assert vol2 == saved_volume

def test_volume_up_more_than_threshold():
    #make sure playback is stopped
    current_state = client.get_current_transport_info()['current_transport_state']
    if current_state == 'PLAYING':
        client.pause()
    original_volume = run_command_get_digits(["v"])

    vol1 = run_command_get_digits(["v", "1"])
    run_command(["v", (5 + client.volume_increase_confirmation_threshold).__str__()], inputs="n")
    vol2 = run_command_get_digits(["v"])
    assert vol2 == vol1
    vol3 = run_command_get_digits(["v", (5 + client.volume_increase_confirmation_threshold).__str__(), "--force"])
    assert vol3 == 5 + client.volume_increase_confirmation_threshold

    vol1 = run_command_get_digits(["v", "1"])
    run_command(["v", "--up", (5 + client.volume_increase_confirmation_threshold).__str__()], inputs="n")
    vol2 = run_command_get_digits(["v"])
    assert vol2 == vol1
    vol3 = run_command_get_digits(["v", "--up", 5 + client.volume_increase_confirmation_threshold, "--force"])
    assert vol3 == vol1 + 5 + client.volume_increase_confirmation_threshold

    vol1 = run_command_get_digits(["v", "1"])
    run_command(["v", "-u", 5 + client.volume_increase_confirmation_threshold], inputs="n")
    vol2 = run_command_get_digits(["v"])
    assert vol2 == vol1
    vol3 = run_command_get_digits(["v", "-u", 5 + client.volume_increase_confirmation_threshold, "-f"])
    assert vol3 == vol1 + 5 + client.volume_increase_confirmation_threshold

    run_command_get_digits(["v", original_volume, "-f"])
    if current_state == 'PLAYING':
        client.play()

def test_volume_up_down_with_value():
    saved_volume = run_command_get_digits(["v"])
    vol1 = run_command_get_digits(["v", "--up", "1"])
    assert vol1 > saved_volume
    vol2 = run_command_get_digits(["v", "--down", "1"])
    assert vol2 == saved_volume

def test_volume_u_d_with_value():
    saved_volume = run_command_get_digits(["v"])
    vol1 = run_command_get_digits(["v", "-u", "1"])
    assert vol1 > saved_volume
    vol2 = run_command_get_digits(["v", "-d", "1"])
    assert vol2 == saved_volume

def test_queue():
    queue = run_command(["q"])
    assert queue.find("Unexpected error:") == -1
    total_items = re.match(r"^Total (\d+) items in queue:", queue)
    assert total_items
    lines = re.findall(".*\n", queue)
    assert len(lines) - 2 == int(total_items.group(1))

def test_version():
    ver_re = re.compile(r"\d+\.\d+\.\d+")
    version = run_command(["version"])
    assert ver_re.match(version)
    version = run_command(["ver"])
    assert ver_re.match(version)

def test_playlists():
    pl = False
    if len(client.get_sonos_playlists()) == 0:
        #setup at least one playlist
        pl = client.create_sonos_playlist("TEMP_FOR_PYTHON_TESTING")

    re_sq = re.compile("SQ:")
    re_total = re.compile("Total:")
    playlists = run_command(["playlists"])
    # playlists = SonosExtrasCLI.main(["playlists"])
    assert re_total.search(playlists)
    assert re_sq.match(playlists)

    if pl:
        client.remove_sonos_playlist(pl)

def test_p():
    state1 = client.get_current_transport_info()["current_transport_state"]
    state2 = None

    run_command(["p"])
    # Now poll for 20 secs until the a different value shows up
    # or timeout
    count = 0
    while count < 20:
        time.sleep(1)
        state2 = client.get_current_transport_info()["current_transport_state"]
        if state2 != state1: break
        count += 1
    assert state2 != state1


    run_command(["p"])
    count = 0
    state3 = None
    while count < 20:
        time.sleep(1)
        state3 = client.get_current_transport_info()["current_transport_state"]
        if state3 == state1: break
        count += 1
    assert state3 == state1