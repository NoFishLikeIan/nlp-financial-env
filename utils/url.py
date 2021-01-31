import pandas as pd

from urllib.parse import urlparse

def get_name(url:str) -> str:

    parsed_uri = urlparse(url)

    netloc = parsed_uri.netloc

    name = netloc.split(".")[-2] if len(netloc) > 1 else netloc

    return name
