# learning.py — Модуль режима обучения
import random
from converter import ar, rom

SUBTRACTION_PAIRS = ('IV', 'IX', 'XL', 'XC', 'CD', 'CM')
RULES = {
    'roman_to_arabic': [
        ("Базовые значения",
         "Каждому символу соответствует значение: I=1, V=5, X=10, L=50, C=100, D=500, M=1000."),
        ("Правило сложения",
         "Символы записываются от большего к меньшему — их значения складываются. "
         "Например: VI = 5+1 = 6, VIII = 5+1+1+1 = 8."),
        ("Правило вычитания",
         "Если меньший символ стоит ПЕРЕД большим — он вычитается. "
         "Допустимые пары: IV=4, IX=9, XL=40, XC=90, CD=400, CM=900."),
        ("Алгоритм чтения",
         "Идите по символам слева направо: если текущий символ меньше следующего — вычтите, иначе прибавьте."),
    ],
    'arabic_to_roman': [
        ("Принцип записи",
         "Число разбивается на тысячи, сотни, десятки и единицы; каждый разряд записывается своими символами."),
        ("Жадный алгоритм",
         "Последовательно вычитайте наибольшее возможное значение: "
         "1000→M, 900→CM, 500→D, 400→CD, 100→C, 90→XC, 50→L, 40→XL, 10→X, 9→IX, 5→V, 4→IV, 1→I."),
        ("Субтрактивные пары",
         "Запомните специальные обозначения: 4=IV, 9=IX, 40=XL, 90=XC, 400=CD, 900=CM. "
         "Нельзя писать IIII, VIIII, XXXX и т.д."),
    ],
}
TOTAL_QUESTIONS = 10
class LearningSession:
    def __init__(self):
        self._questions: list[dict] = []
        self._index: int = 0
        self._correct: int = 0
        self._answers: list[dict] = []
        self._active: bool = False

    def start_test(self) -> None:
        self._questions = [self._generate_question() for _ in range(TOTAL_QUESTIONS)]
        self._index = 0
        self._correct = 0
        self._answers = []
        self._active = True

    def _generate_question(self) -> dict:
        q_type = random.randint(1, 2)
        number = random.randint(1, 3999)
        roman = rom(str(number))['result']
        if q_type == 1:
            return {'question': roman, 'answer': str(number), 'type': 1}
        else:
            return {'question': str(number), 'answer': roman, 'type': 2}

    def nextq(self) -> dict | None:
        if self._index >= len(self._questions):
            return None
        return self._questions[self._index]

    def che(self, user_answer: str) -> dict:
        if self._index >= len(self._questions):
            return {'correct': False, 'explanation': 'Тест завершён.', 'rule_used': None}

        q = self._questions[self._index]
        correct_answer = q['answer']
        q_type = q['type']
        ua = user_answer.strip().upper()
        ca = correct_answer.strip().upper()
        is_correct = (ua == ca)

        if is_correct:
            self._correct += 1
            explanation = f"Верно! {q['question']} = {correct_answer}"
            rule_used = None
        else:
            explanation = (
                f"Неверно. Ваш ответ: {user_answer}. "
                f"Правильный ответ: {correct_answer}."
            )
            rule_used = self._explain_rule(q)

        self._answers.append({
            'question': q['question'],
            'user': user_answer,
            'correct': correct_answer,
            'is_correct': is_correct,
            'type': q_type,
        })
        self._index += 1

        return {
            'correct': is_correct,
            'correct_answer': correct_answer,
            'explanation': explanation,
            'rule_used': rule_used,
        }

    def _explain_rule(self, question: dict) -> str:
        q_type = question['type']
        answer = question['answer']
        if q_type == 1:
            roman = question['question']
            rules = RULES['roman_to_arabic']
            has_sub = any(
                roman[i:i+2] in SUBTRACTION_PAIRS
                for i in range(len(roman) - 1)
            )
            if has_sub:
                rule = rules[2] 
            elif len(roman) > 1:
                rule = rules[1] 
            else:
                rule = rules[0]
            breakdown = self._breakdown_roman(roman)
            return (
                f"Применяемое правило — «{rule[0]}»:\n"
                f"{rule[1]}\n"
                f"Разбор: {breakdown} = {answer}"
            )
        else:
            arabic = int(question['question'])
            rules = RULES['arabic_to_roman']
            d1 = arabic % 10          
            d10 = (arabic // 10) % 10  
            d100 = (arabic // 100) % 10  
            has_sub = (
                d1 in (4, 9) or
                d10 in (4, 9) or
                d100 in (4, 9)
            )
            rule = rules[2] if has_sub else rules[1]
            breakdown = self._breakdown_arabic(arabic)
            return (
                f"Применяемое правило — «{rule[0]}»:\n"
                f"{rule[1]}\n"
                f"Разбор: {breakdown} = {answer}"
            )

    def _breakdown_roman(self, roman: str) -> str:
        """
        Пошаговый разбор слева направо (как читает человек).
        Каждый символ помечается знаком + или −.
        """
        VALUES = {'I': 1, 'V': 5, 'X': 10, 'L': 50,
                  'C': 100, 'D': 500, 'M': 1000}
        s = roman.upper()
        steps = []
        for i, ch in enumerate(s):
            curr = VALUES[ch]
            if i + 1 < len(s) and VALUES[s[i + 1]] > curr:
                steps.append(f"−{curr}({ch})")
            else:
                steps.append(f"+{curr}({ch})")
        # Убираем ведущий '+' для красоты
        expr = ' '.join(steps)
        if expr.startswith('+'):
            expr = expr[1:]
        return expr

    def _breakdown_arabic(self, n: int) -> str:
        """Пошаговый разбор жадного алгоритма."""
        PAIRS = [
            (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
            (100, 'C'),  (90, 'XC'), (50, 'L'),  (40, 'XL'),
            (10,  'X'),  (9,  'IX'), (5,  'V'),  (4,  'IV'),
            (1,   'I'),
        ]
        steps = []
        remaining = n
        for value, symbol in PAIRS:
            while remaining >= value:
                steps.append(f"{remaining}−{value}({symbol})")
                remaining -= value
        return ' → '.join(steps)

    def testrez(self) -> dict:
        total = len(self._answers)
        correct = self._correct
        percent = round(correct / total * 100) if total > 0 else 0
        if percent >= 80:
            grade = 5
        elif percent >= 60:
            grade = 4
        elif percent >= 40:
            grade = 3
        else:
            grade = 2
        return {
            'correct': correct,
            'total': total,
            'percent': percent,
            'grade': grade,
            'answers': self._answers,
        }

    @property
    def current_index(self) -> int:
        return self._index

    @property
    def is_active(self) -> bool:
        return self._active
_session = LearningSession()

def start_test() -> None:
    _session.start_test()


def nextq() -> dict | None:
    return _session.nextq()


def che(user_answer: str) -> dict:
    return _session.che(user_answer)


def testrez() -> dict:
    return _session.testrez()


def current_index() -> int:
    return _session.current_index
