import tkinter as tk
from tkinter import ttk, messagebox

class HospitalSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("نظام المستشفى")
        self.root.geometry("800x600")
        self.root.configure(bg="#e6f2ff")

        self.patients = []
        self.doctors = []
        self.appointments = []
        self.pharmacy = [
            "باراسيتامول", "أوغمنتين", "بانادول", "أموكسيسيلين", "فيتامين سي",
            "زيثروماكس", "ميتفورمين", "ديكلوفيناك", "ابروفين", "أوميبرازول",
            "لورين", "كيتوفان", "فلاجيل", "توبرادكس", "سيتال",
            "كلاريتين", "نيوروتون", "هيستازين", "سيترو" ,"دافلون"
        ]

        self.disease_specialty = {
            "أسنان": "طبيب أسنان",
            "عيون": "طبيب عيون",
            "قلب": "طبيب قلب",
            "أطفال": "طبيب أطفال",
            "جلدية": "طبيب جلدية"
        }

        self.setup_ui()

    def setup_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True)

        self.create_patients_tab(notebook)
        self.create_doctors_tab(notebook)
        self.create_appointments_tab(notebook)
        self.create_pharmacy_tab(notebook)

    def create_patients_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="المرضى")

        self.entry_name = ttk.Entry(tab, width=30)
        self.combo_gender = ttk.Combobox(tab, values=["ذكر", "أنثى"], state="readonly", width=28)
        self.entry_age = ttk.Entry(tab, width=30)
        self.combo_disease = ttk.Combobox(tab, values=list(self.disease_specialty.keys()), state="readonly", width=28)

        ttk.Label(tab, text="الاسم:").grid(row=0, column=0, pady=5, padx=5, sticky='w')
        self.entry_name.grid(row=0, column=1, pady=5)
        ttk.Label(tab, text="النوع:").grid(row=1, column=0, pady=5, padx=5, sticky='w')
        self.combo_gender.grid(row=1, column=1, pady=5)
        ttk.Label(tab, text="العمر:").grid(row=2, column=0, pady=5, padx=5, sticky='w')
        self.entry_age.grid(row=2, column=1, pady=5)
        ttk.Label(tab, text="نوع المرض:").grid(row=3, column=0, pady=5, padx=5, sticky='w')
        self.combo_disease.grid(row=3, column=1, pady=5)

        ttk.Button(tab, text="إضافة", command=self.add_patient).grid(row=4, column=0, pady=10)
        ttk.Button(tab, text="تحديث المدخلات", command=self.clear_patient_inputs).grid(row=4, column=1, pady=10)

        self.patient_list = tk.Text(tab, height=10, width=70)
        self.patient_list.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def add_patient(self):
        name = self.entry_name.get()
        gender = self.combo_gender.get()
        age = self.entry_age.get()
        disease = self.combo_disease.get()
        if name and gender and age.isdigit() and disease:
            self.patients.append((name, gender, age, disease))
            self.display_patients()
            self.clear_patient_inputs()

    def clear_patient_inputs(self):
        self.entry_name.delete(0, tk.END)
        self.combo_gender.set("")
        self.entry_age.delete(0, tk.END)
        self.combo_disease.set("")

    def display_patients(self):
        self.patient_list.delete("1.0", tk.END)
        for p in self.patients:
            self.patient_list.insert(tk.END, f"{p[0]} - {p[1]} - {p[2]} سنة - {p[3]}\n")

    def create_doctors_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="الأطباء")

        self.entry_doc_name = ttk.Entry(tab, width=30)
        self.entry_specialty = ttk.Entry(tab, width=30)
        self.entry_phone = ttk.Entry(tab, width=30)

        ttk.Label(tab, text="اسم الطبيب:").grid(row=0, column=0, pady=5, padx=5, sticky='w')
        self.entry_doc_name.grid(row=0, column=1, pady=5)
        ttk.Label(tab, text="التخصص:").grid(row=1, column=0, pady=5, padx=5, sticky='w')
        self.entry_specialty.grid(row=1, column=1, pady=5)
        ttk.Label(tab, text="رقم الهاتف:").grid(row=2, column=0, pady=5, padx=5, sticky='w')
        self.entry_phone.grid(row=2, column=1, pady=5)

        ttk.Button(tab, text="إضافة", command=self.add_doctor).grid(row=3, column=0, pady=10)
        ttk.Button(tab, text="تحديث المدخلات", command=self.clear_doctor_inputs).grid(row=3, column=1, pady=10)

        self.doctor_list = tk.Text(tab, height=10, width=70)
        self.doctor_list.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def add_doctor(self):
        name = self.entry_doc_name.get()
        specialty = self.entry_specialty.get()
        phone = self.entry_phone.get()
        if name and specialty and phone:
            self.doctors.append((name, specialty, phone))
            self.display_doctors()
            self.clear_doctor_inputs()

    def clear_doctor_inputs(self):
        self.entry_doc_name.delete(0, tk.END)
        self.entry_specialty.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)

    def display_doctors(self):
        self.doctor_list.delete("1.0", tk.END)
        for d in self.doctors:
            self.doctor_list.insert(tk.END, f"{d[0]} - {d[1]} - {d[2]}\n")

    def create_appointments_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="المواعيد")

        self.combo_patient = ttk.Combobox(tab, values=[], width=28)
        self.combo_disease_appointment = ttk.Combobox(tab, values=list(self.disease_specialty.keys()), state="readonly", width=28)
        self.label_result = ttk.Label(tab, text="")

        ttk.Label(tab, text="اختر المريض:").grid(row=0, column=0, pady=5, padx=5)
        self.combo_patient.grid(row=0, column=1, pady=5)
        ttk.Label(tab, text="نوع المرض:").grid(row=1, column=0, pady=5, padx=5)
        self.combo_disease_appointment.grid(row=1, column=1, pady=5)

        ttk.Button(tab, text="حجز الموعد", command=self.book_appointment).grid(row=2, column=0, pady=10)
        ttk.Button(tab, text="تحديث المدخلات", command=self.clear_appointment_inputs).grid(row=2, column=1, pady=10)

        self.label_result.grid(row=3, column=0, columnspan=2)

    def book_appointment(self):
        patient = self.combo_patient.get()
        disease = self.combo_disease_appointment.get()
        if patient and disease:
            specialty = self.disease_specialty.get(disease, "غير معروف")
            doctor = next((d[0] for d in self.doctors if d[1] == specialty), "لا يوجد طبيب متاح")
            self.label_result.config(text=f"الموعد: {patient} مع {doctor} ({specialty})")

    def clear_appointment_inputs(self):
        self.combo_patient.set("")
        self.combo_disease_appointment.set("")
        self.label_result.config(text="")
        self.combo_patient['values'] = [p[0] for p in self.patients]

    def create_pharmacy_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="الصيدلية")

        self.entry_med = ttk.Entry(tab, width=30)
        ttk.Label(tab, text="اسم الدواء:").grid(row=0, column=0, pady=5, padx=5)
        self.entry_med.grid(row=0, column=1, pady=5)

        ttk.Button(tab, text="إضافة", command=self.add_medicine).grid(row=1, column=0, pady=10)
        ttk.Button(tab, text="حذف", command=self.remove_medicine).grid(row=1, column=1, pady=10)
        ttk.Button(tab, text="تحديث المدخلات", command=self.clear_pharmacy_inputs).grid(row=1, column=2, pady=10)

        self.med_list = tk.Text(tab, height=15, width=70)
        self.med_list.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        self.display_medicines()

    def add_medicine(self):
        med = self.entry_med.get()
        if med:
            self.pharmacy.append(med)
            self.display_medicines()
            self.entry_med.delete(0, tk.END)

    def remove_medicine(self):
        med = self.entry_med.get()
        if med in self.pharmacy:
            self.pharmacy.remove(med)
            self.display_medicines()
            self.entry_med.delete(0, tk.END)

    def clear_pharmacy_inputs(self):
        self.entry_med.delete(0, tk.END)

    def display_medicines(self):
        self.med_list.delete("1.0", tk.END)
        for med in self.pharmacy:
            self.med_list.insert(tk.END, f"{med}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalSystem(root)
    root.mainloop()
