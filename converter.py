# converter.py - Модуль конвертации чисел

from validation import validate_roman, validate_arabic

_PAIRS = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100, 'C'),  (90, 'XC'), (50, 'L'),  (40, 'XL'),
    (10, 'X'),   (9, 'IX'),  (5, 'V'),   (4, 'IV'),
    (1, 'I'),
]
_VALUES = {'I': 1, 'V': 5, 'X': 10, 'L': 50,
           'C': 100, 'D': 500, 'M': 1000}

def ar(roman_str: str) -> dict:
    """
    Конвертирует римское число в арабское.
    Возвращает словарь с ключами 'result' (int|None) и 'error' (str|None).
    """
    ok, msg = validate_roman(roman_str)
    if not ok:
        return {'result': None, 'error': msg}
    s = roman_str.upper()
    total = 0
    prev = 0
    for ch in reversed(s):
        curr = _VALUES[ch]
        if curr < prev:
            total -= curr
        else:
            total += curr
        prev = curr
    return {'result': total, 'error': None}


def rom(arabic_str: str) -> dict:
    """
    Конвертирует арабское число в римское.
    Возвращает словарь с ключами 'result' (str|None) и 'error' (str|None).
    """
    ok, msg = validate_arabic(arabic_str)
    if not ok:
        return {'result': None, 'error': msg}
    n = int(arabic_str)
    result = ''
    for value, symbol in _PAIRS:
        while n >= value:
            result += symbol
            n -= value
    return {'result': result, 'error': None}
