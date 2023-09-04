from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QToolBar, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtCore import QTimer
import subprocess
import ctypes
import os
import matplotlib.pyplot as plt
import math
from errors import err_list, list_, list_2
from random import choice

def drop_zero(num):
        num_str = str(num)
        if num_str.endswith('.0'):
            return num_str[:-2]
        return num_str

class mainDll:
    def __init__(self, dll_path):
        self.dll_handle = ctypes.cdll.LoadLibrary(dll_path)
    
    def err_check(self, text):
        return self.dll_handle.err_check(bytes(text, encoding='ASCII'))
    
    def create_compile(self, text):
        self.dll_handle.create_compile(bytes(text, encoding='ASCII'))

    def create_compile_x(self, text):
        self.dll_handle.create_compile_x(bytes(text, encoding='ASCII'))
    
    def create_compile_credit(self, principal, annualRate, loanDurationMonths):
        principal = bytes(principal, encoding='ASCII')
        annualRate = bytes(annualRate, encoding='ASCII')
        loanDurationMonths = bytes(loanDurationMonths, encoding='ASCII')
        self.dll_handle.create_compile_credit(principal, annualRate, loanDurationMonths)
    
    def create_compile_deposit(self, principal, annualRate, depositDurationMonths):
        principal = bytes(principal, encoding='ASCII')
        annualRate = bytes(annualRate, encoding='ASCII')
        depositDurationMonths = bytes(depositDurationMonths, encoding='ASCII')
        self.dll_handle.create_compile_deposit(principal, annualRate, depositDurationMonths)

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


class CreditWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_image)
        self.setWindowTitle("Credit calculator")
        self.setFixedSize(400, 400)
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)
        self.label1 = QLabel("Principal amount")
        main_layout.addWidget(self.label1)
        self.line_edit1 = QLineEdit()
        self.line_edit1.setReadOnly(False)
        main_layout.addWidget(self.line_edit1)
        self.label2 = QLabel("Annual rate")
        main_layout.addWidget(self.label2)
        self.line_edit2 = QLineEdit()
        self.line_edit2.setReadOnly(False)
        main_layout.addWidget(self.line_edit2)
        self.label3 = QLabel("Duration in months")
        main_layout.addWidget(self.label3)
        self.line_edit3 = QLineEdit()
        self.line_edit3.setReadOnly(False)
        main_layout.addWidget(self.line_edit3)
        self.setCentralWidget(main_widget)
        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate_clicked)
        main_layout.addWidget(calculate_button)
        self.label4 = QLabel()
        main_layout.addWidget(self.label4)
        self.gif_path = "install_windows/cat-monday-left-me-broken-cat.gif"
        self.show_image()
        self.line_edit4 = QLineEdit()
        self.line_edit4.setReadOnly(True)
        main_layout.addWidget(self.line_edit4)


    def show_image(self):
        pixmap = QPixmap("install_windows/cat-monday-left-me-broken-cat.gif")  
        self.label4.setPixmap(pixmap)
    def calculate_clicked(self):
        pixmap = QMovie(self.gif_path)
        self.label4.setMovie(pixmap)
        pixmap.start()
        pwd = os.getcwd()
        main_c = mainDll(f"{pwd}\\main.dll")
        print(self.line_edit1.text(),self.line_edit2.text(), self.line_edit3.text())
        main_c.create_compile_credit(self.line_edit1.text(),self.line_edit2.text(), self.line_edit3.text())
        try:
            subprocess.run(["gcc", "-shared", "-o", "expression.dll", "expression.c"], check=True)
            print("Compilation successful.")
            example = ExampleDll(f"{pwd}\\expression.dll")
            result = example.calculate()
            print("result:",result)
            self.line_edit4.setText(str(result))
            self.timer.start(7000)
        except Exception as e:
            print("Exception:", e)
            self.line_edit4.setText(choice(err_list))
            self.timer.start(2000)


class deposittWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_image)
        self.setWindowTitle("deposit calculator")
        self.setFixedSize(400, 400)
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)
        self.label1 = QLabel("Principal amount")
        main_layout.addWidget(self.label1)
        self.line_edit1 = QLineEdit()
        self.line_edit1.setReadOnly(False)
        main_layout.addWidget(self.line_edit1)
        self.label2 = QLabel("Annual rate")
        main_layout.addWidget(self.label2)
        self.line_edit2 = QLineEdit()
        self.line_edit2.setReadOnly(False)
        main_layout.addWidget(self.line_edit2)
        self.label3 = QLabel("deposit duration in months")
        main_layout.addWidget(self.label3)
        self.line_edit3 = QLineEdit()
        self.line_edit3.setReadOnly(False)
        main_layout.addWidget(self.line_edit3)
        self.setCentralWidget(main_widget)
        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate_clicked)
        main_layout.addWidget(calculate_button)
        self.label4 = QLabel()
        main_layout.addWidget(self.label4)
        self.gif_path = "install_windows/cat-small.gif"
        self.show_image()
        self.line_edit4 = QLineEdit()
        self.line_edit4.setReadOnly(True)
        main_layout.addWidget(self.line_edit4)

    def show_image(self):
        pixmap = QPixmap("install_windows/cat-small.gif")  
        self.label4.setPixmap(pixmap)
    def calculate_clicked(self):
        pixmap = QMovie(self.gif_path)
        self.label4.setMovie(pixmap)
        pixmap.start()
        pwd = os.getcwd()
        main_c = mainDll(f"{pwd}\\main.dll")
        print(self.line_edit1.text(),self.line_edit2.text(), self.line_edit3.text())
        main_c.create_compile_deposit(self.line_edit1.text(),self.line_edit2.text(), self.line_edit3.text())
        try:
            subprocess.run(["gcc", "-shared", "-o", "expression.dll", "expression.c"], check=True)
            print("Compilation successful.")
            example = ExampleDll(f"{pwd}\\expression.dll")
            result = example.calculate()
            print("result:",result)
            self.line_edit4.setText(str(result))
            self.timer.start(3000)
        except Exception as e:
            print("Exception:", e)
            self.line_edit4.setText(choice(err_list))
            self.timer.start(3000)


x_max = ''
x_min = ''
x = ''
class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(500, 400)
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        credit_button = QPushButton('Credit calculator')
        credit_button.clicked.connect(self.handle_button_clicked)
        toolbar.addWidget(credit_button)
        credit_button = QPushButton('Deposit calculator')
        credit_button.clicked.connect(self.handle_button_clicked)
        toolbar.addWidget(credit_button)
        graph_button = QPushButton('Graph')
        graph_button.clicked.connect(self.handle_button_clicked)
        toolbar.addWidget(graph_button)
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

        self.label5 = QLabel("X (0 by default)")       
        main_layout.addWidget(self.label5)
        self.line_x = QLineEdit()
        self.line_x.setReadOnly(False)
        main_layout.addWidget(self.line_x)
        self.setCentralWidget(main_widget)

        self.label3 = QLabel("X min (for plot)")
        main_layout.addWidget(self.label3)
        self.line_x_min = QLineEdit()
        self.line_x_min.setReadOnly(False)
        main_layout.addWidget(self.line_x_min)

        self.label4 = QLabel("X max (for plot)")       
        main_layout.addWidget(self.label4)
        self.line_x_max = QLineEdit()
        self.line_x_max.setReadOnly(False)
        main_layout.addWidget(self.line_x_max)
        self.setCentralWidget(main_widget)

    def handle_button_clicked(self):
        global x_max, x_min
        button = self.sender()
        label = button.text()
        if 'ERR' in self.line_edit.text():
            self.line_edit.clear()
        if label == '=':
            text = self.line_edit.text()
            pwd = os.getcwd()
            main_c = mainDll(f"{pwd}\\main.dll")
            if 'x' in text:
                main_c.create_compile_x(text)
                if self.line_x.text() == '':
                    x = 0
                else:
                    try:  
                        x = float(self.line_x.text())
                    except Exception as e:
                        print("Exception:", e)
                        self.line_edit.clear()
                        self.line_edit.setText(choice(err_list))
                try:
                    subprocess.run(["gcc", "-shared", "-o", "expression.dll", "expression.c"], check=True)
                    print("Compilation successful.")
                    example = ExampleDll(f"{pwd}\\expression.dll")
                    result = example.calculate_x(x)
                    self.line_edit.clear()
                    self.line_edit.setText(self.line_edit.text() + drop_zero(result))
                    os.remove('expression.c')
                except Exception as e:
                    print("Exception:", e)
                    self.line_edit.clear()
                    self.line_edit.setText(choice(err_list))
                
            if 'x' not in text:
                main_c.create_compile(text)
                try:
                    subprocess.run(["gcc", "-shared", "-o", "expression.dll", "expression.c"], check=True)
                    print("Compilation successful.")
                    example = ExampleDll(f"{pwd}\\expression.dll")
                    result = example.calculate()
                    self.line_edit.clear()
                    self.line_edit.setText(self.line_edit.text() + drop_zero(result))
                    os.remove('expression.c')
                except Exception as e:
                    print("Exception:", e)
                    self.line_edit.clear()
                    self.line_edit.setText(choice(err_list))
        elif label == 'C':
            text = self.line_edit.text()
            if text:
                for item in  list_2 + list_:
                    if text.endswith(item + '('):
                        self.line_edit.setText(text[:-len(item)-1])
                        return
                self.line_edit.setText(text[:-1])
        elif label == 'CA':
            self.line_edit.clear()
        elif label in list_ or label in list_2:
            self.line_edit.setText(self.line_edit.text() + label + '(')
        elif label == 'Credit calculator':
            self.credit_window = CreditWindow()
            self.credit_window.show()
        elif label == 'Deposit calculator':
            self.deposit_window = deposittWindow()
            self.deposit_window.show()
        elif label == 'Graph':
            text = self.line_edit.text()
            pwd = os.getcwd()
            main_c = mainDll(f"{pwd}\\main.dll")
            if 'x' in text:
                try:
                    if self.line_x_max.text() == '' or self.line_x_min.text() == '':
                        x_max = math.pi
                        x_min = -math.pi
                    else:
                        x_max = float(self.line_x_max.text())
                        x_min = float(self.line_x_min.text())                       
                except Exception as e:
                    print("Exception: ", e)
                    self.line_x_max.clear()
                    self.line_x_min.clear()
                    self.line_x_max.setText("Err")
                    self.line_x_min.setText("Err")
                main_c.create_compile_x(text)
                try:
                    subprocess.run(["gcc", "-shared", "-o", "expression.dll", "expression.c"], check=True)
                    print("Compilation successful.")
                    example = ExampleDll(f"{pwd}\\expression.dll")
                    print("x min and max", x_min, x_max)
                    x = [(x / 999) * (x_max - x_min) + x_min for x in range(1000)]
                    y = [example.calculate_x(i) for i in x]
                    plt.plot(x, y)
                    plt.title("Graph")
                    plt.xlabel("Values of x")
                    plt.ylabel("Values of y")
                    plt.axhline(0, color='black', linewidth=0.5)
                    plt.axvline(0, color='black', linewidth=0.5)
                    plt.show()
                except Exception as e:
                    print("Exception:", e)
                    self.line_edit.clear()
                    self.line_edit.setText(choice(err_list))
            else:
                self.line_edit.setText("Input has to contain 'x' (ERR)") 
        else:
            self.line_edit.setText(self.line_edit.text() + label)

if __name__ == '__main__':
    app = QApplication([])
    window = CalculatorWindow()
    window.show()
    app.exec()