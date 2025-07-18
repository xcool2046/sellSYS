"""
通用样式定义 - 确保所有组件样式一致
"""

# 通用下拉框样式 - 确保文字颜色清晰可见
COMBOBOX_STYLE = """
QComboBox {
    border: 1px solid #ced4da;
    border-radius: 3px;
    padding: 6px 8px;
    font-size: 12px;
    background-color: white;
    color: #333333;
    min-height: 20px;
}
QComboBox:focus {
    border-color: #007bff;
    outline: none;
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
    color: #333333;
    background-color: white;
    border: none;
}
QComboBox QAbstractItemView::item:hover {
    background-color: #f8f9fa;
    color: #333333;
}
QComboBox QAbstractItemView::item:selected {
    background-color: #e3f2fd;
    color: #1976d2;
}
"""

# 通用输入框样式
LINEEDIT_STYLE = """
QLineEdit {
    border: 1px solid #ced4da;
    border-radius: 3px;
    padding: 6px 8px;
    font-size: 12px;
    background-color: white;
    color: #333333;
}
QLineEdit:focus {
    border-color: #007bff;
    outline: none;
}
QLineEdit:disabled {
    background-color: #f8f9fa;
    color: #6c757d;
}
"""

# 通用文本区域样式
TEXTEDIT_STYLE = """
QTextEdit {
    border: 1px solid #ced4da;
    border-radius: 3px;
    padding: 6px 8px;
    font-size: 12px;
    background-color: white;
    color: #333333;
}
QTextEdit:focus {
    border-color: #007bff;
    outline: none;
}
"""

# 通用按钮样式
BUTTON_PRIMARY_STYLE = """
QPushButton {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 3px;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: bold;
    min-width: 80px;
}
QPushButton:hover {
    background-color: #0056b3;
}
QPushButton:pressed {
    background-color: #004085;
}
QPushButton:disabled {
    background-color: #6c757d;
}
"""

BUTTON_SECONDARY_STYLE = """
QPushButton {
    background-color: #6c757d;
    color: white;
    border: none;
    border-radius: 3px;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: bold;
    min-width: 80px;
}
QPushButton:hover {
    background-color: #545b62;
}
QPushButton:pressed {
    background-color: #3d4142;
}
"""

# 通用复选框样式
CHECKBOX_STYLE = """
QCheckBox {
    color: #333333;
    font-size: 12px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
}
QCheckBox::indicator:unchecked {
    border: 1px solid #ced4da;
    background-color: white;
    border-radius: 2px;
}
QCheckBox::indicator:checked {
    border: 1px solid #007bff;
    background-color: #007bff;
    border-radius: 2px;
}
QCheckBox::indicator:hover {
    border-color: #007bff;
}
"""

# 对话框标题栏样式
DIALOG_TITLE_STYLE = """
QLabel {
    font-size: 16px;
    font-weight: bold;
    color: white;
    background-color: #4a90e2;
    padding: 15px 20px;
    margin: 0;
}
"""

# 对话框内容样式
DIALOG_CONTENT_STYLE = """
QDialog {
    background-color: white;
}
QLabel {
    font-size: 12px;
    color: #333333;
}
"""

def apply_combobox_style(combobox):
    """应用下拉框样式"""
    combobox.setStyleSheet(COMBOBOX_STYLE)

def apply_lineedit_style(lineedit):
    """应用输入框样式"""
    lineedit.setStyleSheet(LINEEDIT_STYLE)

def apply_textedit_style(textedit):
    """应用文本区域样式"""
    textedit.setStyleSheet(TEXTEDIT_STYLE)

def apply_primary_button_style(button):
    """应用主要按钮样式"""
    button.setStyleSheet(BUTTON_PRIMARY_STYLE)

def apply_secondary_button_style(button):
    """应用次要按钮样式"""
    button.setStyleSheet(BUTTON_SECONDARY_STYLE)

def apply_checkbox_style(checkbox):
    """应用复选框样式"""
    checkbox.setStyleSheet(CHECKBOX_STYLE)

# 导出
__all__ = [
    'COMBOBOX_STYLE', 'LINEEDIT_STYLE', 'TEXTEDIT_STYLE',
    'BUTTON_PRIMARY_STYLE', 'BUTTON_SECONDARY_STYLE', 'CHECKBOX_STYLE',
    'DIALOG_TITLE_STYLE', 'DIALOG_CONTENT_STYLE',
    'apply_combobox_style', 'apply_lineedit_style', 'apply_textedit_style',
    'apply_primary_button_style', 'apply_secondary_button_style', 'apply_checkbox_style'
]
