import sys
import psycopg2
from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QPushButton, QApplication, QDialog, QLineEdit, QComboBox, QMessageBox
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt
def connect_db():
    return psycopg2.connect(
        dbname="exm",
        user="postgres",  
        password="2791",  
        host="localhost",
        port="5432"
    )

class add_user(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("добавить сотрудника")
        self.setWindowIcon(QIcon("icon.png")) 
        self.setFixedSize(300, 300)
        
        self.layout = QVBoxLayout()
        self.name = QLabel("Введите имя:")
        self.layout.addWidget(self.name)
        
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_input)
        
        self.lastname = QLabel("Введите фамилию:")
        self.layout.addWidget(self.lastname)
        
        self.lastname_input = QLineEdit()
        self.layout.addWidget(self.lastname_input)
        
        self.company = QLabel("Выберите компанию:")
        self.layout.addWidget(self.company)
        
        self.company_combo = QComboBox()
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("SELECT company_id, company_name FROM companies")
            companies = cur.fetchall()
            for comp in companies:
                self.company_combo.addItem(comp[1], comp[0])
        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить компании: {str(e)}")
        finally:
            cur.close()
            conn.close()
        self.layout.addWidget(self.company_combo)
        
        self.position = QLabel("Выберите должность:")
        self.layout.addWidget(self.position)
        
        self.position_combo = QComboBox()
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("SELECT position_id, position_name FROM positions")
            positions = cur.fetchall()
            for pos in positions:
                self.position_combo.addItem(pos[1], pos[0])
        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить должности: {str(e)}")
        finally:
            cur.close()
            conn.close()
        self.layout.addWidget(self.position_combo)
        
        self.add_bat = QPushButton("ДОБАВИТЬ")
        self.layout.addWidget(self.add_bat)
        self.back_bat = QPushButton("НАЗАД")
        self.layout.addWidget(self.back_bat)
        
        self.add_bat.clicked.connect(self.add_employee)
        self.back_bat.clicked.connect(self.reject)
        self.setLayout(self.layout)
        
    def add_employee(self):
        name = self.name_input.text()
        lastname = self.lastname_input.text()
        company_id = self.company_combo.currentData()
        position_id = self.position_combo.currentData()
        if not (name and lastname and company_id and position_id):
            QMessageBox.warning(self, "Предупреждение", "Все поля должны быть заполнены!")
            return
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO employees (first_name, last_name, company_id, position_id) VALUES (%s, %s, %s, %s)",
                        (name, lastname, company_id, position_id))
            conn.commit()
            QMessageBox.information(self, "Успех", "Сотрудник успешно добавлен!")
            self.accept()
        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить сотрудника: {str(e)}\nПроверьте подключение к базе данных или введённые данные.")
        finally:
            cur.close()
            conn.close()

class upd_user(QDialog):
    def __init__(self, emp_id, name, lastname, company, position):
        super().__init__()
        
        self.emp_id = emp_id
        self.setWindowTitle("редактировать сотрудника")
        self.setWindowIcon(QIcon("icon.png"))  
        self.setFixedSize(300, 300)
        self.layout = QVBoxLayout()
        
        self.name = QLabel("Имя:")
        self.layout.addWidget(self.name)
        self.name_inp = QLineEdit(name)
        self.layout.addWidget(self.name_inp)
        
        self.lastname = QLabel("Фамилия:")
        self.layout.addWidget(self.lastname)
        self.lastname_inp = QLineEdit(lastname)
        self.layout.addWidget(self.lastname_inp)
        
        self.company = QLabel("Компания:")
        self.layout.addWidget(self.company)
        self.company_combo = QComboBox()
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("SELECT company_id, company_name FROM companies")
            companies = cur.fetchall()
            for comp in companies:
                self.company_combo.addItem(comp[1], comp[0])
            self.company_combo.setCurrentText(company)
        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить компании: {str(e)}")
        finally:
            cur.close()
            conn.close()
        self.layout.addWidget(self.company_combo)
        
        self.position = QLabel("Должность:")
        self.layout.addWidget(self.position)
        self.position_combo = QComboBox()
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("SELECT position_id, position_name FROM positions")
            positions = cur.fetchall()
            for pos in positions:
                self.position_combo.addItem(pos[1], pos[0])
            self.position_combo.setCurrentText(position)
        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить должности: {str(e)}")
        finally:
            cur.close()
            conn.close()
        self.layout.addWidget(self.position_combo)
        
        self.upd_bat = QPushButton("ОБНОВИТЬ")
        self.layout.addWidget(self.upd_bat)
        self.back_bat = QPushButton("НАЗАД")
        self.layout.addWidget(self.back_bat)
        
        self.upd_bat.clicked.connect(self.upd_employee)
        self.back_bat.clicked.connect(self.reject)
        self.setLayout(self.layout)
        
    def upd_employee(self):
        new_name = self.name_inp.text()
        new_lastname = self.lastname_inp.text()
        new_company_id = self.company_combo.currentData()
        new_position_id = self.position_combo.currentData()
        if not (new_name and new_lastname and new_company_id and new_position_id):
            QMessageBox.warning(self, "Предупреждение", "Все поля должны быть заполнены!")
            return
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE employees SET first_name=%s, last_name=%s, company_id=%s, position_id=%s WHERE employee_id=%s",
                        (new_name, new_lastname, new_company_id, new_position_id, self.emp_id))
            conn.commit()
            QMessageBox.information(self, "Успех", "Данные сотрудника успешно обновлены!")
            self.accept()
        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить данные сотрудника: {str(e)}\nПроверьте подключение к базе данных или введённые данные.")
        finally:
            cur.close()
            conn.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("управление сотрудниками")
        self.setWindowIcon(QIcon("icon.png"))  
        self.resize(500, 500)
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        layout = QVBoxLayout(self.widget)
        
        # Добавление логотипа
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("logo.png").scaled(100, 100, Qt.KeepAspectRatio))
        self.logo.setAlignment(Qt.AlignCenter)  # Центрирование логотипа
        layout.addWidget(self.logo)
        
        self.search_lab = QLabel("поиск:")
        layout.addWidget(self.search_lab)
        self.search_inp = QLineEdit()
        self.search_inp.setPlaceholderText("введите имя, фамилию, компанию или должность")
        layout.addWidget(self.search_inp)
        self.search_bat = QPushButton("НАЙТИ")
        layout.addWidget(self.search_bat)
        
        self.tabl = QTableWidget()
        self.tabl.setColumnCount(5)
        self.tabl.setHorizontalHeaderLabels(["id", "имя", "фамилия", "компания", "должность"])
        layout.addWidget(self.tabl)
        
        buttons_layout = QHBoxLayout()
        self.add_bat = QPushButton("ДОБАВИТЬ")
        self.upd_bat = QPushButton("РЕДАКТИРОВАТЬ")
        self.del_bat = QPushButton("УДАЛИТЬ")
        
        buttons_layout.addWidget(self.add_bat)
        buttons_layout.addWidget(self.upd_bat)
        buttons_layout.addWidget(self.del_bat)
        layout.addLayout(buttons_layout)
        
        self.load_dan()
        self.add_bat.clicked.connect(self.open_add_user)
        self.upd_bat.clicked.connect(self.upd_user)
        self.del_bat.clicked.connect(self.del_user)
        self.search_bat.clicked.connect(self.search_dan)
        
    def open_add_user(self):
        dialog = add_user()
        if dialog.exec() == QDialog.Accepted:
            self.load_dan()
    
    def load_dan(self):
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT e.employee_id, e.first_name, e.last_name, c.company_name, p.position_name
                FROM employees e
                JOIN companies c ON e.company_id = c.company_id
                JOIN positions p ON e.position_id = p.position_id
            """)
            data = cur.fetchall()
            self.tabl.setRowCount(len(data))
            for row_id, rows in enumerate(data):
                for col_id, value in enumerate(rows):
                    self.tabl.setItem(row_id, col_id, QTableWidgetItem(str(value)))
        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {str(e)}\nПроверьте подключение к базе данных.")
        finally:
            cur.close()
            conn.close()
    
    def del_user(self):
        sel_row = self.tabl.currentRow()
        if sel_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите сотрудника для удаления!")
            return
        reply = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите удалить сотрудника?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            emp_id = self.tabl.item(sel_row, 0).text()
            conn = connect_db()
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM employees WHERE employee_id = %s", (emp_id,))
                conn.commit()
                QMessageBox.information(self, "Успех", "Сотрудник успешно удалён!")
                self.load_dan()
            except psycopg2.Error as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить сотрудника: {str(e)}\nПроверьте подключение к базе данных.")
            finally:
                cur.close()
                conn.close()
    
    def upd_user(self):
        sel_row = self.tabl.currentRow()
        if sel_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите сотрудника для редактирования!")
            return
        emp_id = self.tabl.item(sel_row, 0).text()
        name = self.tabl.item(sel_row, 1).text()
        lastname = self.tabl.item(sel_row, 2).text()
        company = self.tabl.item(sel_row, 3).text()
        position = self.tabl.item(sel_row, 4).text()
        dialog = upd_user(emp_id, name, lastname, company, position)
        if dialog.exec() == QDialog.Accepted:
            self.load_dan()
    
    def search_dan(self):
        keyword = self.search_inp.text()
        if not keyword:
            self.load_dan()
            return
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT e.employee_id, e.first_name, e.last_name, c.company_name, p.position_name
                FROM employees e
                JOIN companies c ON e.company_id = c.company_id
                JOIN positions p ON e.position_id = p.position_id
                WHERE e.first_name ILIKE %s OR e.last_name ILIKE %s OR c.company_name ILIKE %s OR p.position_name ILIKE %s
            """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
            data = cur.fetchall()
            self.tabl.setRowCount(len(data))
            for row_id, rows in enumerate(data):
                for col_id, value in enumerate(rows):
                    self.tabl.setItem(row_id, col_id, QTableWidgetItem(str(value)))
        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить поиск: {str(e)}\nПроверьте подключение к базе данных.")
        finally:
            cur.close()
            conn.close()

app = QApplication([])
window = MainWindow()
window.show()
app.exec()