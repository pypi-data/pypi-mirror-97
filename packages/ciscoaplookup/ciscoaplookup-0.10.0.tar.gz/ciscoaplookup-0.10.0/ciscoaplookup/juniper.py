import requests
from bs4 import BeautifulSoup
from ciscoaplookup.countries import get_country_regex

compliance_url = 'https://www.juniper.net/documentation/en_US/release-independent/junos/topics/reference/' \
                 'specifications/access-point-ax411-country-channel-support.html'

_rd_by_cc = None
_rd_by_cn = None


def _init_rd_maps():
    global _rd_by_cc
    if _rd_by_cc:
        return
    global _rd_by_cn
    rd_by_cn = {}
    rd_by_cc = {}
    html = requests.get(compliance_url, allow_redirects=True).content
    parsed = BeautifulSoup(html, features="html.parser")
    table = parsed.body.find('table', attrs={'cellspacing': '0'})
    for tr in table.tbody.children:
        strings = list(tr.strings)
        if len(strings) < 4:
            break
        rd = strings[3][-2:]
        rd_by_cc[strings[0]] = rd
        rd_by_cn[strings[1].lower()] = rd

    _rd_by_cn = rd_by_cn
    _rd_by_cc = rd_by_cc



def get_domain_for(country):
    """
    Get valid domain, in a particular country.
    :param str country:
    :return:
    """
    global _rd_by_cn
    _init_rd_maps()
    if country in _rd_by_cn:
        return _rd_by_cn[country.lower()]
    pat = get_country_regex(country)
    for cn, rd in _rd_by_cn.items():
        if pat.search(cn):
            return rd
    raise ValueError('Couldn\'t find any country matching {}'.format(country))


if __name__ == '__main__':
    _init_rd_maps()
    print(get_domain_for('Viet Nam'))