from DeathCounter import DeathCounter
from Overlay import *
from multiprocessing import Event

PROCESS_NAME = "eldenring.exe"
WINDOW_NAME = "elden ring"

def main():
    dc = DeathCounter(PROCESS_NAME, WINDOW_NAME, 10)

    app = QtWidgets.QApplication(sys.argv)
    win = TransparentWindow(dc.found_event, dc.stop_event)
    win.show()
    sys.exit(app.exec_())

    
if __name__ == "__main__":
    main()
