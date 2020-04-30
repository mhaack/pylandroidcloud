import os

import httpretty
from pytest import fixture

from pylandroidcloud import (
    BASE_URL,
    LandroidAPI,
    LandroidMower,
    LandroidMowerList,
    LandroidMowerState,
)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestLandroidApi:
    @fixture
    @httpretty.activate
    def client(self):
        with open(os.path.join(CURRENT_DIR, "get_token.json"), "r") as get_token:
            httpretty.register_uri(
                httpretty.POST, BASE_URL + "/oauth/token", body=get_token.read()
            )

        return LandroidAPI("1", "faa", "user", "password")

    @httpretty.activate
    def test_landroidmowerlist(self, client):
        with open(os.path.join(CURRENT_DIR, "get_mowers.json"), "r") as get_mowers:
            httpretty.register_uri(
                httpretty.GET, BASE_URL + "/product-items", body=get_mowers.read()
            )
        with open(os.path.join(CURRENT_DIR, "get_token.json"), "r") as get_token:
            httpretty.register_uri(
                httpretty.POST, BASE_URL + "/oauth/token", body=get_token.read()
            )

        mowers = LandroidMowerList(client).mowers
        assert len(mowers) == 1
        assert mowers[0].id == 1
        assert mowers[0].serial_number == "123456789ABCEDF"

    @httpretty.activate
    def test_landroidmower(self, client):
        with open(os.path.join(CURRENT_DIR, "get_mower.json"), "r") as get_mower:
            httpretty.register_uri(
                httpretty.GET,
                BASE_URL + "/product-items/123456789ABCEDF",
                body=get_mower.read(),
            )
        mower = LandroidMower(client, "123456789ABCEDF").mower
        assert mower.id == 1
        assert mower.serial_number == "123456789ABCEDF"
        assert mower.name == "Mower"

    @httpretty.activate
    def test_landroidmowerstate(self, client):
        with open(
            os.path.join(CURRENT_DIR, "get_mower_status.json"), "r"
        ) as get_mower_status:
            httpretty.register_uri(
                httpretty.GET,
                BASE_URL + "/product-items/123456789ABCEDF/status",
                body=get_mower_status.read(),
            )
        mower_status = LandroidMowerState(client, "123456789ABCEDF").state
        assert mower_status.config.serial_number == "123456789ABCEDF"
        assert mower_status.status_code == 1
        assert mower_status.error_code == 5
        assert mower_status.battery.charge_cycle == 42
