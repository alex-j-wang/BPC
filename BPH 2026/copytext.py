#!/usr/bin/env python3
import os
import re
import sys
import urllib.parse
import urllib.request

IMG_TAG_RE = re.compile(
    r'<img\s+[^>]*src="([^"]+)"[^>]*/?>',
    re.IGNORECASE
)

NEXT_IMAGE_RE = re.compile(
    r'_next/image\?url=([^&"]+)'
)

GOOGLE_BLOCK_RE = re.compile(
    r'\s*"application/x-vnd\.google[^"]*"\s*:\s*`.*?`,?\s*',
    re.DOTALL
)

TEXT_HTML_RE = re.compile(
    r'"text/html"\s*:\s*`(.*?)`',
    re.DOTALL
)


def check_url_exists(url: str):
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req) as resp:
            if resp.status >= 400:
                raise RuntimeError(f"HTTP {resp.status}")
    except Exception as e:
        raise RuntimeError(f"Image not reachable: {url} ({e})")


def transform_html(html: str, file_path: str) -> str:
    def replace_img(match):
        src = match.group(1)

        # fully decode HTML entities repeatedly
        while "&amp;" in src:
            src = src.replace("&amp;", "&")

        parsed = urllib.parse.urlparse(src)
        qs = urllib.parse.parse_qs(parsed.query)

        if "url" not in qs:
            return match.group(0)

        decoded_url = urllib.parse.unquote(qs["url"][0])

        # rebuild with original params preserved
        params = {"url": decoded_url}
        for k in ("w", "q"):
            if k in qs:
                params[k] = qs[k][0]

        clean_query = urllib.parse.urlencode(params, safe="/")
        clean = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{clean_query}"

        check_url_exists(clean)

        return f'=IMAGE("{clean}")'
        

def process_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # remove google metadata blocks
    text = GOOGLE_BLOCK_RE.sub("", text)

    def replace_html(match):
        html = match.group(1)
        new_html = transform_html(html, path)
        return f'"text/html": `{new_html}`'

    text = TEXT_HTML_RE.sub(replace_html, text)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main(root):
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name == "data.tsx":
                path = os.path.join(dirpath, name)
                print(f"Processing {path}")
                try:
                    process_file(path)
                except Exception as e:
                    print(f"ERROR in {path}: {e}")
                    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: copytext.py <directory>")
        sys.exit(1)

    main(sys.argv[1])