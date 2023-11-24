from PyQt6.QtCore import QTimer 
from PyQt6.QtWidgets import QMainWindow, QApplication
import requests 
import pyqtgraph as pg
import time 

class DownloadSpeedGraph(QMainWindow):
    def __init__(self):
        super().__init__()

        # Download speed vs time dynamic plot
        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)
        self.plot_graph.setBackground("w")
        self.pen = pg.mkPen(color=(15, 82, 186))
        self.plot_graph.setTitle("Download Speed", color="b", size="20pt")
        styles = {"color": "red", "font-size": "18px"}
        self.plot_graph.setLabel("left", "Download Speed (Mbps)", **styles)
        self.plot_graph.addLegend()
        self.plot_graph.showGrid(x=True, y=True)
        self.plot_graph.setYRange(0, 100)  # Adjust the range as needed
        self.time = list(range(11))
        self.download_speeds = [0] * 11  # Initialize with zeros
        # Get a line reference
        
        self.line = self.plot_graph.plot(
            self.time,
            self.download_speeds,
            name="Download Speed",
            pen=self.pen,
            symbol="+",
            symbolSize=15,
            symbolBrush="b",
        )
        self.plot_graph.getAxis("bottom").setStyle(showValues=False)
        # Disable panning and zooming
        self.plot_graph.getViewBox().setMouseEnabled(x=False, y=False)


        # Add a timer to simulate new download speed measurements
        self.timer = QTimer()
        self.timer.setInterval(300)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def calculate_speed(self, file_url):
        start_time = time.time() 
        file = requests.get(file_url, stream=True)
        total_length = file.headers.get('content-length')
            
        if total_length is not None:
            download_speed = (int(total_length) / (time.time() - start_time)) / 1e6  # Calculate the download speed in Mbps
            return download_speed

    def update_plot(self):
        self.time = self.time[1:]
        self.time.append(self.time[-1] + 1)
        self.download_speeds = self.download_speeds[1:]
        speed = self.calculate_speed("http://ipv4.download.thinkbroadband.com/2MB.zip")
        self.download_speeds.append(speed)
        self.line.setData(self.time, self.download_speeds)

if __name__ == "__main__":
    app = QApplication([])
    main = DownloadSpeedGraph()
    main.show()
    app.exec()
