from userdata_mining.mining import parse_maps_data
from userdata_mining.utils import flush_caches
import os
from numbers import Number


def get_username():
    """
    Fetches the user whose data is on disk.
    """
    users = os.listdir('../data/')
    if len(users) == 0:
        print('WARN: No users to mine.')
        return None
    else:
        return users[0]


def test_parse_maps_data():
    # Fetch the username
    username = get_username()
    if username is None:
        assert True
        return

    # Delete the caches
    flush_caches()

    # Call the function
    results = parse_maps_data(username)

    assert isinstance(results, dict)
    assert len(list(results.keys())) == 3
    assert 'total_distance' in results.keys()
    assert 'places' in results.keys()
    assert 'fuel_needed' in results.keys()

    assert isinstance(results['total_distance'], Number)
    assert isinstance(results['places'], list)
    assert isinstance(results['fuel_needed'], Number)


def test_cache_works():
    caches = os.listdir('../caches/')
    assert '.maps.cache' in caches
