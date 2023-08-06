from urllib.parse import urlparse
import requests
import requests_cache
import bs4
import re
import questionary
import sys
import glob
import os
import importlib

from ..utils import MetaSet


class BaseExtractorError(Exception):
    pass


requests_cache.install_cache(cache_name=os.path.expanduser(
    '~/.lk21-requests-cache'), backend='sqlite', expire_after=180)


class BaseExtractor:
    def __init__(self, logger=None, args=None):
        """
        Induk dari semua 'extractor'

        Args:
              logger: logger instance
              args: 'argparse.Namespace'
        """

        self.session = self._build_session()
        self.re = re
        self.logger = logger
        self.args = args
        self.printInfo = args.info if args else None
        self.counter = 0
        self.to_list = True

        self.MetaSet = MetaSet

    def _build_session(self) -> requests.Session:
        """
        Buat session baru
        """

        session = requests.Session()
        session.headers[
            "User-Agent"] = "Mozilla/5.0 (Linux; Android 7.0; 5060 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36"
        return session

    def setProxies(self, proxy: str) -> None:
        if not proxy:
            return
        if self.logger:
            self.logger.info(f"Menyetel proxy: {proxy}")
        self.session.proxies = {
            "http": f"http://{proxy}",
            "https": f"https://{proxy}"
        }

    def prepare(self):
        """
        ubah :self: sebelum membuat permintaan
        """

        pass

    def dict_to_list(self, d: dict) -> list:
        """
        undocumented
        """
        if not self.to_list:
            return d
        list_ = []
        for k, v in d.items():
            if isinstance(v, dict):
                v = self.dict_to_list(v)
            elif isinstance(v, str) and v.startswith("re:"):
                v = self.host + "/" + v[3:]
            list_.append({
                "key": k.strip(),
                "value": v
            })
        return list_

    def extract_meta(self, id: str) -> dict:
        """
        Ambil semua metadata dari halaman web

        Args:
              id: type 'str'
        """

        return {}

    def extract_data(self, id: str) -> dict:
        """
        Ambil semua situs unduhan dari halaman web

        Args:
              id: jalur url dimulai setelah host, type 'str'
        """

        return {}

    def filterNonetypeDict(self, items: list, keys: tuple) -> list:
        """
        undocumented
        """

        filtered = []
        for item in items:
            if all(item.get(k) not in [None, ""] for k in keys):
                filtered.append(item)
        return filtered

    def extract(self, id: any) -> dict:
        """
        Args:
            id: type 'dict' or 'str'
        """

        if isinstance(id, dict):
            if not id.get("id"):
                raise BaseExtractorError("You must provide a `id` value")
            id = id["id"]

        result = {
            "extractor": self.__class__.__name__,
            "url": f"{self.host}/{id}",
            "host": self.host,
            "id": id,
        }
        result["metadata"] = self.extract_meta(id)
        result["download"] = self.dict_to_list(
            self.extract_data(id))

        return result

    def soup(self, raw: str) -> bs4.BeautifulSoup:
        """
        Ubah 'requests.Response' atau 'str' menjadi 'bs4.BeautifulSoup'

        Args:
              raw: type 'requests.Response' atau 'str'
        """

        text = raw.text if hasattr(raw, "text") else raw
        return bs4.BeautifulSoup(text, "html.parser")

    def getPath(self, url: str) -> str:
        """
        undocumented
        """

        return urlparse(url).path.strip("/")

    def _write(self, soup: bs4.BeautifulSoup, file: str = "x.html") -> None:
        """
        Args:
              soup: type 'requests.Response' atau 'str'
              file: type 'str'
        """

        if hasattr(soup, "prettify"):
            soup = soup.prettify()
        with open(file, "wb") as f:
            f.write(soup.encode())

    def _reformat(self, raw: str, add_counter: bool = True) -> str:
        """
        Reformat text
        """

        if not isinstance(raw, str) or re.match(r"^\d+\.", raw):
            return raw
        else:
            self.counter += 1
            raw = re.sub(r"^\s+|\s+$", "", raw)
            if add_counter:
                return f"{self.counter}. {raw}"
            else:
                return raw

    def info(self, *args, **kwargs):
        """
        undocumented
        """

        if self.printInfo:
            self.logger.info(*args, **kwargs)

    def choice(self, choices, msg=None, reset_counter=True, otype="list"):
        """
        undocumented
        """

        try:
            if reset_counter:
                self.counter = 0
            choices = list(choices)
            if len(choices) == 0:
                sys.exit("Pilihan kosong")

            if len(choices) == 1:
                return choices[0]

            if otype == "list":
                nch = {
                    self._reformat(v): v for v in choices}
                prompt = questionary.select(
                    message=msg or "Pilih:",
                    choices=nch.keys()
                )
            elif otype == "checkbox":
                choices = [
                    {"name": self._reformat(k["name"], add_counter=False),
                     "checked": k["checked"]} if isinstance(k, dict) else k
                    for k in choices]
                prompt = questionary.checkbox(
                    message=msg or "Pilih:",
                    choices=choices,
                    validate=lambda x: "Pilihan tidak boleh kosong" if len(
                        x) == 0 else True
                )
            else:
                raise TypeError(f"{otype!r} is not allowed")

            if (output := prompt.ask()):
                valid_id = re.compile(r" \(direct\)$")
                if isinstance(output, str):
                    return valid_id.sub("", nch[output])
                return [valid_id.sub("", o) for o in output]
        except Exception:
            sys.exit(1)


basedir = os.path.dirname(__file__)
for file in glob.glob(f"{basedir}/*.py"):
    filename = os.path.basename(file)[:-3]
    if not filename.startswith("__"):
        importlib.import_module(f"lk21.extractors.{filename}")
