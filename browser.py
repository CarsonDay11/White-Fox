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
        back_btn.setStatusTip('Back to the previous page')
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        # Forward Button
        forward_btn = QAction('Forward', self)
        forward_btn.setStatusTip('Forward to the next page')
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        # Reload Button
        reload_btn = QAction('Reload', self)
        reload_btn.setStatusTip('Reload the page')
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

        # Theme Combo Box
        self.theme_combobox = QComboBox()
        self.theme_combobox.addItems(["Light Theme", "Dark Theme"])
        self.theme_combobox.setCurrentText("Light Theme")
        self.theme_combobox.currentIndexChanged.connect(self.apply_theme)
        navbar.addWidget(self.theme_combobox)

        # Apply the initial theme
        self.apply_theme()

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

    def apply_theme(self):
        theme = self.theme_combobox.currentText()
        if theme == "Dark Theme":
            self.setStyleSheet("QMainWindow{background-color: #333; color: #FFF;}")
        else:
            self.setStyleSheet("QMainWindow{background-color: #FFF; color: #000;}")

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
        self.home_edit.setPlaceholderText('Enter the home page URL')

        # Theme Combo Box
        self.theme_label = QLabel('Select Theme:')
        self.theme_combobox = QComboBox()
        self.theme_combobox.addItems(["Light Theme", "Dark Theme"])
        self.theme_combobox.setCurrentText("Light Theme")

        # Save button
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_settings)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.home_label)
        layout.addWidget(self.home_edit)
        layout.addWidget(self.theme_label)
        layout.addWidget(self.theme_combobox)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_settings(self):
        home_url = self.home_edit.text()
        self.parent().home_url = home_url
        self.parent().settings.setValue("home_url", home_url)

        # Save Theme
        selected_theme = self.theme_combobox.currentText()
        self.parent().settings.setValue("theme", selected_theme)
        self.parent().apply_theme()  # Apply the theme immediately

        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Car Browser")
    window = Browser()
    app.exec_()
