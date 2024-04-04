from network import STA_IF, AP_IF, WLAN
from credentials import WIFI_SSID, WIFI_PASSWORD, END_POINT_API
from time import sleep
import urequests as requests

station = WLAN(STA_IF)
station.active(True)
station.disconnect()
station.connect(WIFI_SSID, WIFI_PASSWORD)


class Network:
    def __init__(self, ssid, passwd) -> None:
        self.ssid = ssid
        self.passwd = passwd
        self.station = WLAN(STA_IF)
        self.ap = WLAN(AP_IF)

    def connect_station(self):
        self.station.active(True)
        self.station.disconnect()
        self.station.connect(self.ssid, self.passwd)
        print("Connecting to '" + self.ssid + "'")
        while not self.station.isconnected():
            print(".", end="")
            sleep(0.5)
        else:
            print("\nConnected ", station.ifconfig())

    def connect_ap(
        self, ip: str = "192.168.4.1", max_clients: int = 10, channel: int = 6
    ):
        self.ap.active(True)
        self.ap.config(essid=self.ssid, password=self.passwd)
        self.ap.config(max_clients=max_clients)
        self.ap.config(authmode=3)
        self.ap.config(channel=channel)

        ip = ip.split(".")
        self.gateway = f"{ip[0]}.{ip[1]}.{ip[2]}.1"
        self.ap.ifconfig((ip, "255.255.255.0", self.gateway, "8.8.8.8"))
