import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from student import Student
from storage import load_data, save_data
from results import calculate_total_and_average, assign_grade
from reports import generate_class_statistics, generate_text_report

class StudentResultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("900x650")
        self.root.configure(bg="#f4f6f9")

        # Load existing data
        self.students = load_data()

        # Build Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tabs setup
        self.tab_view = ttk.Frame(self.notebook)
        self.tab_add = ttk.Frame(self.notebook)
        self.tab_scores = ttk.Frame(self.notebook)
        self.tab_reports = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_view, text=" View & Search Students ")
        self.notebook.add(self.tab_add, text=" Add / Edit Student ")
        self.notebook.add(self.tab_scores, text=" Record Scores ")
        self.notebook.add(self.tab_reports, text=" Reports & Statistics ")

        self.setup_view_tab()
        self.setup_add_tab()
        self.setup_scores_tab()
        self.setup_reports_tab()

    # --- TAB 1: VIEW & SEARCH STUDENTS ---
    def setup_view_tab(self):
        frame_top = ttk.Frame(self.tab_view)
        frame_top.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(frame_top, text="Search (ID/Name):").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(frame_top, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(frame_top, text="Search", command=self.search_students).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_top, text="Reset List", command=self.refresh_student_table).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_top, text="Delete Selected", command=self.delete_student).pack(side=tk.RIGHT, padx=5)

        # Treeview (Table)
        columns = ("id", "name", "class", "gender", "dob", "total", "average", "grade")
        self.tree = ttk.Treeview(self.tab_view, columns=columns, show="headings")
        
        self.tree.heading("id", text="Student ID")
        self.tree.heading("name", text="Full Name")
        self.tree.heading("class", text="Class")
        self.tree.heading("gender", text="Gender")
        self.tree.heading("dob", text="DOB")
        self.tree.heading("total", text="Total Score")
        self.tree.heading("average", text="Average")
        self.tree.heading("grade", text="Grade")

        for col in columns:
            self.tree.column(col, width=100, anchor=tk.CENTER)
        self.tree.column("name", width=180, anchor=tk.W)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.refresh_student_table()

    def refresh_student_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for s in self.students.values():
            total, avg = calculate_total_and_average(s.scores)
            grade = assign_grade(avg) if s.scores else "N/A"
            self.tree.insert("", tk.END, values=(s.student_id, s.full_name, s.student_class, s.gender, s.dob, total, avg, grade))

    def search_students(self):
        query = self.search_var.get().strip().lower()
        if not query:
            return self.refresh_student_table()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for s in self.students.values():
            if query in s.student_id.lower() or query in s.full_name.lower():
                total, avg = calculate_total_and_average(s.scores)
                grade = assign_grade(avg) if s.scores else "N/A"
                self.tree.insert("", tk.END, values=(s.student_id, s.full_name, s.student_class, s.gender, s.dob, total, avg, grade))

    def delete_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a student from the table to delete.")
            return
        student_id = self.tree.item(selected_item[0])['values'][0]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student {student_id}?"):
            del self.students[str(student_id)]
            save_data(self.students)
            self.refresh_student_table()
            messagebox.showinfo("Success", "Student record deleted successfully.")

    # --- TAB 2: ADD / EDIT STUDENT ---
    def setup_add_tab(self):
        form_frame = ttk.LabelFrame(self.tab_add, text="Student Details")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        labels = ["Student ID:", "Full Name:", "Class / Form:", "Gender:", "Date of Birth (YYYY-MM-DD):"]
        self.entries = {}

        for i, text in enumerate(labels):
            lbl = ttk.Label(form_frame, text=text)
            lbl.grid(row=i, column=0, sticky=tk.W, padx=15, pady=10)
            entry = ttk.Entry(form_frame, width=35)
            entry.grid(row=i, column=1, padx=15, pady=10)
            self.entries[text] = entry

        btn_save = ttk.Button(form_frame, text="Save Student", command=self.save_student_form)
        btn_save.grid(row=5, column=1, sticky=tk.E, padx=15, pady=20)

    def save_student_form(self):
        sid = self.entries["Student ID:"].get().strip()
        name = self.entries["Full Name:"].get().strip()
        s_class = self.entries["Class / Form:"].get().strip()
        gender = self.entries["Gender:"].get().strip()
        dob = self.entries["Date of Birth (YYYY-MM-DD):"].get().strip()

        if not sid or not name:
            messagebox.showwarning("Validation Error", "Student ID and Full Name are required.")
            return

        if sid in self.students:
            # Update existing
            s = self.students[sid]
            s.update_info(name, s_class, gender, dob)
            messagebox.showinfo("Success", f"Updated info for {name}.")
        else:
            # Add new
            self.students[sid] = Student(sid, name, s_class, gender, dob)
            messagebox.showinfo("Success", f"Student {name} registered!")

        save_data(self.students)
        self.refresh_student_table()

        for entry in self.entries.values():
            entry.delete(0, tk.END)

    # --- TAB 3: RECORD SCORES ---
    def setup_scores_tab(self):
        top_frame = ttk.Frame(self.tab_scores)
        top_frame.pack(fill=tk.X, padx=15, pady=15)

        ttk.Label(top_frame, text="Select Student ID:").pack(side=tk.LEFT, padx=5)
        self.score_sid_var = tk.StringVar()
        self.score_student_cb = ttk.Combobox(top_frame, textvariable=self.score_sid_var)
        self.score_student_cb.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(top_frame, text="Load Scores", command=self.load_student_scores).pack(side=tk.LEFT, padx=5)

        self.score_entries_frame = ttk.LabelFrame(self.tab_scores, text="Subject Scores (Minimum 5)")
        self.score_entries_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.subject_fields = []
        for i in range(5):
            lbl_subj = ttk.Label(self.score_entries_frame, text=f"Subject {i+1} Name:")
            lbl_subj.grid(row=i, column=0, padx=10, pady=5)
            ent_subj = ttk.Entry(self.score_entries_frame)
            ent_subj.grid(row=i, column=1, padx=10, pady=5)

            lbl_val = ttk.Label(self.score_entries_frame, text="Score (0-100):")
            lbl_val.grid(row=i, column=2, padx=10, pady=5)
            ent_val = ttk.Entry(self.score_entries_frame)
            ent_val.grid(row=i, column=3, padx=10, pady=5)

            self.subject_fields.append((ent_subj, ent_val))

        ttk.Button(self.tab_scores, text="Save Scores", command=self.save_scores).pack(anchor=tk.E, padx=20, pady=10)

    def load_student_scores(self):
        self.score_student_cb['values'] = list(self.students.keys())
        sid = self.score_sid_var.get().strip()
        if sid not in self.students:
            messagebox.showerror("Error", "Select a valid Student ID.")
            return
        
        s = self.students[sid]
        scores_items = list(s.scores.items())
        
        for i in range(5):
            self.subject_fields[i][0].delete(0, tk.END)
            self.subject_fields[i][1].delete(0, tk.END)
            if i < len(scores_items):
                self.subject_fields[i][0].insert(0, scores_items[i][0])
                self.subject_fields[i][1].insert(0, str(scores_items[i][1]))

    def save_scores(self):
        sid = self.score_sid_var.get().strip()
        if sid not in self.students:
            messagebox.showerror("Error", "Select a valid Student ID first.")
            return

        s = self.students[sid]
        new_scores = {}
        for ent_subj, ent_val in self.subject_fields:
            subj = ent_subj.get().strip()
            val_str = ent_val.get().strip()
            if subj and val_str:
                try:
                    val = float(val_str)
                    if 0 <= val <= 100:
                        new_scores[subj] = val
                    else:
                        messagebox.showwarning("Invalid Score", f"Score for {subj} must be 0-100.")
                        return
                except ValueError:
                    messagebox.showerror("Format Error", f"Score for {subj} must be a number.")
                    return

        s.scores = new_scores
        save_data(self.students)
        self.refresh_student_table()
        messagebox.showinfo("Success", f"Scores saved for {s.full_name}!")

    # --- TAB 4: REPORTS & STATISTICS ---
    def setup_reports_tab(self):
        top_frame = ttk.Frame(self.tab_reports)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(top_frame, text="Refresh Statistics", command=self.update_reports_view).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Export Text Report to File", command=self.export_report).pack(side=tk.LEFT, padx=5)

        self.report_text = tk.Text(self.tab_reports, wrap=tk.WORD, font=("Courier", 10))
        self.report_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.update_reports_view()

    def update_reports_view(self):
        content = generate_text_report(self.students, filename="temp_report.txt")
        self.report_text.delete("1.0", tk.END)
        self.report_text.insert(tk.END, content)

    def export_report(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            generate_text_report(self.students, filename=file_path)
            messagebox.showinfo("Export Successful", f"Report saved to:\n{file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentResultApp(root)
    root.mainloop()