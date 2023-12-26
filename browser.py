import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://carsonday.pro"))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # Navigation Bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Back Button
        back_btn = QAction('Back', self)
        back_btn.setStatusTip('Back to previous page')
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        # Forward Button
        forward_btn = QAction('Forward', self)
        forward_btn.setStatusTip('Forward to next page')
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        # Reload Button
        reload_btn = QAction('Reload', self)
        reload_btn.setStatusTip('Reload page')
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        # Home Button
        home_btn = QAction('Home', self)
        home_btn.setStatusTip('Go home')
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Updating URL bar
        self.browser.urlChanged.connect(self.update_urlbar)

        # Settings Action
        settings_action = QAction('Settings', self)
        settings_action.setStatusTip('Open Settings')
        settings_action.triggered.connect(self.open_settings)
        navbar.addAction(settings_action)

        # Default settings
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

        # Home page URL
        self.home_label = QLabel('Home Page URL:')
        self.home_edit = QLineEdit(self.parent().home_url)
        self.home_edit.setPlaceholderText('Enter home page URL')

        # Save button
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_settings)

        # Layout
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
    QApplication.setApplicationName("Car Browser")
    window = Browser()
    app.exec_()
