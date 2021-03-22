from userdata_mining.mining import *
from userdata_mining.utils import flush_caches, get_username
import os


data_path = '.'


def test_autofill():
    username = get_username(data_path)

    results = parse_autofill(username, data_path=data_path)
    assert isinstance(results, list)


def test_browser_history():
    username = get_username(data_path)

    result = parse_browser_history(username, data_path=data_path)
    assert isinstance(result, list)
