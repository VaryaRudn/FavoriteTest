import pytest
import requests
import time

@pytest.fixture
def auth_token():
    response = requests.post("https://regions-test.2gis.com/v1/auth/tokens")
    token = response.cookies.get('token')
    return token

def test_all_correct(auth_token):
    test_colors = [
        ("GREEN"),
        ("RED"),
        ("BLUE"),
        ("YELLOW")
    ]
    for i in test_colors:
        fresh_token = requests.post("https://regions-test.2gis.com/v1/auth/tokens").cookies.get('token')
        data = {
            "title": "Парк",
            "lat": 55.7558,
            "lon": 37.6173,
            "color": i
        }
        cookies = {"token": fresh_token}
        response = requests.post("https://regions-test.2gis.com/v1/favorites", data=data, cookies=cookies)
        assert response.status_code == 200

def test_correct_without_color(auth_token):
    data = {
        "title": "Парк",
        "lat": 55.7558,
        "lon": 37.6173,
    }
    cookies = {"token": auth_token}

    response = requests.post("https://regions-test.2gis.com/v1/favorites", data = data, cookies = cookies)
    assert response.status_code == 200

def test_wrong_additional_param(auth_token):
        data = {
            "title": "Парк",
            "lat": 55.7558,
            "lon": 37.6173,
            "color": "purple"
        }
        cookies = {"token": auth_token}

        response = requests.post("https://regions-test.2gis.com/v1/favorites", data=data, cookies=cookies)
        assert response.status_code == 400

def test_without_title(auth_token):
    data = {
        "lat": 55.7558,
        "lon": 37.6173,
    }
    cookies = {"token": auth_token}

    response = requests.post("https://regions-test.2gis.com/v1/favorites", data = data, cookies = cookies)
    assert response.status_code == 400

def test_without_lon(auth_token):
    data = {
        "title": "Парк",
        "lat": 55.7558
    }
    cookies = {"token": auth_token}

    response = requests.post("https://regions-test.2gis.com/v1/favorites", data = data, cookies = cookies)
    assert response.status_code == 400

def test_without_lat(auth_token):
    data = {
        "title": "Парк",
        "lon": 37.6173
    }
    cookies = {"token": auth_token}

    response = requests.post("https://regions-test.2gis.com/v1/favorites", data = data, cookies = cookies)
    assert response.status_code == 400

def test_empty_title(auth_token):
    data = {
        "title": "",
        "lat": 55.7558,
        "lon": 37.6173,
        "color": "RED"
    }
    cookies = {"token": auth_token}

    response = requests.post("https://regions-test.2gis.com/v1/favorites", data = data, cookies = cookies)
    assert response.status_code == 400


def test_lat_pos_param(auth_token):
    test_cases = [
        (-90.0),
        (90.0),
        (0.0)
    ]
    for i in test_cases:
        fresh_token = requests.post("https://regions-test.2gis.com/v1/auth/tokens").cookies.get('token')
        data = {
            "title": "Парк",
            "lat": i,
            "lon": 37.6173
        }
        cookies = {"token": fresh_token}
        response = requests.post("https://regions-test.2gis.com/v1/favorites", data=data, cookies=cookies)
        assert response.status_code == 200


def test_lat_neg_param(auth_token):
    test_cases = [
        (-90.000001),
        (90.000001),
        (-100.0),
        (100.0)
    ]
    for i in test_cases:
        fresh_token = requests.post("https://regions-test.2gis.com/v1/auth/tokens").cookies.get('token')
        data = {
            "title": "Парк",
            "lat": i,
            "lon": 37.6173
        }
        cookies = {"token": fresh_token}
        response = requests.post("https://regions-test.2gis.com/v1/favorites", data=data, cookies=cookies)
        assert response.status_code == 400


def test_lon_pos_param(auth_token):
    test_cases = [
        (-180.0),
        (180.0),
        (0.0)
    ]
    for i in test_cases:
        fresh_token = requests.post("https://regions-test.2gis.com/v1/auth/tokens").cookies.get('token')
        data = {
            "title": "Парк",
            "lat": 55.7558,
            "lon": i
        }
        cookies = {"token": fresh_token}
        response = requests.post("https://regions-test.2gis.com/v1/favorites", data=data, cookies=cookies)
        assert response.status_code == 200


def test_lon_neg_param(auth_token):
    test_cases = [
        (-180.000001),
        (180.000001),
        (-200.0),
        (200.0)
    ]
    for i in test_cases:
        fresh_token = requests.post("https://regions-test.2gis.com/v1/auth/tokens").cookies.get('token')
        data = {
            "title": "Парк",
            "lat": 55.7558,
            "lon": i
        }
        cookies = {"token": fresh_token}
        response = requests.post("https://regions-test.2gis.com/v1/favorites", data=data, cookies=cookies)
        assert response.status_code == 400

def test_long_title(auth_token):
    data = {
        "title": "а"*1000,
        "lat": 55.7558,
        "lon": 37.6173,
        "color": "red"
    }
    cookies = {"token": auth_token}

    response = requests.post("https://regions-test.2gis.com/v1/favorites", data = data, cookies = cookies)
    assert response.status_code == 400

def test_without_token():
    data = {
        "title": "а",
        "lat": 55.7558,
        "lon": 37.6173,
        "color": "RED"
    }
    response = requests.post("https://regions-test.2gis.com/v1/favorites", data = data)
    assert response.status_code == 401

def test_color_register(auth_token):
    data = {
        "title": "а" * 1000,
        "lat": 55.7558,
        "lon": 37.6173,
        "color": "red"
    }
    cookies = {"token": auth_token}

    response = requests.post("https://regions-test.2gis.com/v1/favorites", data=data, cookies=cookies)
    assert response.status_code == 400

def test_expired_token():
    token_response = requests.post("https://regions-test.2gis.com/v1/auth/tokens")
    token = token_response.cookies.get('token')
    time.sleep(3)
    data = {
        "title": "Парк",
        "lat": 55.7558,
        "lon": 37.6173,
        "color": "RED"
     }
    cookies = {"token": token}
    response = requests.post("https://regions-test.2gis.com/v1/favorites", data=data, cookies=cookies)
    assert response.status_code == 401