from stib import STIB, Line, API, Dataset
from datetime import datetime
from time import sleep
import sys
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide6.QtCore import QObject, QTimer, Signal, Property
import os


BUS_STOP = os.getenv("BUS_STOP")

icons = {}

icons['Bus'] = "./icons/Bus.svg"
icons['Tramway'] = "./icons/Tramway.svg"
icons['Metro'] = "./icons/Metro.svg"


class BusDataProvider(QObject):
    busDataChanged = Signal()
    
    def __init__(self):
        super().__init__()
        self.error = ""
        self.stib = None
        try:
            self.stib = STIB(BUS_STOP)
        except Exception as e:
            self.error = f"Error: {e}"
        self._bus_data = []
        self.lineColors = {}
        self.lineTypes = {}
        self.last_update = datetime.now().astimezone().strftime("%H:%M:%S")
        self.updateBusData()
    
    @Property(list, notify=busDataChanged)
    def busData(self):
        return self._bus_data

    def updateBusData(self):
        try:
            if not self.stib:
                try:
                    self.stib = STIB(BUS_STOP)
                except Exception as e:
                    self.error = f"Error: {e}"
                return
            next_lines = self.stib.next_lines
            print("Fetched", len(next_lines), "lines")
            self._bus_data = [
                {"line": l.id, "destination": l.destination, "waiting": l.time_left(), "color": l.color, "type": l.type}
                for l in next_lines
            ]
            self.last_update = datetime.now().astimezone().strftime("%H:%M:%S")
            self.busDataChanged.emit()
            print("Updated bus lines at", self.last_update)
        except Exception as e:
            print(f"Error updating bus data: {e}")
            self.error = f"Error: {e}"

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    
    bus_provider = BusDataProvider()
    qmlRegisterType(BusDataProvider, "BusData", 1, 0, "BusDataProvider")

    engine = QQmlApplicationEngine()
    engine.addImportPath(sys.path[0])
    engine.rootContext().setContextProperty("busProvider", bus_provider)
    engine.rootContext().setContextProperty("busError", bus_provider.error)
    engine.rootContext().setContextProperty("busLastUpdate", bus_provider.last_update)
    # engine.rootContext().setContextProperty("busLineColors", bus_provider.lineColors)
    engine.rootContext().setContextProperty("lineTypeIcons", icons)
    engine.rootContext().setContextProperty("busStopName", BUS_STOP if BUS_STOP else "ULB")
    engine.loadFromModule("views", "main")
    
    timer = QTimer()
    timer.timeout.connect(bus_provider.updateBusData)
    timer.start(30000) 
    if not engine.rootObjects():
        sys.exit(-1)
    exit_code = app.exec()
    del engine
    sys.exit(exit_code)