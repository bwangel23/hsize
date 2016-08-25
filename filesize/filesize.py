
import re

(DIGIT, UNIT, SPACE) = tuple(range(3))
(STATE0, STATE1, STATE2, STATE3) = tuple(range(4))

traditional = {
    "B": 1,
    "K": 1024,
    "M": 1024 ** 2,
    "G": 1024 ** 3,
    "T": 1024 ** 4,
    "P": 1024 ** 5,
    "E": 1024 ** 6,
    "Z": 1024 ** 7,
}

si = {
    "B": 1,
    "K": 1000,
    "M": 1000 ** 2,
    "G": 1000 ** 3,
    "T": 1000 ** 4,
    "P": 1000 ** 5,
    "E": 1000 ** 6,
    "Z": 1000 ** 7,
}


def from_human_readable(size, system=traditional, default_unit='M'):
    """Convert human readable size to the bytes
    `size`: the human readable size
    `default_unit`: the default unit when there is no unit after the `size`

    Using the traditional system, where a factor of 1024 is used::

    >>> from_human_readable('35B')
    35
    >>> from_human_readable('35 mB')
    36700160
    >>> from_human_readable('35 GB')
    37580963840
    >>> from_human_readable('35 TB')
    38482906972160
    >>> from_human_readable('35 pb')
    39406496739491840
    >>> from_human_readable('35 eb')
    40352252661239644160
    >>> from_human_readable('35 zb')
    41320706725109395619840
    >>> from_human_readable('  35 ')
    36700160

    Using the SI system, with a factor 1000
    >>> from_human_readable('35B', system=si)
    35
    >>> from_human_readable('35 mB', system=si)
    35000000
    >>> from_human_readable('35 GB', system=si)
    35000000000
    >>> from_human_readable('35 TB', system=si)
    35000000000000
    >>> from_human_readable('35 pb', system=si)
    35000000000000000
    >>> from_human_readable('35 eb', system=si)
    35000000000000000000
    >>> from_human_readable('35 zb', system=si)
    35000000000000000000000
    >>> from_human_readable('  35 ', system=si)
    35000000
    """
    size = size.upper()
    trans_table = [
        #digit, unit, space
        [1, -1, 0],  # State0
        [1, 3, 2],   # State1
        [-1, 3, 2],  # State2
        [-1, -1, 3], # State3
    ]
    digit = ""

    state = STATE0
    it = enumerate(size)
    for i,c in it:
        if re.match(r"[0-9]", c):
            input_type = DIGIT
            digit += c
            state = trans_table[state][input_type]
        elif re.match(r"[BKMGTPEZ]", c):
            input_type = UNIT
            unit = c
            state = trans_table[state][input_type]
            if c == 'B':
                continue
            try:
                if size[i + 1] == 'B':
                    next(it)
            except IndexError:
                pass
            except:
                raise
        elif c == ' ':
            input_type = SPACE
            state = trans_table[state][input_type]
        else:
            state = -1

        if state == -1:
            break

    if state == 1 or state == 2:
        # 必须输入了UNIT才能够到达State3, 如果没到状态3，那么unit一定是默认的
        if not 'unit' in locals():
            unit = default_unit
        _bytes = int(digit) * system[unit]
    elif state == 3:
        _bytes = int(digit) * system[unit]
    elif state == -1:
        raise ValueError("size has wrong format: %s" % size)

    return _bytes

def to_human_readable():
    pass
