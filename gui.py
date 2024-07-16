import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QFileDialog, QTableWidget, QTableWidgetItem,
                             QHBoxLayout, QHeaderView, QCheckBox, QMessageBox, QAbstractItemView)
from PyQt5.QtCore import Qt
from main import DiscordImageDownloader


class DownloaderGUI(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the main window's properties
        self.layout = None
        self.token_label = None
        self.token_input = None

        self.button_layout = None
        self.file_button = None
        self.emoji_checkbox = None

        self.add_manual_entry_layout = None
        self.channel_id_input = None
        self.folder_path_input = None
        self.limit_input = None
        self.add_button = None

        self.table_widget = None

        self.add_button_layout = None
        self.delete_button = None
        self.start_button = None

        self.pos_x = 100
        self.pos_y = 100
        self.width = 800
        self.height = 500

        self.setWindowTitle('Discord Image Downloader')
        self.setGeometry(self.pos_x, self.pos_y, self.width, self.height)

        # Initialize the user interface
        self.initUI()

    def initUI(self):
        # Main layout
        self.layout = QVBoxLayout()

        # Bot Token Input
        self.token_label = QLabel('Bot Token:')
        self.layout.addWidget(self.token_label)

        self.token_input = QLineEdit()
        self.token_input.setEchoMode(QLineEdit.Password)  # Mask the token input
        self.layout.addWidget(self.token_input)

        # Upload Channels File Button
        self.button_layout = QHBoxLayout()
        self.file_button = QPushButton('Upload Channels File')
        self.file_button.clicked.connect(self.upload_file)
        self.button_layout.addWidget(self.file_button)

        # Checkbox for Emoji Reaction
        self.emoji_checkbox = QCheckBox("Enable Emoji Reaction")
        self.emoji_checkbox.setChecked(True)
        self.button_layout.addWidget(self.emoji_checkbox)

        # Manual Input Fields for Channel ID, Folder Path, and Limit
        self.add_manual_entry_layout = QHBoxLayout()
        self.channel_id_input = QLineEdit()
        self.channel_id_input.setPlaceholderText('Channel ID')
        self.add_manual_entry_layout.addWidget(self.channel_id_input)

        self.folder_path_input = QLineEdit()
        self.folder_path_input.setPlaceholderText('Folder Path')
        self.add_manual_entry_layout.addWidget(self.folder_path_input)

        self.limit_input = QLineEdit()
        self.limit_input.setPlaceholderText('Limit')
        self.limit_input.setText('0')  # Set default value to 0
        self.add_manual_entry_layout.addWidget(self.limit_input)

        self.add_button = QPushButton('Add Channel')
        self.add_button.clicked.connect(self.add_channel_manually)
        self.add_manual_entry_layout.addWidget(self.add_button)

        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.add_manual_entry_layout)

        # Table Widget for Displaying Channels
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['Channel ID', 'Folder Path', 'Limit'])
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table_widget)

        self.add_button_layout = QHBoxLayout()

        # Delete Selected Rows Button
        self.delete_button = QPushButton('Delete Selected')
        self.delete_button.clicked.connect(self.delete_selected_rows)

        # Add hover effect using stylesheet
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: lightgray;
                border: 1px solid black;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: red;
                color: white;
            }
        """)

        self.add_button_layout.addWidget(self.delete_button)

        # Start Download Button
        self.start_button = QPushButton('Start Download')
        self.start_button.clicked.connect(self.start_download)

        # Add hover effect using stylesheet
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: lightgray;
                border: 1px solid black;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: green;
                color: white;
            }
        """)

        self.add_button_layout.addWidget(self.start_button)

        self.layout.addLayout(self.add_button_layout)

        self.setLayout(self.layout)

        # Set table selection behavior to select rows
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def upload_file(self):
        """
        Opens a file dialog to select and read a file containing channel information.
        Populates the table with the channels and sets the bot token if present in the file.
        """
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

    def add_channel_manually(self):
        """
        Adds a channel manually to the table using the input fields for Channel ID, Folder Path, and Limit.
        """
        channel_id_text = self.channel_id_input.text().strip()
        folder_path_text = self.folder_path_input.text().strip()
        limit_text = self.limit_input.text().strip()

        if not channel_id_text or not folder_path_text or not limit_text:
            QMessageBox.warning(self, 'Input Error', 'Please fill in all fields.')
            return

        try:
            channel_id = int(channel_id_text)
            limit = int(limit_text)
        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Channel ID and Limit must be integers.')
            return

        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)
        self.table_widget.setItem(row_position, 0, QTableWidgetItem(channel_id_text))
        self.table_widget.setItem(row_position, 1, QTableWidgetItem(folder_path_text))
        self.table_widget.setItem(row_position, 2, QTableWidgetItem(limit_text))

        # Clear the input fields after adding the channel
        self.channel_id_input.clear()
        self.folder_path_input.clear()
        self.limit_input.clear()

    def delete_selected_rows(self):
        """
        Deletes the selected rows from the table.
        """
        selected_rows = sorted(set(index.row() for index in self.table_widget.selectedIndexes()), reverse=True)
        for row in selected_rows:
            self.table_widget.removeRow(row)

    def start_download(self):
        """
        Starts the download process using the provided bot token and channel information.
        """
        bot_token = self.token_input.text()
        if not bot_token:
            QMessageBox.warning(self, 'Missing Token', 'Bot token is required.')
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
                    QMessageBox.warning(self, 'Invalid Data Format', 'Please ensure all fields are filled correctly.')
                    return

        use_emoji = self.emoji_checkbox.isChecked()
        downloader = DiscordImageDownloader(bot_token, channels, use_emoji)
        downloader.run()

    def keyPressEvent(self, event):
        """
        Overrides the key press event to delete selected rows when the Delete key is pressed.
        """
        if event.key() == Qt.Key_Delete:
            self.delete_selected_rows()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DownloaderGUI()
    ex.show()
    sys.exit(app.exec_())
