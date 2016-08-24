#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

(DIGIT, UNIT, SPACE) = tuple(range(3))
(STATE0, STATE1, STATE2, STATE3) = tuple(range(4))


def from_human_readable(size, unit='M'):
    """
    """
    size = size.upper()
    trans_table = [
        #digit, unit, space
        [1, -1, 0],  # State0
        [1, 3, 2],   # State1
        [-1, 3, 2],  # State2
        [-1, -1, 3], # State3
    ]
    unit_conversion = {
        "K": 1024,
        "M": 1024 ** 2,
        "G": 1024 ** 3,
        "T": 1024 ** 4,
        "P": 1024 ** 5,
        "E": 1024 ** 6,
        "Z": 1024 ** 7,
    }
    digit = ""

    state = STATE0
    it = enumerate(size)
    for i,c in it:
        if re.match(r"[0-9]", c):
            input_type = DIGIT
            digit += c
            state = trans_table[state][input_type]
        elif re.match(r"[KMGTPEZ]", c):
            if size[i + 1] == 'B':
                next(it)
            input_type = UNIT
            unit = c
            state = trans_table[state][input_type]
        elif c == ' ':
            input_type = SPACE
            state = trans_table[state][input_type]
        else:
            state = -1

        if state == -1:
            break

    if state == 1 or state == 2:
        # 必须输入了UNIT才能够到达State3, 如果没到状态3，那么unit一定是默认的
        _bytes = int(digit) * unit_conversion[unit]
        print(digit, unit, _bytes)
    elif state == 3:
        _bytes = int(digit) * unit_conversion[unit]
        print(digit, unit, _bytes)
    elif state == -1:
        print("Error")

def to_human_readable():
    pass


if __name__ == '__main__':
    from_human_readable('35MB')
    from_human_readable('35 MB')
    from_human_readable('  35  ')
    from_human_readable('   35 MB   ')
    from_human_readable('  MB 35    ')
