from pyrustic.app import App
from jupitest.misc.builder import MainViewBuilder
from jupitest.misc import my_theme


def main():
    app = App(__package__)
    app.root.title("Jupitest - Pyrustic Test Runner")
    app.theme = my_theme.get_theme()
    app.view = MainViewBuilder().build(app)
    app.center()
    app.start()

if __name__ == "__main__":
    main()
