import platform
import re
import struct
import os
import zipfile
import tarfile
from bs4 import BeautifulSoup
import requests
is_64bit = struct.calcsize('P') * 8 == 64


def getGeckoDriver():
    print(os.getcwd())
    if len([x for x in os.listdir(os.getcwd()) if re.search("gecko", x)]) > 0:
        return True
    system = platform.system()
    suffix = "32"
    if is_64bit:
        suffix = "64"
    print(system)
    if system.lower() == "windows":
        links = getLinks("win" + suffix)
        print(links[0])
        path = os.getcwd() +"/"+ links[0].split("/")[-1]
        print(path)
        download_url(url=links[0], save_path=path)
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())
        return True
    if system.lower() == "linux":
        links = getLinks("linux" + suffix)
        extract_tar(links)
        return True
    if system.lower() == "darwin":
        links = getLinks("mac" + suffix)
        extract_tar(links)
        return True
    return False


def extract_tar(links):
    path = os.getcwd() + "/" + links[0].split("/")[-1]
    print(path)
    download_url(url=links[0], save_path=path)
    file = tarfile.open(path)
    file.extractall(os.getcwd())
    file.close()


def getLinks(current_os):
    URL = 'https://github.com/mozilla/geckodriver/releases'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.find_all('a')
    output = []
    for i in links:
        if "href" in i.attrs:
            if re.search(current_os, i.attrs["href"]):
                output.append("https://github.com" + i["href"])
    return output


def download_url(url, save_path, chunk_size=128):
    print("Install GeckoDriver...(Required to use WebProcessor)",url)
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)
    print("Finished Installing GeckoDriver")


