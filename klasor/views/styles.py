GLOBAL_STYLE = """
QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #334155;
}
QLineEdit, QComboBox {
    padding: 8px 12px;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    background-color: #ffffff;
    selection-background-color: #3b82f6;
}
QLineEdit:focus, QComboBox:focus {
    border: 2px solid #3b82f6;
}
QPushButton {
    background-color: #3b82f6;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #2563eb;
}
QPushButton#CikisButonu {
    background-color: #ef4444;
}
QPushButton#CikisButonu:hover {
    background-color: #dc2626;
}
QPushButton#YenileButonu {
    background-color: #10b981;
}
QPushButton#YenileButonu:hover {
    background-color: #059669;
}
QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    gridline-color: #e2e8f0;
}
QHeaderView::section {
    background-color: #f1f5f9;
    color: #0f172a;
    padding: 6px;
    border: none;
    border-bottom: 2px solid #cbd5e1;
    font-weight: bold;
}
"""