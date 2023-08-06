import os, re
from sonos_extras.module import SonosExtrasCliHelper

client = SonosExtrasCliHelper(os.environ["SONOS_EXTRAS_IP"])

def test_print_current_status():
    output = client.get_current_status()
    assert output.find('current_transport_status') > 0
    assert output.find('current_transport_state') > 0
    assert output.find('current_transport_speed') > 0

def test_get_volume():
    v = client.volume
    assert int(v) in range(101)

def test_set_volume():
    current_volume = client.volume
    client.volume = current_volume - 1
    vol = client.volume
    assert int(vol) == current_volume - 1
    client.volume = current_volume
    vol = client.volume
    assert int(vol) == current_volume

def test_should_print_queue():
    queue = client.print_queue()
    assert ' '.join(queue).find("Unexpected error:") == -1
    total_items = re.match(r"^Total (\d+) items in queue:", queue[0])
    assert total_items
    assert len(queue) - 1 == int(total_items.group(1))

def test_playlists():
    pl = False
    if len(client.get_sonos_playlists()) == 0:
        #setup at least one playlist
        pl = client.create_sonos_playlist("TEMP_FOR_PYTHON_TESTING")

    re_sq = re.compile("SQ:")
    re_total = re.compile("Total:")
    playlists = client.playlists()
    assert re_total.search(playlists)
    assert re_sq.match(playlists)

    if pl:
        client.remove_sonos_playlist(pl)
