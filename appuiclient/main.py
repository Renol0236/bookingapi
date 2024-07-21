import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, \
    QFormLayout, QTableWidgetItem, QTableWidget, QStackedWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from api_client import ApiClient


class MainWindow(QMainWindow):
    def __init__(self, api_client):
        super().__init__()
        self.setWindowTitle("Booking App")
        self.api_client = api_client
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QStackedWidget()

        self.page1 = QWidget()
        self.page2 = QWidget()
        self.page3 = QWidget()
        self.page4 = QWidget()
        self.page5 = QWidget()

        self.init_page1()
        self.init_page2()
        self.init_page3()

        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.page3)

        main_layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        button1 = QPushButton("Page 1")
        button1.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page1))
        button2 = QPushButton("Page 2")
        button2.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page2))
        button3 = QPushButton("Page 3")
        button3.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page3))

        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        button_layout.addWidget(button3)

        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.stacked_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.init_ui()

    def init_page1(self):
        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Add Booking"))
        self.page1.setLayout(layout)

    def init_page2(self):
        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Update Booking"))
        self.page2.setLayout(layout)

    def init_page3(self):
        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Delete Booking"))
        self.page3.setLayout(layout)

    def init_ui(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(50, 120, 255, 255), stop:1 rgba(85, 170, 255, 255)
                );
            }""")


class AuthWindow(QMainWindow):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = None
        self.setWindowTitle("Login Window")
        self.api_client = api_client
        self.setGeometry(100, 100, 300, 150)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QFormLayout(central_widget)

        # Username filed
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        # Password filed
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        # Login button
        self.login_button = QPushButton()
        self.login_button.setText("Login")
        self.login_button.clicked.connect(self.handle_login)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red")

        # Adding Widgets
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.error_label)

    def handle_login(self):
        username, password = self.username_input.text(), self.password_input.text()

        try:
            self.api_client.login(username, password)
            self.main_window = MainWindow(self.api_client)
            self.main_window.show()
            self.close()
        except Exception as e:
            self.error_label.setText(str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    api_client = ApiClient("http://127.0.0.1:8000")
    auth_window = AuthWindow(api_client)
    auth_window.show()
    sys.exit(app.exec_())
