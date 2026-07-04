import sys
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib
matplotlib.rcParams["font.sans-serif"] = [
    "PingFang TC",
    "Heiti TC",
    "Arial Unicode MS",
    "Noto Sans CJK TC"
]
matplotlib.rcParams["axes.unicode_minus"] = False


from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QSplitter
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


tickers = {
    "台積電": "2330.TW",
    "聯電": "2303.TW",
    "聯發科": "2454.TW",
    "鴻海": "2317.TW",
}


def fetch_data():
    data = yf.download(
        list(tickers.values()),
        start="2026-01-01",
        interval="1d",
        auto_adjust=True,
        threads=False,
        progress=False
    )
    close = data["Close"].rename(columns={v: k for k, v in tickers.items()})
    returns = close.pct_change().dropna()
    corr = returns.corr()
    latest = close.tail(1).T.reset_index()
    latest.columns = ["股票", "收盤價"]
    latest["收盤價"] = latest["收盤價"].round(2)
    return close, returns, corr, latest


class HeatmapCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

    def update_heatmap(self, corr: pd.DataFrame):
        self.ax.clear()
        sns.heatmap(
            corr,
            annot=True,
            fmt=".2f",
            cmap="RdBu_r",
            vmin=-1,
            vmax=1,
            center=0,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
            ax=self.ax
        )
        self.ax.set_title("日報酬率相關係數")
        self.ax.set_xlabel("")
        self.ax.set_ylabel("")
        self.figure.tight_layout()
        self.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("四檔股票相關係數")
        self.resize(1100, 700)

        self.setStyleSheet("""
            QMainWindow { background: #f6f8fb; }
            QLabel#Title { font-size: 22px; font-weight: 700; color: #111827; }
            QLabel#Sub { font-size: 13px; color: #6b7280; }
            QLabel#Summary { font-size: 13px; color: #374151; }
            QPushButton {
                background: #2563eb; color: white; border: none;
                padding: 10px 16px; border-radius: 10px; font-weight: 600;
            }
            QPushButton:hover { background: #1d4ed8; }
            QTableWidget {
                background: white; border: 1px solid #e5e7eb;
                border-radius: 12px; gridline-color: #e5e7eb;
                font-size: 13px;
            }
            QHeaderView::section {
                background: #eaf2ff; color: #111827;
                padding: 8px; border: none; font-weight: 700;
            }
        """)

        central = QWidget()
        main_layout = QVBoxLayout(central)

        top_row = QHBoxLayout()
        title_box = QVBoxLayout()
        self.title = QLabel("四檔股票日報酬相關係數")
        self.title.setObjectName("Title")
        self.sub = QLabel("快速查看台積電、聯電、聯發科、鴻海的關聯性")
        self.sub.setObjectName("Sub")
        title_box.addWidget(self.title)
        title_box.addWidget(self.sub)
        top_row.addLayout(title_box)
        top_row.addStretch()

        self.btn = QPushButton("更新資料")
        self.btn.clicked.connect(self.load_data)
        top_row.addWidget(self.btn)

        main_layout.addLayout(top_row)

        self.summary = QLabel("")
        self.summary.setObjectName("Summary")
        main_layout.addWidget(self.summary)

        splitter = QSplitter(Qt.Horizontal)

        self.table = QTableWidget()
        splitter.addWidget(self.table)

        self.heatmap = HeatmapCanvas()
        splitter.addWidget(self.heatmap)

        splitter.setSizes([520, 580])
        main_layout.addWidget(splitter)

        self.setCentralWidget(central)
        self.load_data()

    def load_data(self):
        try:
            close, returns, corr, latest = fetch_data()

            self.summary.setText(
                "最新收盤價："
                + " / ".join([f"{r['股票']} {r['收盤價']}" for _, r in latest.iterrows()])
            )

            self.table.setRowCount(corr.shape[0])
            self.table.setColumnCount(corr.shape[1])
            self.table.setHorizontalHeaderLabels(corr.columns.tolist())
            self.table.setVerticalHeaderLabels(corr.index.tolist())

            for i in range(corr.shape[0]):
                for j in range(corr.shape[1]):
                    val = corr.iloc[i, j]
                    item = QTableWidgetItem(f"{val:.4f}")
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(i, j, item)

            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()

            self.heatmap.update_heatmap(corr.round(2))

        except Exception as e:
            QMessageBox.critical(self, "錯誤", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
