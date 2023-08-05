from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
import subprocess
import ctypes
import os
import numpy as np
import matplotlib.pyplot as plt
import math

def show_graph():
    pass

def drop_zero(num):
        num_str = str(num)
        if num_str.endswith('.0'):
            return num_str[:-2]
        return num_str


class mainDll:
    def __init__(self, dll_path):
        self.dll_handle = ctypes.cdll.LoadLibrary(dll_path)
    
    def create_compile(self, text):
        self.dll_handle.create_compile(bytes(text, encoding='ASCII'))

    def create_compile_x(self, text):
        self.dll_handle.create_compile_x(bytes(text, encoding='ASCII'))

    def create_expression(self, count):
        self.dll_handle.create_expression(bytes(str(count), encoding='ASCII'))


class ExampleDll:
    def __init__(self, dll_path):
        self.dll_handle = ctypes.cdll.LoadLibrary(dll_path)
        self.dll_handle.calculate.restype = ctypes.c_double

    def calculate(self):
        return self.dll_handle.calculate()
    
    def calculate_x(self, x):
        return self.dll_handle.calculate(ctypes.c_double(x))

    def __del__(self):
        ctypes.windll.kernel32.FreeLibrary(ctypes.c_void_p(self.dll_handle._handle))

class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(500, 400)
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)

        self.line_edit = QLineEdit()
        self.line_edit.setReadOnly(True)

        main_layout.addWidget(self.line_edit)
        buttons_layout = QVBoxLayout()
        button_labels = [
            ['C', 'CA', '(', ')'],
            ['7', '8', '9', '/','sin', 'asin'],
            ['4', '5', '6', '*', 'cos', 'acos'],
            ['1', '2', '3', '-', 'tan', 'atan'],
            ['0', '.', '=', '+','sqrt', '^',],
            [ 'log', 'ln', 'mod', 'x'],
        ]

        for row in button_labels:
            row_layout = QHBoxLayout()
            for label in row:
                button = QPushButton(label)
                button.clicked.connect(self.handle_button_clicked)
                row_layout.addWidget(button)
            buttons_layout.addLayout(row_layout)

        main_layout.addLayout(buttons_layout)
        self.setCentralWidget(main_widget)

    def handle_button_clicked(self):
        global count
        button = self.sender()
        label = button.text()
        if self.line_edit.text() == 'ERR':
            self.line_edit.clear()
        if label == '=':
            text = self.line_edit.text()
            pwd = os.getcwd()
            if 'x' in self.line_edit.text():
                main_c = mainDll(f"{pwd}\\main.dll")
                main_c.create_compile_x(text)
                main_c.create_expression(1)
                example = ExampleDll(f"{pwd}\\expression1.dll")
                x = np.linspace(-math.pi, math.pi, 1000)
                y = [example.calculate_x(i) for i in x]
                plt.plot(x, y)
                plt.title("Graph")
                plt.xlabel("Values of x")
                plt.ylabel("Values of y")
                plt.axhline(0, color='black', linewidth=0.5)
                plt.axvline(0, color='black', linewidth=0.5)
                plt.show()
                
            if os.path.exists(f"{pwd}\\expression.c") and 'x' not in text:
                main_c = mainDll(f"{pwd}\\main.dll")
                main_c.create_compile(text)
                main_c.create_expression(1)
                example = ExampleDll(f"{pwd}\\expression1.dll")
                result = example.calculate()
                self.line_edit.clear()
                self.line_edit.setText(self.line_edit.text() + drop_zero(result))
            else:
                self.line_edit.clear()
                self.line_edit.setText('ERR')
        elif label == 'C':
            text = self.line_edit.text()
            if text:
                self.line_edit.setText(text[:-1])
        elif label == 'CA':
            self.line_edit.clear()
        elif label == 'sin' or label == 'cos' or label == 'tan' or label == 'asin' or label == 'acos' or label == 'atan' or label == 'sqrt':
            self.line_edit.setText(self.line_edit.text() + label + '(')
        else:
            self.line_edit.setText(self.line_edit.text() + label)

if __name__ == '__main__':
    app = QApplication([])
    window = CalculatorWindow()
    window.show()
    app.exec()
