#!/usr/bin/python
from .thirdparty.exrex import generate as generate_strings
from .extractors._rules import allDirectRules, directRules
from .extractors import BaseExtractor
from .options import ArgumentParser
from .utils import parse_range
from urllib.parse import urlparse
from pkg_resources import parse_version
from . import __version__
import logging
import questionary
import sys
import re
import json
import colorama
colorama.init()


logging.basicConfig(format=f"\x1b[K%(message)s", level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)

'''
logging.info(f"""
  _____     ___  ____    _____    __
 |_   _|   |_  ||_  _|  / ___ `. /  |
   | |       | |_/ /   |_/___) | `| |
   | |   _   |  __'.    .'____.'  | |
  _| |__/ | _| |  \ \_ / /_____  _| |_
 |________||____||____||_______||_____| {__version__}
""")
'''


def title(text, rtn=False):
    r = f" [\x1b[92m{text}\x1b[0m]"
    if rtn:
        return r
    logging.info(r)


def _check_version():
    try:
        base = BaseExtractor()
        raw = base.session.get("https://pypi.org/project/lk21", timeout=2)
        soup = base.soup(raw)

        if (name := soup.find(class_="package-header__name")):
            version = name.text.split()[-1]
            if parse_version(__version__) < parse_version(version):
                return (
                    "\x1b[93m"
                    f"WARNING: Anda menggunakan lk21 versi {__version__}, sedangkan versi {version} telah tersedia.\n"
                    "Anda harus mempertimbangkan untuk mengupgrade melalui perintah 'python -m pip install --upgrade lk21'."
                    "\x1b[0m")
    except Exception:
        return


def recursive_choice(extractor, result):
    prevresult = None
    index = 0
    last = False

    #selected_items = []
    while True:
        # if last is True:
        #    otype = "checkbox"
        #    keys = [{
        #            "name": f"{key} (direct)" if isinstance(
        #                value, str) and allDirectRules.search(value) else key,
        #            "checked": result.get(key) in selected_items
        #        } for key, value in result.items() if value]
        #    keys.extend([questionary.Separator(), {
        #        "name": "00. Kembali",
        #        "checked": False
        #    }])
        #    print (keys, selected_items)
        # else:
        #   otype = "list"

        keys = [
            f"{key} (direct)" if isinstance(
                value, str) and allDirectRules.search(value) else key
            for key, value in result.items() if value
        ]
        if prevresult and index > 0:
            keys.extend([questionary.Separator(), "00. Kembali"])

        key = extractor.choice(keys)

        # if isinstance(key, list):
        #    for k in key:
        #        if (v := result.get(k)):
        #            selected_items.append(v)

        if "00. Kembali" in key:
            last = False
            result = prevresult
            index -= 1
        else:
            prevresult = result
            index += 1
            result = result[key]

        if (index == 1 and isinstance(result, str)) or last is True:
            break

        if not all(isinstance(v, dict) for v in result.values()):
            last = True

    prefix = re.compile("^(?:" + r"|".join([extractor.host, "re\:"]) + ")")
    if prefix.search(result):
        id = extractor.getPath(prefix.sub("", result))
        logging.info(f"Mengekstrak link unduhan: {id}")
        result = extractor.extract(id).get("download", {})
        result = recursive_choice(extractor, result)
    return result


def main():
    extractors = {
        obj.__name__.lower(): obj for obj in BaseExtractor.__subclasses__() if obj
    }
    _version_msg = _check_version()

    parser = ArgumentParser(**{
        "extractors": extractors,
        "version_msg": _version_msg,
    })
    args = parser.parse_args()

    if args.version:
        sys.exit(__version__)

    _direct = extractors.pop("_direct")(logging)

    if args.list_bypass:
        def add_color(x): return x.replace(r"[id]", "\x1b[33m[id]\x1b[0m")
        for name, (rule, _) in directRules.items():
            if _ is not None:
                valid_url = re.sub(
                    r"\[\^.+?\][+*]|\\[a-zA-Z][+*]", "\[id\]", rule.pattern)
                logging.info(title(name, rtn=True))
                for s in generate_strings(valid_url):
                    logging.info(f"  - {add_color(s)}")
        sys.exit(0)
    elif args.extract_direct:
        logging.info(
            "\n" + _direct.extract_direct_url(args.extract_direct) + "\n")
        sys.exit(0)

    if not args.query or (args._exec and "{}" not in args._exec):
        parser.print_help()
        sys.exit(0)

    extractor = extractors["layarkaca21"]
    for egn, kls in extractors.items():
        if args.__dict__[egn]:
            extractor = kls
            break

    extractor = extractor(logging, args)
    if "proxy" in getattr(extractor, "required", []) and not args.skip_proxy:
        if not args.proxy:
            parser.error(
                f"{extractor.__class__.__name__} required arguments --proxy, or skip using the --skip-proxy argument if already using vpn")

    extractor.to_list = args.json or args.json_dump

    if not extractor.tag and not args.debug:
        sys.exit(f"Module {extractor.__module__} belum bisa digunakan")
    query = " ".join(args.query)
    extractor.prepare()

    id = False
    nextPage = True
    Range = parse_range(args.page)
    netloc = urlparse(extractor.host).netloc
    try:
        page = Range.__next__()
        cache = {page: extractor.search(query, page=page)}
        while not id:
            print(
                f"Mencari {query!r} -> {netloc} halaman {page}")
            logging.info(
                f"Total item terkumpul: {sum(len(v) for v in cache.values())} item dari total {len(cache)} halaman")
            if not cache[page]:
                sys.exit("Tidak ditemukan")

            if len(cache[page]) == 1:
                response = f"1. " + cache[page][0]["title"]
            else:
                response = extractor.choice([
                    i['title'] for i in cache[page]] + [
                    questionary.Separator(), "00. Kembali", "01. Lanjut", "02. Keluar"], reset_counter=False)
            pgs = list(cache.keys())
            index = pgs.index(page)
            if response.endswith("Keluar"):
                break
            elif response.endswith("Kembali"):
                if extractor.counter > -1:
                    extractor.counter -= len(cache[page])
                print("\x1b[3A\x1b[K", end="")
                if index > 0 and len(pgs) > 1:
                    page = pgs[index - 1]
                    extractor.counter -= len(cache[page])
            elif response.endswith("Lanjut") and nextPage is True:
                if index >= len(pgs) - 1:
                    try:
                        ppage = Range.__next__()
                        if len(res := extractor.search(query, page=page)) > 0:
                            page = ppage
                            cache[page] = res
                        else:
                            extractor.counter -= len(cache[page])
                    except StopIteration:
                        nextPage = False
                else:
                    page = pgs[index + 1]
                if nextPage:
                    print("\x1b[3A\x1b[K", end="")
            else:
                for r in cache[page]:
                    if r.get("title") == re.sub(r"^\d+\. ", "", response):
                        id = r["id"]
                        break
        if id:
            logging.info(f"Mengekstrak link unduhan: {id}")
            result = extractor.extract(id)

            if args.json:
                sys.exit(f"\n{result}\n")
            elif args.json_dump:
                with open(args.json_dump, "w") as file:
                    file.write(json.dumps(result, indent=2, default=lambda o: o.store
                                          if isinstance(getattr(o, "store"), dict) else o.__dict__))
                sys.exit(
                    f"Menyimpan hasil unduhan kedalam file: {args.json_dump!r}")

            # cetak informasi jika ada
            extractor.info(f"\n [\x1b[92m{r.pop('title')}\x1b[0m]")
            for k, v in result.get("metadata", {}).items():
                extractor.info(
                    f"   {k}: {', '.join(filter(lambda x: x, v)) if isinstance(v, list) else v}")
            extractor.info("")

            result = result.get("download", {})
            dlurl = recursive_choice(extractor, result)
            url = _direct.extract_direct_url(dlurl)

            if args._exec:
                os.system(args._exec.format(url))
            else:
                logging.info("")
                title("Url Dipilih")
                logging.info(f"\n{url}\n")

    except Exception as e:
        logging.info(f"{e}")
        if args.debug:
            raise

    if _version_msg:
        logging.warning(_version_msg)
