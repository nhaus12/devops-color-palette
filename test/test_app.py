import json
import pytest
import requests

# TODO: parametrize for different engines once implemented
PORT = 8000

def test_color_palette_default():
    expected = json.loads('{"special": {"background": "#1e1e1c", "foreground": "#e2e4e7", "cursor": "#e2e4e7"}, "colors": {"color0": "#1e1e1c", "color1": "#237B86", "color2": "#139EAD", "color3": "#59B3C1", "color4": "#5EB9C7", "color5": "#D0B6A3", "color6": "#A1CFDB", "color7": "#e2e4e7", "color8": "#9e9fa1", "color9": "#237B86", "color10": "#139EAD", "color11": "#59B3C1", "color12": "#5EB9C7", "color13": "#D0B6A3", "color14": "#A1CFDB", "color15": "#e2e4e7"}}')

    url = f"http://localhost:{PORT}/palette"
    files = {'image': open('./test/test-image.jpg', 'rb')}
    resp = requests.post(url, files=files).json()

    assert resp == expected