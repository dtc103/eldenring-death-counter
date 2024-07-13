from DeathCounter import DeathCounter
from Overlay import *


PROCESS_NAME = "eldenring.exe"
WINDOW_NAME = "elden ring"
MONITOR_IDX = 1


def main():
    dc = DeathCounter(PROCESS_NAME, WINDOW_NAME, MONITOR_IDX, 10)
    dc.start()

    app = QtWidgets.QApplication(sys.argv)
    win = TransparentWindow(dc.found_event, dc.stop_event)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
