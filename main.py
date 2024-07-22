from flask import Flask
from faker import Faker
from typing import List
from faker.providers import internet
import random

app = Flask(__name__)


ROLES = ['edge router', 'backbone router', 'gateway router']

CATALOGS = {
    'juniper networks': ['mx480', 'mx960', 'ex3300', 'mx204'],
    'adva optical': ['xg480', 'xg304', 'xg308'],
    'ciena': [],
}


def _get_roll() -> str:
    idx = random.randint(0, len(ROLES) - 1)
    return ROLES[idx]


def _get_catalog(vendor: str) -> str:
    vendor = vendor.lower()
    idx = random.randint(0, len(CATALOGS[vendor]) - 1)
    return CATALOGS[vendor][idx]


def generate_devices(vendor: str, count: int = 20) -> List:
    fake = Faker()
    Faker.seed(0)
    fake.add_provider(internet)
    dev_list = []
    for i in range(count):
        dev_list.append({
                        'CATALOG': _get_catalog(vendor),
                        'MANUFACTURER': vendor,
                        'IPADDR': f"{fake.ipv4_private()}/24",
                        'HOSTNAME': fake.hostname(),
                        'ROLE': _get_roll(),
                        })

    return dev_list


@app.route('/api/v1/devices/<hostname>')
def get_device(hostname):
    pass


@app.route('/api/v1/vendors/<name>')
def get_vendor(name):
    return generate_devices(name)


if __name__ == "__main__":
    app.run()
