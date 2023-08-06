import re
from typing import Any
from decimal import Decimal
from urllib.parse import urlparse, parse_qs

UTM_PARAMS = [
    'utm_source',
    'utm_medium',
    'utm_campaign',
    'utm_term',
    'utm_content',
    'utm_referrer',
]

__all__ = (
    'parse_utm',
    'get_operations',
    'calc',
    'calculate',
    'remove_tags',
    'replacer',
    'UTM_PARAMS',
)


def parse_utm(url: str) -> dict:
    """
    :param url: str
    :return: dict
    """
    out = {}
    try:
        url_params = parse_qs(urlparse(url.replace('#', '')).query)
        for utm in UTM_PARAMS:
            if utm in url_params:
                out[utm] = url_params[utm][0]
        return out
    except (KeyError, ValueError, IndexError, TypeError):
        return {}


def get_operations(data: dict) -> dict:
    """
    create valid calculation dict
    :param data: dict
    :return: dict
    """
    if data:
        if "cogs" in data or "crm_net_cost" in data:
            data["first_cost"] = (
                data.pop('cogs') if "cogs" in data else data.pop('crm_net_cost')
            )
        if "revenue" in data or "crm_deal_cost" in data:
            data['transaction_amount'] = (
                data.pop('revenue') if "revenue" in data else data.pop('crm_deal_cost')
            )
        return {
            field: str(data[field]).replace('{', '').replace('}', '')
            for field in data
            if data[field]
        }
    return {}


def calc(s: str) -> str:
    """
    :param s: str (value like ('(1 * 2) / 3'))
    :return: str (result of math operation)
    """
    val = s.group()
    if not val.strip():
        return val
    return "%s" % eval(val.strip(), {'__builtins__': None})


def calculate(s: str) -> str:
    """
    :param s: str
    :return: str
    """
    return re.sub(r"([0-9\ \.\+\*\-\/(\)]+)", calc, s)


def replacer(string: str, name: str, value: Any) -> str:
    """
    replace for calculated data
    :param string: str
    :param name: str
    :param value: Any
    :return: str
    """
    string = string.replace(name, Decimal(value).__str__())
    return string


def remove_tags(text: str) -> str:
    """
    remove html tags from text
    :param text: str
    :return: str
    """
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)
