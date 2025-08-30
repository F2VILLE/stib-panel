from stib import STIB, Line
from datetime import datetime
from time import sleep
import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide6.QtCore import QObject, QTimer, Signal, Property
import os
# clear = "\033[H\033[J"

BUS_STOP = os.getenv("BUS_STOP")

class BusDataProvider(QObject):
    busDataChanged = Signal()
    
    def __init__(self):
        super().__init__()
        self.stib = STIB(BUS_STOP)
        self._bus_data = []
        self.last_update = ""
        self.updateBusData()
    
    @Property(list, notify=busDataChanged)
    def busData(self):
        return self._bus_data

    def updateBusData(self):
        try:
            next_lines = self.stib.next_lines
            print("Fetched", len(next_lines), "lines")
            self._bus_data = [
                {"line": l.id, "destination": l.destination, "waiting": l.time_left()} 
                for l in next_lines
            ]
            self.last_update = datetime.now().astimezone().strftime("%H:%M:%S")
            self.busDataChanged.emit()
            print("Updated bus lines at", self.last_update)
        except Exception as e:
            print(f"Error updating bus data: {e}")

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    
    bus_provider = BusDataProvider()
    qmlRegisterType(BusDataProvider, "BusData", 1, 0, "BusDataProvider")

    engine = QQmlApplicationEngine()
    engine.addImportPath(sys.path[0])
    engine.rootContext().setContextProperty("busProvider", bus_provider)
    engine.rootContext().setContextProperty("busLastUpdate", bus_provider.last_update)
    engine.rootContext().setContextProperty("busStopName", BUS_STOP if BUS_STOP else "ULB")
    engine.loadFromModule("views", "main")
    
    timer = QTimer()
    timer.timeout.connect(bus_provider.updateBusData)
    timer.start(10000) 
    if not engine.rootObjects():
        sys.exit(-1)
    exit_code = app.exec()
    del engine
    sys.exit(exit_code)