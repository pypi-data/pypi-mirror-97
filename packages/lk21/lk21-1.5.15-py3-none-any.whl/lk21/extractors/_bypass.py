from . import BaseExtractor
from ._rules import directRules, re
from urllib.parse import quote

class _Bypass(BaseExtractor):
    """
    Extractor
    """

    def bypass_url(self, url):
        end = False
        prev = url
        while not end:
            found_pattern = False
            for title, (pattern, klsname) in directRules.items():
                if klsname and pattern.search(url):
                    if self.logger is not None:
                        self.logger.info(f"Bypass link unduhan {title}: {url}")
                    func = getattr(self, f"bypass_{klsname}")
                    try:
                        if not (result := func(url)):
                            break
                        elif not isinstance(result, dict):
                            result = {"": result}
                    except Exception:
                        result = {"": url}
                    url = result[self.choice(result.keys())]
                    if url == prev:
                        break
                    prev = url
                    found_pattern = True
            if not found_pattern:
                end = True
        return quote(url, safe="://")

    def bypass_filesIm(self, url):
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
        head = self.session.head(url)
        return head.headers.get("Location", url)

    def bypass_linkpoi(self, url):
        raw = self.session.get(url)
        soup = self.soup(raw)

        if (a := soup.find("a", class_="btn-primary")):
            return a["href"]

    def bypass_mediafire(self, url):
        raw = self.session.get(url)
        soup = self.soup(raw)

        if (dl := soup.find(id="downloadButton")):
            return dl["href"]

    def bypass_zippyshare(self, url):
        raw = self.session.get(url)
        res = re.search(
            r'href = "(?P<i>[^"]+)" \+ \((?P<t>[^>]+?)\) \+ "(?P<f>[^"]+)', raw.text)
        if res is not None:
            res = res.groupdict()
            return re.search(r"(^https://www\d+.zippyshare.com)", raw.url).group(1) + \
                res["i"] + str(eval(res["t"])) + res["f"]
        return url

    def bypass_fembed(self, url):
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
