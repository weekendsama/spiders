import os
import re
import requests
from lxml import etree


def parse(url):
    raw_url = requests.get(url)
    if raw_url.status_code != 200:
        parse(url)
    return etree.HTML(raw_url)
