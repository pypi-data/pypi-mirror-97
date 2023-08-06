from ..thirdparty import exrex
from . import BaseExtractor
from urllib.parse import urlparse
from collections import defaultdict
import re
import inspect


class Bypass(BaseExtractor):
    bypassPattern = defaultdict(lambda: defaultdict(set))
    allBypassPattern = None

    def report_bypass(self, url):
        if self.logger:
            self.logger.info(f"Bypass link unduhan {urlparse(url).netloc}: {url}")

    def bypass_url(self, url):
        """
        Bypass url

        Args:
              url: type 'str'
        """

        end = False
        prev = url
        while not end:
            found_pattern = False
            for funcName, item in self.bypassPattern.items():
                for pattern in item["pattern"]:
                  if pattern.search(url):
                    self.report_bypass(url)
                    func = getattr(self, funcName)
                    try:
                        if not (result := func(url)):
                            break
                        elif not isinstance(result, dict):
                            result = {"result": result}
                    except Exception as e:
                        if self.logger:
                            self.logger.error(f"Error: {e}")
                        result = {"result": url}
                    if not self.run_as_module:
                        return url
                    url = result[self.choice(result.keys())]
                    if url == prev:
                        break
                    prev = url
                    found_pattern = True
            if not found_pattern:
                end = True
        return re.sub(r" ", "%20", url)

    def bypass_letsupload(self, url):
        """
        regex: https?://letsupload\.[ic]o/[0-9A-Za-z]+(?:/|\?pt=)[^>]+
        """

        raw = self.session.get(url)
        if (fileId := re.search(r"(?i)showFileInformation\((\d+)\)", raw.text)):
            return self.bypass_redirect('https://letsupload.io/account/direct_download/' + fileId.group(1))
        if (nextUrl := re.search(r"window.location += ['\"]([^\"']+)", raw.text)):
            return nextUrl.group(1)

    def bypass_filesIm(self, url):
        """
        regex: https?://(?:files\.im|racaty\.net|hxfile\.co)/[^>]+
        """

        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36',
        }

        data = {
            'op': 'download2',
            'id': self.getPath(url),
            'rand': '',
            'referer': '',
            'method_free': '',
            'method_premium': '',
        }

        response = self.session.post(url, headers=headers, data=data)
        soup = self.soup(response)

        if (btn := soup.find(class_="btn btn-dow")):
            return btn["href"]
        if (unique := soup.find(id="uniqueExpirylink")):
            return unique["href"]

    def bypass_redirect(self, url):
        """
        regex: https?://(?:link\.zonawibu\.cc/redirect\.php\?go|player\.zafkiel\.net/blogger\.php\?yuzu)\=[^>]+
        """
        head = self.session.head(url)
        return head.headers.get("Location", url)

    def bypass_linkpoi(self, url):
        """
        regex: https?://(?:www\.)?uservideo\.xyz/file/[^>]+
        regex: https?://linkpoi\.me/[^>]+
        """

        raw = self.session.get(url)
        soup = self.soup(raw)

        if (a := soup.find("a", class_="btn-primary")):
            return a["href"]

    def bypass_mediafire(self, url):
        """
        regex: https?://(?:www\.)?mediafire\.com/file/[^>]+(?:/file)?
        """

        raw = self.session.get(url)
        soup = self.soup(raw)

        if (dl := soup.find(id="downloadButton")):
            return dl["href"]

    def bypass_zippyshare(self, url):
        """
        regex: https?://www\d+\.zippyshare\.com/v/[^/]+/file\.html
        """

        raw = self.session.get(url)
        res = re.search(
            r'href = "(?P<i>[^"]+)" \+ \((?P<t>[^>]+?)\) \+ "(?P<f>[^"]+)', raw.text)
        if res is not None:
            res = res.groupdict()
            return re.search(r"(^https://www\d+.zippyshare.com)", raw.url).group(1) + \
                res["i"] + str(eval(res["t"])) + res["f"]
        return url

    def bypass_fembed(self, url):
        """
        regex: https?://(?:www\.naniplay|naniplay)(?:\.nanime\.(?:in|biz)|\.com)/file/[^>]+
        regex: https?://layarkacaxxi\.icu/f/[^>]+
        """

        raw = self.session.get(url)
        api = re.search(r"(/api/source/[^\"']+)", raw.text)
        if api is not None:
            result = {}
            raw = self.session.post(
                "https://layarkacaxxi.icu" + api.group(1)).json()
            for d in raw["data"]:
                f = d["file"]
                direct = self.bypass_redirect(f)
                result[f"{d['label']}/{d['type']}"] = direct
            return result


# lazy method
allBypassPattern = []
pattern = re.compile(r"regex *: *(.+)(?:\n|$)")
for key, value in inspect.getmembers(Bypass):
    if key.startswith("bypass_"):
        for urlPattern in pattern.findall(value.__doc__ or ""):
            Bypass.bypassPattern[key]["pattern"].add(
                re.compile(urlPattern)
            )
            allBypassPattern.append(urlPattern)
        if (allPattern := Bypass.bypassPattern.get(key)):
            for rule in allPattern["pattern"]:
                valid_regex = re.sub(
                    r"\[.+?\][+*]\??|\\[a-zA-Z][+*]\??", "\[id\]", rule.pattern)
                valid_regex = re.sub(r"\.[*+]\??", "\[any\]", valid_regex)
                for url in exrex.generate(valid_regex):
                    Bypass.bypassPattern[key]["support"].add(urlparse(url).netloc.removeprefix("www."))

Bypass.allBypassPattern = re.compile(r"|".join(allBypassPattern))
