from . import BaseExtractor
from ._rules import directRules, re


class _direct(BaseExtractor):
    """
    Extractor
    """

    def extract_direct_url(self, url):
        end = False
        while not end:
            found_pattern = False
            for title, (pattern, klsname) in directRules.items():
                if klsname and pattern.search(url):
                    if self.logger is not None:
                        self.logger.info(f"Mengekstrak {title}: {url}")
                    func = getattr(self, klsname)
                    try:
                        if not (result := func(url)):
                            break
                        elif not isinstance(result, dict):
                            result = {"": result}
                    except Exception:
                        result = {"": url}
                    url = result[self.choice(result.keys())]
                    found_pattern = True
            if not found_pattern:
                end = True
        return url

    def _redirect(self, url):
        head = self.session.head(url)
        return head.headers.get("Location", url)

    def _linkpoi(self, url):
        raw = self.session.get(url)
        soup = self.soup(raw)

        if (a := soup.find("a", class_="btn-primary")):
            return a["href"]

    def _mediafire(self, url):
        raw = self.session.get(url)
        soup = self.soup(raw)

        if (dl := soup.find(id="downloadButton")):
            return dl["href"]

    def _zippyshare(self, url):
        raw = self.session.get(url)
        res = re.search(
            r'href = "(?P<i>[^"]+)" \+ \((?P<t>[^>]+?)\) \+ "(?P<f>[^"]+)', raw.text)
        if res is not None:
            res = res.groupdict()
            return re.search(r"(^https://www\d+.zippyshare.com)", raw.url).group(1) + \
                res["i"] + str(eval(res["t"])) + res["f"]
        return url

    def _fembed(self, url):
        raw = self.session.get(url)
        api = re.search(r"(/api/source/[^\"']+)", raw.text)
        if api is not None:
            result = {}
            raw = self.session.post(
                "https://layarkacaxxi.icu" + api.group(1)).json()
            for d in raw["data"]:
                f = d["file"]
                direct = self._redirect(f)
                result[f"{d['label']}/{d['type']}"] = direct
            return result
