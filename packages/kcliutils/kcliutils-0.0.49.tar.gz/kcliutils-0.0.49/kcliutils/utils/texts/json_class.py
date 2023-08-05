# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Dict
import string

# Local
from .core_texts import json_class
from .utils import comment_line, multi_replace

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

def new_json_class(class_name: str, d: Dict[str, any]) -> str:
    return multi_replace(
        json_class,
        {
            '[CLASS_NAME]': class_name,
            '[CLASS_NAME_COMMENT_LINE]': comment_line('class: {}'.format(class_name)),
            '[INIT_VARS]': __init_vars_str(d)
        }
    )


# ----------------------------------------------------------- Private methods ------------------------------------------------------------ #

def __init_vars_str(
    d: Dict[str, any],
    indent_spaces: int = 4
) -> str:
    init_strs = []
    key_pairs = {k:__formatted_key(k) for k in d.keys()}
    longest = len(sorted(key_pairs.values(), key=len)[-1])

    for k, fk in key_pairs.items():
        init_strs.append(
            '{}self.{}{} = d.get(\'{}\')'.format(
                ' ' * 2 * indent_spaces,
                fk,
                ' ' * (longest - len(fk)),
                k
            )
        )

    return '\n'.join(init_strs)

def __formatted_key(s: str) -> str:
    _s = ''
    last_c = None

    for i, c in enumerate(s):
        if c in string.punctuation:
            if last_c == '_':
                last_c = c

                continue

            c = '_'
        elif c in string.ascii_uppercase:
            if last_c and '_' in last_c:
                c = c.lower()
                last_c = c
                _s += c

                continue

            c = '{}{}'.format('_' if i > 0 else '', c.lower())

        last_c = c
        _s += c

    return _s


# ---------------------------------------------------------------------------------------------------------------------------------------- #