from userdata_mining.mining import *
from userdata_mining.utils import flush_caches, get_username
import os
from numbers import Number


def test_maps_distance():
    eb2_coords = [35.772118381683015, -78.67368013731435]
    talley_coords = [35.783540341056266, -78.67065028705414]
    result = get_maps_distance([eb2_coords, talley_coords])
    assert isinstance(result, float)
    assert result > 0


def test_nearby_places():
    talley_coords = [35.783540341056266, -78.67065028705414]
    result = get_nearby_places(talley_coords)
    assert isinstance(result, list)
    assert len(result) > 0


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
    results = parse_maps_data('rahul')
    caches = os.listdir('./caches/')
    assert '.maps.cache' in caches
