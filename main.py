import tkinter as tk
from tkinter import messagebox
import mysql.connector


class EmployeeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("员工信息管理系统")

        # 员工信息存储结构为字典，key为员工号，value是员工信息的字典
        self.employees = {}

        self.create_gui()

    def create_gui(self):
        # 创建标签和输入框
        self.label_employee_id = tk.Label(self.root, text="员工号：")
        self.label_employee_id.grid(row=0, column=0)
        self.entry_employee_id = tk.Entry(self.root)
        self.entry_employee_id.grid(row=0, column=1)

        self.label_employee_name = tk.Label(self.root, text="员工姓名：")
        self.label_employee_name.grid(row=1, column=0)
        self.entry_employee_name = tk.Entry(self.root)
        self.entry_employee_name.grid(row=1, column=1)

        self.label_department = tk.Label(self.root, text="所属部门：")
        self.label_department.grid(row=2, column=0)
        self.entry_department = tk.Entry(self.root)
        self.entry_department.grid(row=2, column=1)

        self.label_phone_number = tk.Label(self.root, text="电话号码：")
        self.label_phone_number.grid(row=3, column=0)
        self.entry_phone_number = tk.Entry(self.root)
        self.entry_phone_number.grid(row=3, column=1)

        # 创建按钮
        self.button_add_employee = tk.Button(self.root, text="添加员工", command=self.add_employee)
        self.button_add_employee.grid(row=4, column=0, columnspan=2)

        self.button_remove_employee = tk.Button(self.root, text="删除员工", command=self.remove_employee)
        self.button_remove_employee.grid(row=5, column=0, columnspan=2)

        self.button_find_employee = tk.Button(self.root, text="查找员工", command=self.find_employee)
        self.button_find_employee.grid(row=6, column=0, columnspan=2)

        self.button_display_department = tk.Button(self.root, text="浏览部门员工信息", command=self.display_department)
        self.button_display_department.grid(row=7, column=0, columnspan=2)

        self.button_count_employees = tk.Button(self.root, text="统计部门人数", command=self.count_employees)
        self.button_count_employees.grid(row=8, column=0, columnspan=2)

    def add_employee(self):
        employee_id = self.entry_employee_id.get()
        employee_name = self.entry_employee_name.get()
        department = self.entry_department.get()
        phone_number = self.entry_phone_number.get()

        if employee_id in self.employees:
            messagebox.showerror("错误", "员工号已存在")
        else:
            self.employees[employee_id] = {
                "员工姓名": employee_name,
                "所属部门": department,
                "电话号码": phone_number
            }
            messagebox.showinfo("成功", "员工添加成功")

    def remove_employee(self):
        employee_id = self.entry_employee_id.get()
        
        if employee_id in self.employees:
            del self.employees[employee_id]
            messagebox.showinfo("成功", "员工删除成功")
        else:
            messagebox.showerror("错误", "未找到该员工")

    def find_employee(self):
        employee_id = self.entry_employee_id.get()

        if employee_id in self.employees:
            employee_info = self.employees[employee_id]
            messagebox.showinfo("员工信息", f"员工信息：\n员工号: {employee_id}\n员工姓名: {employee_info['员工姓名']}\n所属部门: {employee_info['所属部门']}\n电话号码: {employee_info['电话号码']}")
        else:
            messagebox.showerror("错误", "未找到该员工")

    def display_department(self):
        department = self.entry_department.get()
        employees_in_department = [emp_info for emp_info in self.employees.values() if emp_info["所属部门"] == department]

        if employees_in_department:
            message = "部门员工信息：\n"
            for emp_info in employees_in_department:
                message += f"员工姓名: {emp_info['员工姓名']}, 电话号码: {emp_info['电话号码']}\n"
            messagebox.showinfo("部门员工信息", message)
        else:
            messagebox.showinfo("部门员工信息", "未找到在该部门的员工")
    def count_employees(self):
        department = self.entry_department.get()
        employees_in_department = [emp_info for emp_info in self.employees.values() if emp_info["所属部门"] == department]
        employee_count = len(employees_in_department)

        messagebox.showinfo("部门人数统计", f"部门 {department} 的人数为: {employee_count}")
    def save_to_mysql(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="your_username",
                password="your_password",
                database="employee_db"
            )
            cursor = connection.cursor()

            # 清空表
            cursor.execute("TRUNCATE TABLE employees")

            # 插入数据
            for employee_id, employee_info in self.employees.items():
                sql = "INSERT INTO employees (employee_id, employee_name, department, phone_number) VALUES (%s, %s, %s, %s)"
                val = (employee_id, employee_info["员工姓名"], employee_info["所属部门"], employee_info["电话号码"])
                cursor.execute(sql, val)

            connection.commit()
            messagebox.showinfo("成功", "员工信息保存到MySQL数据库成功")

        except mysql.connector.Error as error:
            messagebox.showerror("错误", f"保存到MySQL数据库时发生错误: {error}")

        finally:
            if 'connection' in locals():
                if connection.is_connected():
                    cursor.close()
                    connection.close()

    def load_from_mysql(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="your_username",
                password="your_password",
                database="employee_db"
            )
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM employees")
            rows = cursor.fetchall()
            for row in rows:
                self.employees[row[0]] = {
                    "员工姓名": row[1],
                    "所属部门": row[2],
                    "电话号码": row[3]
                }

        except mysql.connector.Error as error:
            messagebox.showerror("错误", f"从MySQL数据库加载数据时发生错误: {error}")

        finally:
            if 'connection' in locals():
                if connection.is_connected():
                    cursor.close()
                    connection.close()

# 创建GUI程序
root = tk.Tk()
app = EmployeeManagementSystem(root)
app.load_from_mysql()  # 在GUI启动时加载之前保存的员工信息
root.protocol("WM_DELETE_WINDOW", app.save_to_mysql)  # 在关闭GUI时保存员工信息到MySQL数据库
root.mainloop()