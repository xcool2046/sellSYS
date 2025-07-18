"""
对话框通用样式定义
确保所有对话框中的文字都可见
"""

DIALOG_STYLE = """
QDialog {
    background-color: white;
    color: #333333;
}

QLabel {
    color: #333333;
    font-size: 12px;
    padding: 4px;
}

QLineEdit {
    border: 1px solid #ced4da;
    border-radius: 3px;
    padding: 6px 8px;
    font-size: 12px;
    color: #333333;
    background-color: white;
}

QLineEdit:focus {
    border-color: #4a90e2;
    outline: none;
}

QLineEdit::placeholder {
    color: #6c757d;
    font-style: normal;
}

QTextEdit {
    border: 1px solid #ced4da;
    border-radius: 3px;
    padding: 6px 8px;
    font-size: 12px;
    color: #333333;
    background-color: white;
}

QTextEdit:focus {
    border-color: #4a90e2;
    outline: none;
}

QComboBox {
    border: 1px solid #ced4da;
    border-radius: 3px;
    padding: 6px 8px;
    font-size: 12px;
    color: #333333;
    background-color: white;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #666;
    margin-right: 5px;
}

QComboBox QAbstractItemView {
    border: 1px solid #ced4da;
    background-color: white;
    color: #333333;
    selection-background-color: #e3f2fd;
    selection-color: #1976d2;
    outline: none;
}

QComboBox QAbstractItemView::item {
    padding: 6px 8px;
    border: none;
    color: #333333;
}

QComboBox QAbstractItemView::item:hover {
    background-color: #f8f9fa;
    color: #333333;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #e3f2fd;
    color: #1976d2;
}

QRadioButton {
    color: #333333;
    font-size: 12px;
}

QRadioButton::indicator {
    width: 16px;
    height: 16px;
}

QRadioButton::indicator:unchecked {
    border: 2px solid #ced4da;
    border-radius: 8px;
    background-color: white;
}

QRadioButton::indicator:checked {
    border: 2px solid #4a90e2;
    border-radius: 8px;
    background-color: #4a90e2;
}

QCheckBox {
    color: #333333;
    font-size: 12px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
}

QCheckBox::indicator:unchecked {
    border: 2px solid #ced4da;
    border-radius: 2px;
    background-color: white;
}

QCheckBox::indicator:checked {
    border: 2px solid #4a90e2;
    border-radius: 2px;
    background-color: #4a90e2;
}

QPushButton {
    background-color: #4a90e2;
    color: white;
    border: none;
    border-radius: 3px;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #357abd;
}

QPushButton:pressed {
    background-color: #2968a3;
}

QPushButton:disabled {
    background-color: #6c757d;
    color: #adb5bd;
}

QScrollArea {
    border: 1px solid #ced4da;
    background-color: white;
}

QScrollArea QWidget {
    background-color: white;
    color: #333333;
}

QFrame {
    background-color: white;
    color: #333333;
}

QGroupBox {
    color: #333333;
    font-size: 12px;
    font-weight: bold;
    border: 1px solid #ced4da;
    border-radius: 3px;
    margin-top: 10px;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
    color: #333333;
}

/* 滚动条样式 */
QScrollBar:vertical {
    border: none;
    background: #f1f1f1;
    width: 12px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #c1c1c1;
    min-height: 20px;
    border-radius: 6px;
}

QScrollBar::handle:vertical:hover {
    background: #a8a8a8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}

QScrollBar:horizontal {
    border: none;
    background: #f1f1f1;
    height: 12px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background: #c1c1c1;
    min-width: 20px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal:hover {
    background: #a8a8a8;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    border: none;
    background: none;
}

/* 消息框样式 */
QMessageBox {
    background-color: white;
    color: #333333;
}

QMessageBox QLabel {
    color: #333333;
    font-size: 12px;
}

QMessageBox QPushButton {
    min-width: 80px;
}
"""

def apply_dialog_style(dialog):
    """为对话框应用通用样式"""
    dialog.setStyleSheet(DIALOG_STYLE)

def show_message_box(parent, title, message, icon=None):
    """显示带有正确样式的消息框"""
    from PySide6.QtWidgets import QMessageBox

    if icon is None:
        icon = QMessageBox.Icon.Information

    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(icon)

    # 应用样式确保文字可见
    msg_box.setStyleSheet("""
        QMessageBox {
            background-color: white;
            color: #333333;
        }
        QMessageBox QLabel {
            color: #333333;
            font-size: 12px;
            padding: 10px;
        }
        QMessageBox QPushButton {
            background-color: #4a90e2;
            color: white;
            border: none;
            border-radius: 3px;
            padding: 8px 16px;
            font-size: 12px;
            font-weight: bold;
            min-width: 80px;
        }
        QMessageBox QPushButton:hover {
            background-color: #357abd;
        }
    """)

    return msg_box.exec()
