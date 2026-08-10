# validation.py — Полная валидация по правилам классической римской нумерации

_VALUES = {'I': 1, 'V': 5, 'X': 10, 'L': 50,
           'C': 100, 'D': 500, 'M': 1000}

_VALID_CHARS = set('IVXLCDM')

_PAIRS = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100, 'C'),  (90, 'XC'), (50, 'L'),  (40, 'XL'),
    (10,  'X'),  (9,  'IX'), (5,  'V'),  (4,  'IV'),
    (1,   'I'),
]


def _raw_to_int(s: str) -> int | None:
    total, prev = 0, 0
    for ch in reversed(s):
        if ch not in _VALUES:
            return None
        curr = _VALUES[ch]
        total += curr if curr >= prev else -curr
        prev = curr
    return total


def _int_to_roman(n: int) -> str:
    result = ''
    for value, symbol in _PAIRS:
        while n >= value:
            result += symbol
            n -= value
    return result


def validate_roman(s: str) -> tuple[bool, str]:
    """
    Канонический метод: переводим строку в число, потом обратно в эталон
    и сравниваем. Любое нестандартное написание не совпадёт с эталоном.
    """
    if not s:
        return False, 'Введите число'
    upper = s.upper()
    for ch in upper:
        if ch not in _VALID_CHARS:
            return False, f"Недопустимый символ '{ch}'. Используйте I V X L C D M"
    value = _raw_to_int(upper)
    if value is None or value <= 0:
        return False, 'Некорректная запись римского числа'
    if value > 3999:
        return False, 'Число превышает 3999 — максимум римской системы'
    canonical = _int_to_roman(value)
    if upper != canonical:
        return False, f"Некорректная запись. Правильно: {canonical}"
    return True, ''


def validate_arabic(s: str) -> tuple[bool, str]:
    if not s:
        return False, 'Введите число'
    for ch in s:
        if not ch.isdigit():
            return False, 'Допустимы только цифры 0–9'
    if s.startswith('0') and len(s) > 1:
        return False, 'Число не может начинаться с нуля'
    n = int(s)
    if n == 0:
        return False, 'Минимальное значение: 1'
    if n > 3999:
        return False, 'Максимальное значение: 3999'
    return True, ''
