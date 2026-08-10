# main.py — Точка входа в программу

from gui import App


def main():
    """Запускает приложение «Конвертер римских чисел»."""
    app = App()
    app.run()


if __name__ == '__main__':
    main()
