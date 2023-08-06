import re

directRules = {
    "naniplay": (re.compile(r"https?://(?:www\.)?naniplay(?:\.nanime\.(?:in|biz)|\.com)/file/[^>]+"), "fembed"),
    "layarkacaxxi": (re.compile(r"https?://layarkacaxxi\.icu/f/[^>]+"), "fembed"),
    "zippyshare": (re.compile(r"https?://www\d+\.zippyshare\.com/v/[^/]+/file\.html"), "zippyshare"),
    "mediafire": (re.compile(r"https?://(?:www\.)?mediafire\.com/file/[^>]+(?:/file)?"), "mediafire"),
    "linkpoi": (re.compile(r"https?://linkpoi\.me/[^>]+"), "linkpoi"),
    "uservideo": (re.compile(r"https?://(?:www\.)?uservideo\.xyz/file/[^>]+"), "linkpoi"),
    "ouo": (re.compile(r'https?://ouo\.io/[^>]+'), None),
    "files.im": (re.compile(r"https?://(?:files\.im|racaty\.net|hxfile\.co)/[^>]+"), "filesIm"),
    "redirect": (re.compile(r"https?://(?:link\.zonawibu\.cc/redirect\.php\?go|player\.zafkiel\.net/blogger\.php\?yuzu)\=[^>]+"), "redirect")
}

allDirectRules = re.compile(
    r"|".join(v.pattern for v, _ in directRules.values()))
