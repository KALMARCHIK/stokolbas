""" Парсеры """

from .borisovmeat import parse as parse_borsovmeat

parse_dict = {
    'borisovmeat.by': parse_borsovmeat,
    #'pikant.by': '',
    #'meat.by': '',
    #'kmk.by': ''
}

async def parse(parse_data: dict):
    for k in parse_dict:
        if k in parse_data['url']:
            return await parse_dict[k](parse_data)

    return None
