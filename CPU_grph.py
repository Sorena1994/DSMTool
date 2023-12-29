#This code creates a widget consisted of CPU usage graph alongside with a table showing different CPU values. 
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
)
from PyQt6.QtCore import QTimer, QThread, pyqtSignal
from calc_cpu_params import cpu_TableWidget
import pyqtgraph as pg
import psutil
import sys


class WorkerThread(QThread):
    update_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def run(self):
        cpu_usage_data = [psutil.cpu_percent(interval=0.10) for _ in range(11)]
        self.update_signal.emit(cpu_usage_data)
        self.msleep(20)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("CPU Usage Graph")

        # setting geometry
        self.setGeometry(100, 100, 600, 500)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

    def UiComponents(self):
        # creating a widget object
        widget = QWidget()

        self.plot_graph = pg.PlotWidget()
        self.tableWidget = cpu_TableWidget()
        # Creating a grid layout
        layout = QVBoxLayout()

        # setting this layout to the widget
        widget.setLayout(layout)

        # button goes in the upper-left
        layout.addWidget(self.plot_graph)
        layout.addWidget(self.tableWidget)

        # setting this widget as the central widget of the main window
        self.setCentralWidget(widget)

        self.worker_thread = WorkerThread()
        self.worker_thread.update_signal.connect(self.receive_data)
        self.worker_thread.start()
        self.plot_cpu_graph() 

    def plot_cpu_graph(self): 
        self.plot_graph.setBackground("w")
        self.pen = pg.mkPen(color=(15, 82, 186))
        self.time = list(range(11))
        #self.cpu_usage = [0] * 11  # Initial placeholder data
        self.cpu_usage = [psutil.cpu_percent(interval=0.10) for _ in range(11)]

        self.plot_graph.setTitle("CPU Usage", color="b", size="20pt")
        styles = {"color": "red", "font-size": "18px"}
        self.plot_graph.setLabel("left", "CPU Usage (%)", **styles)
        self.plot_graph.addLegend()
        self.plot_graph.showGrid(x=True, y=True)
        self.plot_graph.setYRange(0, 100)

        # Get a line reference
        self.line = self.plot_graph.plot(
            self.time,
            self.cpu_usage,
            name="CPU Usage",
            pen=self.pen,
            symbol="+",
            symbolSize=15,
            symbolBrush="b",
        )
        # Disable mouse interaction on the plot
        self.plot_graph.setMouseEnabled(x=False, y=False)
        
        # Disable panning and zooming
        self.plot_graph.getAxis("bottom").setStyle(showValues=False)

        # Start the thread to update initial data
        self.worker_thread = WorkerThread()
        self.worker_thread.update_signal.connect(self.receive_data)
        self.worker_thread.start()

        # Add a timer to continue updating the plot
        self.timer_plot = QTimer()
        self.timer_plot.setInterval(500)
        self.timer_plot.timeout.connect(self.update_plot)
        self.timer_plot.start()

    def receive_data(self, update_signal):
        self.cpu_usage = update_signal
        self.line.setData(self.time, self.cpu_usage)

    def update_plot(self):
        # Update the plot with new data
        self.time = self.time[1:]
        self.time.append(self.time[-1] + 1)
        self.cpu_usage = self.cpu_usage[1:]
        self.cpu_usage.append(psutil.cpu_percent(interval=0.10))
        self.line.setData(self.time, self.cpu_usage)


app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()
