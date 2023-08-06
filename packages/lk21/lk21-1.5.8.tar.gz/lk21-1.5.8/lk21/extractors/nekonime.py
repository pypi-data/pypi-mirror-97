from . import BaseExtractor


class Nekonime(BaseExtractor):
    host = "https://nekonime.stream"
    tag = "anime"
    required = ["proxy"]

    def extract_meta(self, id: str) -> dict:
        """
        Ambil semua metadata dari halaman web

        Args:
              id: type 'str'
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        meta = self.MetaSet()
        content = soup.find(id="info", role="tabpanel")

        alias = {"Skor": "score", "Diterbitkan Nekonime": "diunggah"}
        for div in content.findAll(style="margin-bottom: 7px;"):
            k, v = self.re.split(r"\s*:\s*", div.text)
            meta.add(alias.get(k, k), v)

        sinop = soup.find(id="sinopsis")
        sinop.h2.decompose()
        meta["sinopsis"] = sinop.text

        return meta

    def extract_data(self, id: str) -> dict:
        """
        Ambil semua situs unduhan dari halaman web

        Args:
              id: jalur url dimulai setelah host, type 'str'

        Returns:
              dict: hasil 'scrape' halaman web
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        d = {}
        if (eps := soup.find(class_="daftarepi")):
            for a in eps.findAll("a"):
                d[a.text] = "re:" + self.getPath(a["href"])
            return d

        if (eps := soup.find(class_="flircontainer")):
            alleps = eps.find("a", text="All Eps")
            d[alleps.text] = "re:" + self.getPath(alleps["href"])

        if (ddl := soup.find(class_="soraddl")):
            for p in ddl.findAll(class_="soraurl"):
                result = {}
                for a in p.findAll("a"):
                    result[a.text] = a["href"]
                d[p.strong.text] = result
        return d

    def search(self, query: str, page: int = 1) -> list:
        """
        Cari item berdasarkan 'query' yang diberikan

        Args:
              query: kata kunci pencarian, type 'str'
              page: indeks halaman web, type 'int'

        Returns:
              list: daftar item dalam bentuk 'dict'
        """

        raw = self.session.get(f"{self.host}/page/{page}", params={"s": query})
        soup = self.soup(raw)

        result = []
        for article in soup.findAll(class_="article-body"):
            a = article.find("a")
            result.append({
                "title": a.text,
                "id": self.getPath(a["href"])
            })
        return result
