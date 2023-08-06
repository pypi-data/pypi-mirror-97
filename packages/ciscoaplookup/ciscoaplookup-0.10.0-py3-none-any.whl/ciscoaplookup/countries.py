from re import compile, IGNORECASE
import country_converter as coco


def get_country_regex(country):
    pat = coco.convert(names=country, to='regex', not_found=None)
    if not pat:
        raise ValueError('Unknown country: {}'.format(country))

    return compile(pat, IGNORECASE)



