import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QFileDialog, QTableWidget, QTableWidgetItem,
                             QHBoxLayout, QHeaderView, QCheckBox)
from PyQt5.QtCore import Qt
import os
from main import DiscordImageDownloader


class DownloaderGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.pos_x = 100
        self.pos_y = 100
        self.width = 800
        self.height = 400

        self.setWindowTitle('Discord Image Downloader')
        self.setGeometry(self.pos_x, self.pos_y, self.width, self.height)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.token_label = QLabel('Bot Token:')
        self.layout.addWidget(self.token_label)

        self.token_input = QLineEdit()
        self.token_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.token_input)

        self.button_layout = QHBoxLayout()
        self.file_button = QPushButton('Upload Channels File')
        self.file_button.clicked.connect(self.upload_file)
        self.button_layout.addWidget(self.file_button)

        self.emoji_checkbox = QCheckBox("Enable Emoji Reaction")
        self.emoji_checkbox.setChecked(True)
        self.button_layout.addWidget(self.emoji_checkbox)

        self.layout.addLayout(self.button_layout)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['Channel ID', 'Folder Path', 'Limit'])
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table_widget)

        self.start_button = QPushButton('Start Download')
        self.start_button.clicked.connect(self.start_download)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

    def upload_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Channels File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_path:
            self.table_widget.setRowCount(0)
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if lines[0].startswith("BOT_TOKEN="):
                    bot_token = lines[0].strip().split('=', 1)[1]
                    self.token_input.setText(bot_token)
                    lines = lines[1:]

                for line in lines:
                    parts = line.strip().split(',')
                    if len(parts) == 2:
                        row_position = self.table_widget.rowCount()
                        self.table_widget.insertRow(row_position)
                        self.table_widget.setItem(row_position, 0, QTableWidgetItem(parts[0].strip()))
                        self.table_widget.setItem(row_position, 1, QTableWidgetItem(parts[1].strip()))
                        limit_item = QTableWidgetItem('0')
                        self.table_widget.setItem(row_position, 2, limit_item)

    def start_download(self):
        bot_token = self.token_input.text()
        if not bot_token:
            print("Bot token is required.")
            return

        channels = []
        row_count = self.table_widget.rowCount()
        for row in range(row_count):
            channel_id_item = self.table_widget.item(row, 0)
            folder_path_item = self.table_widget.item(row, 1)
            limit_item = self.table_widget.item(row, 2)
            if channel_id_item and folder_path_item and limit_item:
                try:
                    channel_id = int(channel_id_item.text().strip())
                    folder_path = folder_path_item.text().strip()
                    limit = int(limit_item.text().strip())
                    channels.append((channel_id, folder_path, limit))
                except ValueError:
                    print("Invalid data format. Please ensure all fields are filled correctly.")
                    return

        use_emoji = self.emoji_checkbox.isChecked()
        downloader = DiscordImageDownloader(bot_token, channels, use_emoji)
        downloader.run()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DownloaderGUI()
    ex.show()
    sys.exit(app.exec_())
