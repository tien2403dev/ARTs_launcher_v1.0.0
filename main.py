import sys
from PyQt5.QtWidgets import QApplication

from ui.launcher_window import LauncherWindow
from controllers.launcher_controller import LauncherController


def main():
    app = QApplication(sys.argv)

    window = LauncherWindow()
    controller = LauncherController(window)

    controller.start()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()