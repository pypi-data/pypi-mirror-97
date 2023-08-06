# -*- coding: utf-8 -*-
import re

def parse_value_from_type(value, api):
    if isinstance(value, int):
        return int(value)
    elif isinstance(value, float):
        return float(value)
    elif value.lower() == "false":
        return False
    elif value.lower() == "true":
        return True
    else:
        value = str(value)
        for v in re.findall(r'\{\{.+?\}\}', value):
            api['config']["variables"][v[2:-2]] = ''
            value = value.replace(v, '${{{}}}'.format(v[2:-2]))
        return value