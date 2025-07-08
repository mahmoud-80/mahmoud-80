import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class BookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("نظام حجز مواعيد العاصمة الإدارية الجديدة")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Load or initialize user data
        self.users_file = "users.json"
        self.users = self.load_users()
        
        # Create main container
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Show welcome screen
        self.show_welcome_screen()
        
        # Service data
        self.services = {
            1: "اصدار رخصة مركبة اول مرة",
            2: "تجديد رخصة مركبة",
            3: "اصدار رخصة قيادة اول مرة",
            4: "تجديد رخصة قيادة",
            5: "اصدار بدل فاقد"
        }
        
        self.days = {
            1: ("الأحد", "13-04-2025", [4, 6, 7, 8, 11]),
            2: ("الاثنين", "14-04-2025", [2, 1, 8, 6, 4]),
            3: ("الثلاثاء", "15-04-2025", [3, 1, 6, 6, 4]),
            4: ("الأربعاء", "16-04-2025", [1, 6, 9, 8, 3]),
            5: ("الخميس", "17-04-2025", [4, 7, 7, 10, 1])
        }
        
        self.time_slots = ["9:00", "10:00", "11:00", "12:00", "13:00"]
        
        # Styling
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 12), padding=10)
        self.style.configure('TLabel', font=('Arial', 12))
        self.style.configure('TEntry', font=('Arial', 12), padding=5)
        
    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_users(self):
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)
    
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_welcome_screen(self):
        self.clear_frame()
        
        # Welcome label
        tk.Label(self.main_frame, text="مرحباً بكم في نظام حجز المواعيد", 
                font=('Arial', 16, 'bold')).pack(pady=20)
        
        # Buttons
        tk.Button(self.main_frame, text="تسجيل مستخدم جديد", font=('Arial', 14),
                 command=self.show_register_screen, width=20, bg='#4CAF50', fg='white').pack(pady=10)
        
        tk.Button(self.main_frame, text="تسجيل الدخول", font=('Arial', 14),
                 command=self.show_login_screen, width=20, bg='#2196F3', fg='white').pack(pady=10)
        
        tk.Button(self.main_frame, text="خروج", font=('Arial', 14),
                 command=self.root.quit, width=20, bg='#f44336', fg='white').pack(pady=10)
    
    def show_register_screen(self):
        self.clear_frame()
        
        # Title
        tk.Label(self.main_frame, text="تسجيل مستخدم جديد", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Back button
        tk.Button(self.main_frame, text="رجوع", command=self.show_welcome_screen).pack(anchor='w', padx=10)
        
        # Form frame
        form_frame = tk.Frame(self.main_frame)
        form_frame.pack(pady=20)
        
        # Username
        tk.Label(form_frame, text="اسم المستخدم:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.reg_username = tk.Entry(form_frame, font=('Arial', 12))
        self.reg_username.grid(row=0, column=1, padx=10, pady=10)
        
        # Password
        tk.Label(form_frame, text="كلمة المرور:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.reg_password = tk.Entry(form_frame, show="*", font=('Arial', 12))
        self.reg_password.grid(row=1, column=1, padx=10, pady=10)
        
        # Password hint
        hint = "يجب أن تحتوي كلمة المرور على:\n- 8 أحرف بالضبط\n- حروف كبيرة وصغيرة\n- لا تحتوي على أرقام أو رموز"
        tk.Label(form_frame, text=hint, justify='right').grid(row=2, column=0, columnspan=2, pady=10)
        
        # Confirm Password
        tk.Label(form_frame, text="تأكيد كلمة المرور:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.reg_confirm_password = tk.Entry(form_frame, show="*", font=('Arial', 12))
        self.reg_confirm_password.grid(row=3, column=1, padx=10, pady=10)
        
        # Register button
        tk.Button(self.main_frame, text="تسجيل", command=self.register_user, 
                 bg='#4CAF50', fg='white', font=('Arial', 12)).pack(pady=20)
    
    def is_strong_password(self, password):
        if len(password) != 8:
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        if any(not char.isalpha() for char in password):
            return False
        return True
    
    def register_user(self):
        username = self.reg_username.get()
        password = self.reg_password.get()
        confirm_password = self.reg_confirm_password.get()
        
        if not username or not password or not confirm_password:
            messagebox.showerror("خطأ", "يجب ملء جميع الحقول")
            return
        
        if username in self.users:
            messagebox.showerror("خطأ", "اسم المستخدم موجود بالفعل")
            return
        
        if not self.is_strong_password(password):
            messagebox.showerror("خطأ", "كلمة المرور ضعيفة. يجب أن تحتوي على 8 أحرف (حروف كبيرة وصغيرة فقط)")
            return
        
        if password != confirm_password:
            messagebox.showerror("خطأ", "كلمة المرور غير متطابقة")
            return
        
        self.users[username] = password
        self.save_users()
        messagebox.showinfo("نجاح", "تم التسجيل بنجاح")
        self.show_login_screen()
    
    def show_login_screen(self):
        self.clear_frame()
        
        # Title
        tk.Label(self.main_frame, text="تسجيل الدخول", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Back button
        tk.Button(self.main_frame, text="رجوع", command=self.show_welcome_screen).pack(anchor='w', padx=10)
        
        # Form frame
        form_frame = tk.Frame(self.main_frame)
        form_frame.pack(pady=20)
        
        # Username
        tk.Label(form_frame, text="اسم المستخدم:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.login_username = tk.Entry(form_frame, font=('Arial', 12))
        self.login_username.grid(row=0, column=1, padx=10, pady=10)
        
        # Password
        tk.Label(form_frame, text="كلمة المرور:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.login_password = tk.Entry(form_frame, show="*", font=('Arial', 12))
        self.login_password.grid(row=1, column=1, padx=10, pady=10)
        
        # Login button
        tk.Button(self.main_frame, text="دخول", command=self.login_user, 
                 bg='#2196F3', fg='white', font=('Arial', 12)).pack(pady=20)
    
    def login_user(self):
        username = self.login_username.get()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showerror("خطأ", "يجب إدخال اسم المستخدم وكلمة المرور")
            return
        
        if username not in self.users or self.users[username] != password:
            messagebox.showerror("خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة")
            return
        
        self.current_user = username
        messagebox.showinfo("نجاح", f"مرحباً بك {username}!")
        self.show_services_screen()
    
    def show_services_screen(self):
        self.clear_frame()
        
        # Title
        tk.Label(self.main_frame, text=f"مرحباً بك {self.current_user}", 
                font=('Arial', 16, 'bold')).pack(pady=10)
        
        tk.Label(self.main_frame, text="الخدمات المتاحة:", 
                font=('Arial', 14)).pack(pady=10)
        
        # Back button
        tk.Button(self.main_frame, text="تسجيل الخروج", command=self.show_welcome_screen).pack(anchor='w', padx=10)
        
        # Services buttons
        for num, service in self.services.items():
            tk.Button(self.main_frame, text=f"{num}. {service}", 
                     command=lambda n=num: self.select_service(n),
                     font=('Arial', 12), width=40).pack(pady=5)
    
    def select_service(self, service_num):
        self.selected_service = service_num
        self.show_days_screen()
    
    def show_days_screen(self):
        self.clear_frame()
        
        # Title
        tk.Label(self.main_frame, text=f"الخدمة: {self.services[self.selected_service]}", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        tk.Label(self.main_frame, text="اختر اليوم:", 
                font=('Arial', 14)).pack(pady=10)
        
        # Back button
        tk.Button(self.main_frame, text="رجوع", command=self.show_services_screen).pack(anchor='w', padx=10)
        
        # Days buttons
        for num, (day, date, _) in self.days.items():
            tk.Button(self.main_frame, text=f"{num}. {day} - {date}", 
                     command=lambda n=num: self.select_day(n),
                     font=('Arial', 12), width=40).pack(pady=5)
    
    def select_day(self, day_num):
        self.selected_day = day_num
        day_name, date, slots = self.days[day_num]
        
        # Check if any slots available
        available_slots = []
        for i, (time, bookings) in enumerate(zip(self.time_slots, slots)):
            if bookings < 10:
                available_slots.append((i+1, time, 10-bookings))
        
        if not available_slots:
            messagebox.showinfo("لا يوجد مواعيد", "لا توجد مواعيد متاحة في هذا اليوم")
            return
        
        self.show_slots_screen(available_slots, day_name, date)
    
    def show_slots_screen(self, available_slots, day_name, date):
        self.clear_frame()
        
        # Title
        tk.Label(self.main_frame, 
                text=f"الخدمة: {self.services[self.selected_service]}\nاليوم: {day_name} - {date}", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        tk.Label(self.main_frame, text="المواعيد المتاحة:", 
                font=('Arial', 14)).pack(pady=10)
        
        # Back button
        tk.Button(self.main_frame, text="رجوع", command=self.show_days_screen).pack(anchor='w', padx=10)
        
        # Slots buttons
        for slot in available_slots:
            tk.Button(self.main_frame, 
                     text=f"{slot[0]}. الساعة {slot[1]} - {slot[2]} مواعيد متبقية", 
                     command=lambda s=slot: self.select_slot(s, day_name, date),
                     font=('Arial', 12), width=40).pack(pady=5)
    
    def select_slot(self, slot, day_name, date):
        self.selected_slot = slot
        self.show_personal_info_screen(day_name, date)
    
    def show_personal_info_screen(self, day_name, date):
        self.clear_frame()
        
        # Title
        tk.Label(self.main_frame, 
                text=f"الخدمة: {self.services[self.selected_service]}\nاليوم: {day_name} - {date}\nالموعد: الساعة {self.selected_slot[1]}", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        tk.Label(self.main_frame, text="البيانات الشخصية:", 
                font=('Arial', 14)).pack(pady=10)
        
        # Back button
        tk.Button(self.main_frame, text="رجوع", command=lambda: self.show_slots_screen(
            [self.selected_slot], day_name, date)).pack(anchor='w', padx=10)
        
        # Form frame
        form_frame = tk.Frame(self.main_frame)
        form_frame.pack(pady=20)
        
        # Full Name
        tk.Label(form_frame, text="الاسم بالكامل:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.full_name = tk.Entry(form_frame, font=('Arial', 12))
        self.full_name.grid(row=0, column=1, padx=10, pady=10)
        
        # ID Number
        tk.Label(form_frame, text="رقم الهوية:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.id_number = tk.Entry(form_frame, font=('Arial', 12))
        self.id_number.grid(row=1, column=1, padx=10, pady=10)
        
        # Confirm button
        tk.Button(self.main_frame, text="تأكيد الحجز", command=self.confirm_booking, 
                 bg='#4CAF50', fg='white', font=('Arial', 12)).pack(pady=20)
    
    def confirm_booking(self):
        full_name = self.full_name.get()
        id_number = self.id_number.get()
        
        if not full_name or not id_number:
            messagebox.showerror("خطأ", "يجب إدخال الاسم الكامل ورقم الهوية")
            return
        
        day_name, date, _ = self.days[self.selected_day]
        slot_time = self.selected_slot[1]
        service = self.services[self.selected_service]
        
        # Create booking confirmation message
        confirmation = f"""
        تم تأكيد الحجز بنجاح!
        
        التفاصيل:
        الاسم: {full_name}
        رقم الهوية: {id_number}
        الخدمة: {service}
        التاريخ: {date} ({day_name})
        الموعد: الساعة {slot_time}
        
        شكراً لاستخدامكم نظام حجز المواعيد
        """
        
        messagebox.showinfo("تم الحجز", confirmation)
        
        # Here you would normally save the booking to a database
        # For now, we'll just return to the services screen
        self.show_services_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = BookingSystem(root)
    root.mainloop()