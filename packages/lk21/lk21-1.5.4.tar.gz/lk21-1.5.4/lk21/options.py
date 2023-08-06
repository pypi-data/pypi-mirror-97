from .thirdparty.exrex import getone as regex_to_string
from shutil import get_terminal_size
from .extractors._rules import allDirectRules
from urllib.parse import urlparse
import argparse
import re


def ArgumentParser(**kwargs):
    extractors = kwargs.pop("extractors")
    version_msg = kwargs.pop("version_msg")

    parser = argparse.ArgumentParser(
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(
            prog, max_help_position=get_terminal_size().lines),
        epilog=version_msg)

    parser.add_argument("query", metavar="query",
                        nargs="*", help="kueri, judul, kata kunci")
    parser.add_argument("--version", action="store_true",
                        help="show version and exit")
    parser.add_argument("-d", "--debug", action="store_true",
                        help=argparse.SUPPRESS)
    parser.add_argument("-p", metavar="page", dest="page",
                        help=("halaman situs, contoh penggunaan:\n"
                              "  - 1,2,3\n"
                              "  - 1:2, 2:8\n"
                              "  - 1,2,3:8\n"
                              "  - default halaman pertama\n"
                              "    dan seterusnya"), type=str, default="1:")
    parser.add_argument("-i", "--information", dest="info",
                        action="store_true", help="cetak informasi dari item yang dipilih")
    parser.add_argument("--exec", metavar="cmd", dest="_exec",
                        help=("jalankan 'perintah' dengan argument berupa\n"
                              "url yang dipilih.\n\n"
                              "contoh: axel2 {}"))

    valid_e_rules = re.compile(
        r"\[\^.+?\][+*]")
    valid_allDirectRules = valid_e_rules.sub(
        "[A-Za-z0-9-.]{5,7}", allDirectRules.pattern)
    parser.add_argument("-e", "--extract-direct", metavar="url",
                        help=("bypass situs download\n\n"
                              f"contoh url: {regex_to_string(valid_allDirectRules, 3)!r}\n"
                              ))

    parser.add_argument("--list-bypass", action="store_true",
                        help="cetak semua daftar situs download yang dapat\ndi-bypass")

    parser.add_argument("--json-dump", metavar="filename",
                        help="simpan hasil ekstraksi unduhan")
    parser.add_argument("--json", action="store_true",
                        help="cetak hasil ekstraksi unduhan")

    proxies = parser.add_argument_group("Proxies")
    proxies.add_argument("--proxy", metavar="url",
                         help="gunakan HTTP/HTTPS/SOCKS proxy")
    proxies.add_argument("--skip-proxy", action="store_true",
                         help="lewati penggunakan argument --proxy")

    extractor_group = parser.add_argument_group("Daftar Extractor",
                                                description=(
                                                    f"pilih salah satu dari {len(extractors)} situs berikut:"
                                                ))
    extractor_exclusiveGroup = extractor_group.add_mutually_exclusive_group()
    for egn, kls in extractors.items():
        egn = egn.replace("_", "-")
        if hasattr(kls, "host"):
            pa = urlparse(kls.host)
            for index in range(1, len(egn)):
                try:
                    arg = [f"-{egn[:index]}".rstrip("-")]
                    if arg[0] != f"-{egn}":
                        arg.append(f"--{egn}")
                    extractor_exclusiveGroup.add_argument(*arg, action="store_true",
                                                          help=f"site: {pa.scheme}://{pa.netloc} [{kls.tag}]")
                    break
                except argparse.ArgumentError:
                    continue
    return parser
