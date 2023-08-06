# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

def multi_replace(s: str, keys_vals: dict) -> str:
    for k, v in keys_vals.items():
        v = v or ''

        s = s.replace(k, str(v))

    return s

def comment_line(text: str, line_len: int = 140) -> str:
    import math

    text = text.strip()
    pre, post = '# ', ' #'
    needeed_len = line_len - (len(text)+2) - len(pre) - len(post)

    pre_div_len = math.ceil(needeed_len/2)
    post_div_len = needeed_len - pre_div_len

    return '# {} {} {} #'.format(pre_div_len*'-', text, post_div_len*'-')


# ---------------------------------------------------------------------------------------------------------------------------------------- #