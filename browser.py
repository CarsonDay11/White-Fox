import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-web-security'

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        self.setWindowIcon(QIcon(icon_path))

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://car-browser.vercel.app/"))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_urlbar)

        settings_action = QAction('Settings', self)
        settings_action.triggered.connect(self.open_settings)
        navbar.addAction(settings_action)

        self.settings = QSettings("MyCompany", "MyBrowser")
        self.home_url = self.settings.value("home_url", "http://www.google.com")

    def navigate_home(self):
        self.browser.setUrl(QUrl(self.home_url))

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.browser.setUrl(q)

    def update_urlbar(self, q):
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec_()

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle('Browser Settings')

        self.home_label = QLabel('Home Page URL:')
        self.home_edit = QLineEdit(self.parent().home_url)
        self.home_edit.setPlaceholderText('Enter the home page URL')

        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_settings)

        layout = QVBoxLayout()
        layout.addWidget(self.home_label)
        layout.addWidget(self.home_edit)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_settings(self):
        home_url = self.home_edit.text()
        self.parent().home_url = home_url
        self.parent().settings.setValue("home_url", home_url)

        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName("White Fox")
    window = Browser()
    app.exec_()
