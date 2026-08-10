# gui.py — Графический интерфейс. Светлая тема, минималистичный дизайн.

import tkinter as tk
from tkinter import messagebox, font as tkfont
import time
import converter
import learning
BG        = '#F5F0E8'
BG_PANEL  = '#EDE8DF'
BG_ENTRY  = '#FFFFFF'
BG_BTN    = '#5C6BC0'
BG_BTN2   = '#78909C'
BG_OK     = '#558B6E'
BG_ERR    = '#B85450'
BG_WARN   = '#C97B2A'
FG_MAIN   = '#2C2C2C'
FG_SUB    = '#6B6B6B'
FG_WHITE  = '#FFFFFF'
BORDER    = '#C8C0B4'
ACCENT    = '#5C6BC0'
FONT      = 'Georgia'
FONT_MONO = 'Courier New'
FONT_UI   = 'Segoe UI'

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Конвертер римских чисел')
        self.root.geometry('780x560')
        self.root.configure(bg=BG)
        self.root.resizable(True, True)
        self.root.minsize(680, 500)
        self._timer_job = None
        self._t0 = 0.0
        self._build_header()
        self._build_nav()
        self._build_status()
        self.content = tk.Frame(self.root, bg=BG)
        self.content.pack(fill='both', expand=True, padx=24, pady=(0, 8))
        self.show_converter()


    def _btn(self, parent, text, cmd, bg=None, fg=FG_WHITE, **kw):
        bg = bg or BG_BTN
        b = tk.Button(parent, text=text, command=cmd,
                      bg=bg, fg=fg, activebackground=bg, activeforeground=fg,
                      font=(FONT_UI, 10), relief='flat', bd=0,
                      padx=14, pady=6, cursor='hand2', **kw)
        b.bind('<Enter>', lambda e: b.configure(bg=self._lighten(bg)))
        b.bind('<Leave>', lambda e: b.configure(bg=bg))
        return b

    @staticmethod
    def _lighten(hex_color):
        """Делает цвет немного светлее для hover-эффекта."""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        r = min(255, r + 22)
        g = min(255, g + 22)
        b = min(255, b + 22)
        return f'#{r:02x}{g:02x}{b:02x}'

    def _entry(self, parent, width=26, font_size=14):
        e = tk.Entry(parent, bg=BG_ENTRY, fg=FG_MAIN,
                     font=(FONT_MONO, font_size),
                     insertbackground=ACCENT,
                     relief='flat', bd=0, width=width,
                     highlightthickness=1,
                     highlightbackground=BORDER,
                     highlightcolor=ACCENT)
        return e

    def _label(self, parent, text, size=11, bold=False, color=None, **kw):
        return tk.Label(parent, text=text,
                        bg=kw.pop('bg', BG), fg=color or FG_MAIN,
                        font=(FONT_UI, size, 'bold' if bold else 'normal'),
                        **kw)

    def _sep(self, parent):
        return tk.Frame(parent, bg=BORDER, height=1)


    def _build_header(self):
        h = tk.Frame(self.root, bg=ACCENT, pady=10)
        h.pack(fill='x')
        tk.Label(h, text='Конвертер римских чисел',
                 font=(FONT, 17, 'bold'), bg=ACCENT, fg=FG_WHITE).pack()
        tk.Label(h, text='перевод · обучение · проверка',
                 font=(FONT_UI, 9), bg=ACCENT, fg='#C5CAE9').pack()

    def _build_nav(self):
        nav = tk.Frame(self.root, bg=BG_PANEL, pady=6)
        nav.pack(fill='x')
        inner = tk.Frame(nav, bg=BG_PANEL)
        inner.pack()
        self._btn(inner, '⇄  Конвертация', self.show_converter,
                  bg=BG_BTN).pack(side='left', padx=6)
        self._btn(inner, '✎  Обучение', self.show_learning,
                  bg=BG_BTN2).pack(side='left', padx=6)
        self._sep(self.root).pack(fill='x')

    def _build_status(self):
        self._status_var = tk.StringVar(value='Выберите режим')
        bar = tk.Label(self.root, textvariable=self._status_var,
                       bg=BG_PANEL, fg=FG_SUB,
                       font=(FONT_UI, 9), anchor='w', padx=12, pady=3)
        bar.pack(fill='x', side='bottom')
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill='x', side='bottom')

    def _set_status(self, text):
        self._status_var.set(text)

    def _clear(self):
        for w in self.content.winfo_children():
            w.destroy()
        if self._timer_job:
            self.root.after_cancel(self._timer_job)
            self._timer_job = None

    def show_converter(self):
        self._clear()
        self._set_status('Режим конвертации')
        wrap = tk.Frame(self.content, bg=BG)
        wrap.pack(fill='both', expand=True, pady=12)
        self._block_title(wrap, 'Римское  →  Арабское')
        row1 = tk.Frame(wrap, bg=BG)
        row1.pack(fill='x', pady=(4, 0))
        self._re = self._entry(row1, width=24)
        self._re.pack(side='left', ipady=5, padx=(0, 8))
        self._re.bind('<Return>', lambda e: self._do_r2a())
        self._btn(row1, 'Перевести', self._do_r2a).pack(side='left')
        self._r_res = tk.Label(wrap, text='', font=(FONT_MONO, 20, 'bold'),
                               bg=BG, fg=BG_OK, anchor='w')
        self._r_res.pack(fill='x', pady=(4, 0))
        self._sep(wrap).pack(fill='x', pady=14)

        self._block_title(wrap, 'Арабское  →  Римское')
        row2 = tk.Frame(wrap, bg=BG)
        row2.pack(fill='x', pady=(4, 0))
        self._ae = self._entry(row2, width=24)
        self._ae.pack(side='left', ipady=5, padx=(0, 8))
        self._ae.bind('<Return>', lambda e: self._do_a2r())
        self._btn(row2, 'Перевести', self._do_a2r).pack(side='left')
        self._a_res = tk.Label(wrap, text='', font=(FONT_MONO, 20, 'bold'),
                               bg=BG, fg=BG_OK, anchor='w')
        self._a_res.pack(fill='x', pady=(4, 0))
        self._err_lbl = tk.Label(wrap, text='', font=(FONT_UI, 10),
                                 bg=BG, fg=BG_ERR, anchor='w', wraplength=600,
                                 justify='left')
        self._err_lbl.pack(fill='x', pady=(6, 0))

        self._sep(wrap).pack(fill='x', pady=14)
        hint = tk.Frame(wrap, bg=BG_PANEL, padx=14, pady=10,
                        highlightthickness=1, highlightbackground=BORDER)
        hint.pack(fill='x')
        tk.Label(hint, text='Допустимые символы: I V X L C D M  ·  Диапазон: 1 – 3999',
                 font=(FONT_UI, 9), bg=BG_PANEL, fg=FG_SUB).pack(anchor='w')
        tk.Label(hint,
                 text='Субтрактивные пары: IV=4  IX=9  XL=40  XC=90  CD=400  CM=900',
                 font=(FONT_MONO, 9), bg=BG_PANEL, fg=FG_SUB).pack(anchor='w', pady=(2, 0))

    def _block_title(self, parent, text):
        tk.Label(parent, text=text, font=(FONT_UI, 11, 'bold'),
                 bg=BG, fg=ACCENT, anchor='w').pack(fill='x')

    def _do_r2a(self):
        s = self._re.get().strip()
        res = converter.ar(s)
        self._err_lbl.config(text='')
        if res['error']:
            self._r_res.config(text='')
            self._err_lbl.config(text=f'Ошибка: {res["error"]}')
            self._set_status(f'Ошибка: {res["error"]}')
        else:
            self._r_res.config(text=f'= {res["result"]}')
            self._set_status(f'{s.upper()} = {res["result"]}')

    def _do_a2r(self):
        s = self._ae.get().strip()
        res = converter.rom(s)
        self._err_lbl.config(text='')
        if res['error']:
            self._a_res.config(text='')
            self._err_lbl.config(text=f'Ошибка: {res["error"]}')
            self._set_status(f'Ошибка: {res["error"]}')
        else:
            self._a_res.config(text=f'= {res["result"]}')
            self._set_status(f'{s} = {res["result"]}')


    def show_learning(self):
        self._clear()
        self._set_status('Режим обучения')
        ctrl = tk.Frame(self.content, bg=BG, pady=8)
        ctrl.pack(fill='x')
        self._btn(ctrl, '▶  Начать тест', self._start_test, bg=BG_OK).pack(side='left', padx=(0, 8))
        self._btn(ctrl, '?  Правила', self._show_rules, bg=BG_BTN2).pack(side='left')
        self._timer_lbl = tk.Label(ctrl, text='', font=(FONT_UI, 10),
                                   bg=BG, fg=FG_SUB)
        self._timer_lbl.pack(side='right')
        self._stat_lbl = tk.Label(ctrl, text='', font=(FONT_UI, 10, 'bold'),
                                  bg=BG, fg=FG_MAIN)
        self._stat_lbl.pack(side='right', padx=12)
        self._sep(self.content).pack(fill='x')
        self._learn_area = tk.Frame(self.content, bg=BG)
        self._learn_area.pack(fill='both', expand=True, pady=10)

        self._show_welcome()

    def _show_welcome(self):
        self._clear_area()
        frame = tk.Frame(self._learn_area, bg=BG_PANEL,
                         padx=28, pady=28,
                         highlightthickness=1, highlightbackground=BORDER)
        frame.pack(expand=True, fill='both')
        tk.Label(frame, text='Тест по переводу римских чисел',
                 font=(FONT, 14, 'bold'), bg=BG_PANEL, fg=FG_MAIN).pack(pady=(0, 8))
        tk.Label(frame,
                 text=(
                     '10 случайных вопросов двух типов:\n'
                     '  · перевести римское число в арабское\n'
                     '  · перевести арабское число в римское\n\n'
                     'При неверном ответе программа покажет\n'
                     'правильный ответ и объяснит правило перевода.'
                 ),
                 font=(FONT_UI, 11), bg=BG_PANEL, fg=FG_SUB,
                 justify='left').pack(anchor='w')

    def _clear_area(self):
        for w in self._learn_area.winfo_children():
            w.destroy()

    def _start_test(self):
        learning.start_test()
        self._t0 = time.time()
        self._tick()
        self._show_question()

    def _tick(self):
        elapsed = int(time.time() - self._t0)
        m, s = divmod(elapsed, 60)
        self._timer_lbl.config(text=f'⏱ {m:02d}:{s:02d}')
        self._timer_job = self.root.after(1000, self._tick)

    def _show_question(self):
        self._clear_area()

        q = learning.nextq()
        if q is None:
            self._show_results()
            return
        idx = learning.current_index()
        correct_so_far = learning._session._correct
        self._stat_lbl.config(text=f'Вопрос {idx + 1} / 10  |  ✓ {correct_so_far}')
        frame = tk.Frame(self._learn_area, bg=BG_PANEL,
                         padx=24, pady=20,
                         highlightthickness=1, highlightbackground=BORDER)
        frame.pack(fill='both', expand=True)
        prompt = ('Переведите римское число в арабское:'
                  if q['type'] == 1
                  else 'Переведите арабское число в римское:')
        tk.Label(frame, text=prompt, font=(FONT_UI, 11),
                 bg=BG_PANEL, fg=FG_SUB).pack(anchor='w')
        tk.Label(frame, text=q['question'],
                 font=(FONT, 36, 'bold'), bg=BG_PANEL, fg=ACCENT).pack(pady=12)
        self._ans_entry = self._entry(frame, width=20, font_size=15)
        self._ans_entry.pack(ipady=7, pady=(0, 10))
        self._ans_entry.focus_set()
        self._ans_entry.bind('<Return>', lambda e: self._check())
        btn_row = tk.Frame(frame, bg=BG_PANEL)
        btn_row.pack()
        self._btn(btn_row, '✔  Проверить', self._check, bg=BG_OK).pack(side='left', padx=4)
        self._btn(btn_row, '→  Пропустить', self._skip, bg=BG_BTN2).pack(side='left', padx=4)
        self._fb = tk.Label(frame, text='', font=(FONT_UI, 10),
                            bg=BG_PANEL, fg=FG_MAIN,
                            wraplength=680, justify='left')
        self._fb.pack(pady=(14, 0), anchor='w')

    def _check(self):
        ans = self._ans_entry.get().strip()
        if not ans:
            messagebox.showwarning('Внимание', 'Введите ответ или нажмите «Пропустить».')
            return
        res = learning.che(ans)
        if res['correct']:
            self._fb.config(
                text=f'✓  {res["explanation"]}',
                fg=BG_OK
            )
        else:
            rule = f'\n\n{res["rule_used"]}' if res.get('rule_used') else ''
            self._fb.config(
                text=f'✗  {res["explanation"]}{rule}',
                fg=BG_ERR
            )
        self.root.after(5000, self._show_question)

    def _skip(self):
        q = learning.nextq()
        correct = q['answer'] if q else '—'
        learning.che('__SKIP__')
        self._fb.config(
            text=f'Пропущено. Правильный ответ: {correct}',
            fg=BG_WARN
        )
        self.root.after(3000, self._show_question)

    def _show_results(self):
        if self._timer_job:
            self.root.after_cancel(self._timer_job)
            self._timer_job = None
        res = learning.testrez()
        elapsed = int(time.time() - self._t0)
        m, s = divmod(elapsed, 60)
        self._clear_area()

        frame = tk.Frame(self._learn_area, bg=BG_PANEL,
                         padx=28, pady=22,
                         highlightthickness=1, highlightbackground=BORDER)
        frame.pack(fill='both', expand=True)
        grade_color = {5: BG_OK, 4: '#4A8C6F', 3: BG_WARN, 2: BG_ERR}[res['grade']]
        grade_lbl = {5: 'Отлично', 4: 'Хорошо', 3: 'Удовлетворительно', 2: 'Неудовлетворительно'}[res['grade']]
        tk.Label(frame, text='Результаты теста',
                 font=(FONT, 15, 'bold'), bg=BG_PANEL, fg=FG_MAIN).pack(pady=(0, 14))
        grid = tk.Frame(frame, bg=BG_PANEL)
        grid.pack()

        def row(label, value, color=FG_MAIN):
            r = tk.Frame(grid, bg=BG_PANEL)
            r.pack(fill='x', pady=2)
            tk.Label(r, text=f'{label}:', font=(FONT_UI, 11),
                     bg=BG_PANEL, fg=FG_SUB, width=22, anchor='e').pack(side='left')
            tk.Label(r, text=value, font=(FONT_UI, 11, 'bold'),
                     bg=BG_PANEL, fg=color).pack(side='left', padx=8)

        row('Правильных ответов', f'{res["correct"]} из {res["total"]}')
        row('Процент выполнения', f'{res["percent"]}%')
        row('Оценка', f'{res["grade"]} — {grade_lbl}', grade_color)
        row('Время', f'{m:02d}:{s:02d}')
        btn_row = tk.Frame(frame, bg=BG_PANEL)
        btn_row.pack(pady=16)
        self._btn(btn_row, 'Пройти ещё раз', self._start_test, bg=BG_BTN).pack(side='left', padx=6)
        self._btn(btn_row, 'Подробная статистика', self._show_detail, bg=BG_BTN2).pack(side='left', padx=6)
        self._stat_lbl.config(text=f'✓ {res["correct"]} / {res["total"]}')

    def _show_detail(self):
        res = learning.testrez()
        win = tk.Toplevel(self.root)
        win.title('Подробная статистика')
        win.configure(bg=BG)
        win.geometry('600x420')
        tk.Label(win, text='Разбор вопросов',
                 font=(FONT, 13, 'bold'), bg=BG, fg=FG_MAIN).pack(pady=10)
        txt = tk.Text(win, bg=BG_ENTRY, fg=FG_MAIN,
                      font=(FONT_MONO, 10), relief='flat',
                      padx=10, pady=8, wrap='word',
                      highlightthickness=1, highlightbackground=BORDER)
        txt.pack(fill='both', expand=True, padx=12, pady=(0, 12))
        for i, a in enumerate(res['answers'], 1):
            mark = '✓' if a['is_correct'] else '✗'
            txt.insert('end',
                       f'{i:2}. {mark}  Вопрос: {a["question"]:10}  '
                       f'Ваш ответ: {a["user"]:12}  '
                       f'Правильно: {a["correct"]}\n')
        txt.config(state='disabled')

    def _show_rules(self):
        TEXT = (
            'ПРАВИЛА ЗАПИСИ РИМСКИХ ЧИСЕЛ\n'
            '══════════════════════════════════════\n\n'
            'СИМВОЛЫ И ЗНАЧЕНИЯ:\n'
            '  I = 1    V = 5    X = 10    L = 50\n'
            '  C = 100  D = 500  M = 1000\n\n'
            'ПРАВИЛО СЛОЖЕНИЯ:\n'
            '  Если каждый следующий символ ≤ предыдущего — значения складываются.\n'
            '  Пример: VIII = 5+1+1+1 = 8\n\n'
            'ПРАВИЛО ВЫЧИТАНИЯ:\n'
            '  Если меньший символ стоит ПЕРЕД большим — он вычитается.\n'
            '  Допустимые субтрактивные пары:\n'
            '    IV = 4    IX = 9\n'
            '    XL = 40   XC = 90\n'
            '    CD = 400  CM = 900\n\n'
            'ОГРАНИЧЕНИЯ:\n'
            '  · I, X, C, M — не более 3 раз подряд\n'
            '  · V, L, D — никогда не повторяются\n'
            '  · Вычитать можно только одну степень: нельзя IL, IC, IM\n'
            '  · Диапазон: 1 – 3999\n\n'
            'КАК ЧИТАТЬ ЧИСЛО — СПРАВА НАЛЕВО:\n'
            '  Если текущий символ < предыдущего → вычти, иначе → прибавь.\n'
            '  Пример: MCMXCIX\n'
            '    X(10) − I(1) + C(100) − X(10) + M(1000) − C(100) + M(1000)\n'
            '    = 9 + 90 + 900 + 1000 = 1999\n'
        )
        win = tk.Toplevel(self.root)
        win.title('Правила перевода')
        win.configure(bg=BG)
        win.geometry('520x500')
        tk.Label(win, text='Справочник', font=(FONT, 13, 'bold'),
                 bg=BG, fg=FG_MAIN).pack(pady=10)
        txt = tk.Text(win, bg=BG_ENTRY, fg=FG_MAIN,
                      font=(FONT_MONO, 10), relief='flat',
                      padx=14, pady=10, wrap='word',
                      highlightthickness=1, highlightbackground=BORDER)
        txt.pack(fill='both', expand=True, padx=12, pady=(0, 12))
        txt.insert('end', TEXT)
        txt.config(state='disabled')

    def run(self):
        self.root.mainloop()
