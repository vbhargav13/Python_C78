# Student Progress Tracker — Lessons 13–23 (All-in-One File)
# -----------------------------------------------------------------------------
# This single file intentionally contains:
# 1) A fully functional Tkinter GUI capstone app that gradually incorporates
#    features mapped to Lessons 13–23.
# 2) Clearly separated "Additional Activity" mini-programs/functions for each lesson.
# 3) A simple Console (CLI) mode (Lesson 23 homework) that supports CRUD, Search,
#    Topper, CSV Save/Load, and TXT report generation.
#
#
# PEDAGOGICAL STRUCTURE
# ---------------------
# Each section below starts with a big banner like:
#    ===== Lesson 13 =====
# and includes comments showing which parts of the code satisfy the curriculum.
#
# This file is designed so that the *same* domain model and logic are reused across
# GUI and CLI modes to reinforce software design concepts.
# -----------------------------------------------------------------------------

import csv
import sys
import argparse
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from dataclasses import dataclass, field, asdict
from typing import List, Optional


# =============================================================================
# ===== Lesson 13: Domain Model (dataclass), totals/averages, grade method =====
# =============================================================================
# - Define Student dataclass with attributes: roll, name, marks (3 subjects).
# - Methods: total(), average(), grade().
# - This is the foundation for all subsequent lessons.
@dataclass
class Student:
    roll: str
    name: str
    marks: List[int] = field(default_factory=lambda: [0, 0, 0])

    def total(self) -> int:
        return sum(self.marks)

    def average(self) -> float:
        return round(self.total() / len(self.marks), 2) if self.marks else 0.0

    def grade(self) -> str:
        avg = self.average()
        if avg >= 90:
            return "A+"
        elif avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 50:
            return "D"
        else:
            return "F"


# =============================================================================
# ===== Lesson 14: Tkinter Basics (main window, labels, entries, submit) =======
# =============================================================================
# This GUI scaffolding grows over lessons. By Lesson 23 it becomes the full app.
PALETTE = {
    "bg": "#F7FAFC",
    "header_start": "#7F7FD5",
    "header_mid":   "#86A8E7",
    "header_end":   "#91EAE4",
    "accent": "#2563EB",
    "success": "#16A34A",
    "warn": "#F59E0B",
    "danger": "#DC2626",
    "muted": "#64748B",
    "card": "#FFFFFF",
    "border": "#E5E7EB",
}

GRADE_TAGS = {
    "A+": ("#065F46", "#D1FAE5"),
    "A":  ("#065F46", "#D1FAE5"),
    "B":  ("#1E40AF", "#DBEAFE"),
    "C":  ("#92400E", "#FEF3C7"),
    "D":  ("#92400E", "#FEF3C7"),
    "F":  ("#7F1D1D", "#FEE2E2"),
}


def grade_to_tag(grade: str) -> str:
    return grade  # We use grade text as the Treeview tag


class StudentPerformanceApp(tk.Tk):
    """
    ===== Lessons 14–23: Tkinter App that evolves =====
    L14: Create window, title/size, labels/entries for roll/name/marks, Submit.
    L15: Use StringVar/Entry, validate marks, show error popups.
    L16: Add Treeview table: roll, name, marks, total, average, grade. Color rows.
    L17: Add CRUD buttons (Add/Update, Delete), Clear inputs.
    L18: Add Search (by roll or name) and highlight results.
    L19: Add Topper (popup), small confetti window.
    L20: Save/Load CSV with robust error handling.
    L21: Export per-student TXT report with grade & remarks.
    L22: Polish UI (styles, badges, header gradient).
    L23: Final integration, Reset All.
    """
    def __init__(self):
        super().__init__()
        self.title("Student Performance Tracker — L14–L23")
        self.geometry("1100x650")
        self.minsize(1024, 620)
        self.configure(bg=PALETTE["bg"])

        # Data store for GUI mode
        self.students: List[Student] = []

        # Build the interface (Lessons 14, 16, 22)
        self._build_styles()          # L22
        self._build_header()          # L22
        self._build_body()            # L14 + L16 core widgets
        self._bind_events()

    # ------------------- Styling / Header (L22) -------------------
    def _build_styles(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("TFrame", background=PALETTE["bg"])
        style.configure("Card.TFrame", background=PALETTE["card"], relief="groove")
        style.configure("TLabel", background=PALETTE["bg"], foreground="#111827", font=("Segoe UI", 10))
        style.configure("Header.TLabel", background=PALETTE["bg"], foreground="#111827", font=("Segoe UI", 14, "bold"))
        style.configure("Muted.TLabel", background=PALETTE["bg"], foreground=PALETTE["muted"], font=("Segoe UI", 10, "italic"))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.map("TButton", foreground=[("active", "#111827")])
        style.configure("Treeview",
                        background=PALETTE["card"],
                        fieldbackground=PALETTE["card"],
                        bordercolor=PALETTE["border"],
                        rowheight=26,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def _build_header(self):
        header_h = 90
        self.header_canvas = tk.Canvas(self, height=header_h, highlightthickness=0, bd=0)
        self.header_canvas.pack(fill="x")
        self._draw_gradient(self.header_canvas, 0, 0, self.winfo_screenwidth(), header_h,
                            PALETTE["header_start"], PALETTE["header_mid"], PALETTE["header_end"])
        self.header_canvas.create_text(24, header_h//2 - 10, anchor="w",
                                       text="Student Performance Tracker",
                                       font=("Segoe UI", 20, "bold"), fill="white")
        self.header_canvas.create_text(24, header_h//2 + 16, anchor="w",
                                       text="Add • Update • Search • Grade • Save/Load • Export",
                                       font=("Segoe UI", 11), fill="#F8FAFC")

    def _draw_gradient(self, canvas, x1, y1, x2, y2, c1, c2, c3, steps=256):
        r1, g1, b1 = self.winfo_rgb(c1)
        r2, g2, b2 = self.winfo_rgb(c2)
        r3, g3, b3 = self.winfo_rgb(c3)
        for i in range(steps//2):
            r = int(r1 + (r2 - r1) * i / (steps//2))
            g = int(g1 + (g2 - g1) * i / (steps//2))
            b = int(b1 + (b2 - b1) * i / (steps//2))
            color = f"#{r//256:02x}{g//256:02x}{b//256:02x}"
            y = y1 + (y2 - y1) * i / steps
            canvas.create_rectangle(x1, y, x2, y + (y2-y1)/steps, outline="", fill=color)
        for i in range(steps//2):
            r = int(r2 + (r3 - r2) * i / (steps//2))
            g = int(g2 + (g3 - g2) * i / (steps//2))
            b = int(b2 + (b3 - b2) * i / (steps//2))
            color = f"#{r//256:02x}{g//256:02x}{b//256:02x}"
            y = y1 + (y2 - y1) * (i + steps//2) / steps
            canvas.create_rectangle(x1, y, x2, y + (y2-y1)/steps, outline="", fill=color)

    # ------------------- Body: Inputs + Table (L14, L16) -------------------
    def _build_body(self):
        root = ttk.Frame(self)
        root.pack(fill="both", expand=True, padx=12, pady=12)

        # Left: Inputs + Buttons (L14, L15, L17, L18, L19, L20, L21, L23)
        left = ttk.Frame(root, style="Card.TFrame")
        left.pack(side="left", fill="y", padx=(0,10))

        right = ttk.Frame(root)
        right.pack(side="left", fill="both", expand=True)

        title = ttk.Label(left, text="Student Input", font=("Segoe UI", 12, "bold"))
        title.pack(anchor="w", pady=(2,8))

        frm = ttk.Frame(left)
        frm.pack(fill="x")

        ttk.Label(frm, text="Roll No.").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.roll_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.roll_var, width=20).grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(frm, text="Name").grid(row=0, column=2, sticky="w", padx=6, pady=6)
        self.name_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.name_var, width=22).grid(row=0, column=3, padx=6, pady=6)

        ttk.Label(frm, text="Marks (0–100)").grid(row=1, column=0, sticky="w", padx=6, pady=(6,2))
        self.m1_var = tk.StringVar(); self.m2_var = tk.StringVar(); self.m3_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.m1_var, width=8).grid(row=1, column=1, sticky="w", padx=6, pady=2)
        ttk.Entry(frm, textvariable=self.m2_var, width=8).grid(row=1, column=2, sticky="w", padx=6, pady=2)
        ttk.Entry(frm, textvariable=self.m3_var, width=8).grid(row=1, column=3, sticky="w", padx=6, pady=2)

        # Buttons (L17 CRUD, L18 Search, L19 Topper, L23 Reset, L20/21 Save/Load/Export)
        btns = ttk.Frame(left)
        btns.pack(fill="x", pady=(10,4))

        self.add_update_btn = ttk.Button(btns, text="Add / Update", command=self.add_or_update_student)
        self.add_update_btn.grid(row=0, column=0, padx=4, pady=4, sticky="ew")

        self.delete_btn = ttk.Button(btns, text="Delete", command=self.delete_student)
        self.delete_btn.grid(row=0, column=1, padx=4, pady=4, sticky="ew")

        self.clear_btn = ttk.Button(btns, text="Clear Inputs", command=self.clear_inputs)
        self.clear_btn.grid(row=0, column=2, padx=4, pady=4, sticky="ew")

        self.search_btn = ttk.Button(btns, text="Search", command=self.search_student)
        self.search_btn.grid(row=1, column=0, padx=4, pady=4, sticky="ew")

        self.topper_btn = ttk.Button(btns, text="Show Topper", command=self.show_topper)
        self.topper_btn.grid(row=1, column=1, padx=4, pady=4, sticky="ew")

        self.reset_btn = ttk.Button(btns, text="Reset All", command=self.reset_all)
        self.reset_btn.grid(row=1, column=2, padx=4, pady=4, sticky="ew")

        self.save_btn = ttk.Button(btns, text="Save CSV", command=self.save_to_csv)
        self.save_btn.grid(row=2, column=0, padx=4, pady=4, sticky="ew")

        self.load_btn = ttk.Button(btns, text="Load CSV", command=self.load_from_csv)
        self.load_btn.grid(row=2, column=1, padx=4, pady=4, sticky="ew")

        self.export_btn = ttk.Button(btns, text="Export Report", command=self.export_report)
        self.export_btn.grid(row=2, column=2, padx=4, pady=4, sticky="ew")
        for i in range(3):
            btns.grid_columnconfigure(i, weight=1)

        # Table (L16) ---------------------------------------------------------
        table_lbl = ttk.Label(right, text="Student Records", style="Header.TLabel")
        table_lbl.pack(anchor="w", pady=(0,6))

        columns = ("roll", "name", "m1", "m2", "m3", "total", "average", "grade")
        self.tree = ttk.Treeview(right, columns=columns, show="headings", selectmode="browse")
        self.tree.pack(fill="both", expand=True)
        self.tree.heading("roll", text="Roll No.");   self.tree.column("roll", width=110, anchor="center")
        self.tree.heading("name", text="Name");       self.tree.column("name", width=220, anchor="w")
        self.tree.heading("m1", text="Marks 1");      self.tree.column("m1", width=90, anchor="center")
        self.tree.heading("m2", text="Marks 2");      self.tree.column("m2", width=90, anchor="center")
        self.tree.heading("m3", text="Marks 3");      self.tree.column("m3", width=90, anchor="center")
        self.tree.heading("total", text="Total");     self.tree.column("total", width=90, anchor="center")
        self.tree.heading("average", text="Average"); self.tree.column("average", width=100, anchor="center")
        self.tree.heading("grade", text="Grade");     self.tree.column("grade", width=90, anchor="center")

        for g, (fg, bg) in GRADE_TAGS.items():
            self.tree.tag_configure(g, foreground=fg, background=bg)

        # Stats badges (L22 polish)
        stats = ttk.Frame(right)
        stats.pack(fill="x", pady=(8,0))
        self.total_var = tk.StringVar(value="Total: —")
        self.avg_var   = tk.StringVar(value="Average: —")
        self.grade_var = tk.StringVar(value="Grade: —")
        self.total_badge = tk.Label(stats, textvariable=self.total_var, bg="#E0E7FF", fg="#1E3A8A",
                                    font=("Segoe UI", 10, "bold"), padx=10, pady=6)
        self.avg_badge   = tk.Label(stats, textvariable=self.avg_var,   bg="#FEF3C7", fg="#92400E",
                                    font=("Segoe UI", 10, "bold"), padx=10, pady=6)
        self.grade_badge = tk.Label(stats, textvariable=self.grade_var, bg="#DCFCE7", fg="#065F46",
                                    font=("Segoe UI", 10, "bold"), padx=10, pady=6)
        self.total_badge.pack(side="left", padx=(0,8))
        self.avg_badge.pack(side="left", padx=8)
        self.grade_badge.pack(side="left", padx=8)

        helper = ttk.Label(right, text="Tip: Click a row to auto-fill inputs. Use Search with Roll/Name; try Show Topper!",
                           style="Muted.TLabel", wraplength=680, justify="left")
        helper.pack(anchor="w", pady=(8,0))

    def _bind_events(self):
        self.tree.bind("<<TreeviewSelect>>", self.on_select_record)

    # ------------------- Internals: parse/search/refresh -------------------
    def _find_student_index_by_roll(self, roll: str) -> Optional[int]:
        for i, st in enumerate(self.students):
            if st.roll == roll:
                return i
        return None

    def _parse_marks(self, m1: str, m2: str, m3: str) -> List[int]:
        # L15: Validation + errors
        try:
            nums = [int(m1), int(m2), int(m3)]
        except ValueError:
            raise ValueError("Marks must be integers (0–100).")
        for n in nums:
            if n < 0 or n > 100:
                raise ValueError("Marks must be between 0 and 100.")
        return nums

    def _refresh_tree(self, keep_selection: bool = False):
        selection = self.tree.selection()
        selected_id = selection[0] if selection else None
        for iid in self.tree.get_children():
            self.tree.delete(iid)
        for st in self.students:
            tag = grade_to_tag(st.grade())
            self.tree.insert("", "end", iid=st.roll,
                             values=(st.roll, st.name, st.marks[0], st.marks[1], st.marks[2],
                                     st.total(), st.average(), st.grade()),
                             tags=(tag,))
        if keep_selection and selected_id and self.tree.exists(selected_id):
            self.tree.selection_set(selected_id)
            self.tree.see(selected_id)

    def _update_badges_for(self, st: Optional[Student]):
        if not st:
            self.total_var.set("Total: —"); self.avg_var.set("Average: —"); self.grade_var.set("Grade: —")
            self.grade_badge.configure(bg="#E5E7EB", fg="#111827")
            return
        self.total_var.set(f"Total: {st.total()}")
        self.avg_var.set(f"Average: {st.average()}")
        g = st.grade()
        self.grade_var.set(f"Grade: {g}")
        fg, bg = GRADE_TAGS.get(g, ("#111827", "#E5E7EB"))
        self.grade_badge.configure(bg=bg, fg=fg)

    # ------------------- Events (L17–L21 & L23) -------------------
    def on_select_record(self, _evt=None):
        sel = self.tree.selection()
        if not sel:
            return
        roll = sel[0]
        idx = self._find_student_index_by_roll(roll)
        if idx is None:
            return
        st = self.students[idx]
        self.roll_var.set(st.roll); self.name_var.set(st.name)
        self.m1_var.set(str(st.marks[0])); self.m2_var.set(str(st.marks[1])); self.m3_var.set(str(st.marks[2]))
        self._update_badges_for(st)

    def clear_inputs(self):
        self.roll_var.set(""); self.name_var.set("")
        self.m1_var.set(""); self.m2_var.set(""); self.m3_var.set("")
        self.tree.selection_remove(self.tree.selection())
        self._update_badges_for(None)

    def reset_all(self):
        # L23: Reset all
        if messagebox.askyesno("Reset All", "This will remove ALL student records. Continue?"):
            self.students.clear()
            self._refresh_tree()
            self.clear_inputs()

    def add_or_update_student(self):
        # L17: Add/Update with validation (L15)
        roll = self.roll_var.get().strip()
        name = self.name_var.get().strip()
        try:
            if not roll:
                raise ValueError("Roll number cannot be empty.")
            if not name:
                raise ValueError("Name cannot be empty.")
            marks = self._parse_marks(self.m1_var.get(), self.m2_var.get(), self.m3_var.get())

            idx = self._find_student_index_by_roll(roll)
            if idx is None:
                st = Student(roll=roll, name=name, marks=marks)
                self.students.append(st)
                messagebox.showinfo("Added", f"Student added: {roll} — {name}")
            else:
                st = self.students[idx]
                st.name = name; st.marks = marks
                messagebox.showinfo("Updated", f"Student updated: {roll} — {name}")

            self._refresh_tree()
            self.tree.selection_set(roll); self.tree.see(roll)
            self._update_badges_for(self.students[self._find_student_index_by_roll(roll)])

        except Exception as e:
            messagebox.showerror("Input Error", str(e))

    def delete_student(self):
        # L17: Delete
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select Record", "Please select a record to delete.")
            return
        roll = sel[0]
        idx = self._find_student_index_by_roll(roll)
        if idx is None:
            return
        st = self.students[idx]
        if messagebox.askyesno("Delete", f"Delete {st.roll} — {st.name}?"):
            del self.students[idx]
            self._refresh_tree()
            self.clear_inputs()

    def search_student(self):
        # L18: Search by roll or name; highlight results
        query = self.roll_var.get().strip() or self.name_var.get().strip()
        if not query:
            messagebox.showinfo("Search", "Type a Roll No. or Name (or part of it) in the input boxes, then click Search.")
            return
        q = query.lower()
        self.tree.selection_remove(self.tree.selection())
        hits = [st.roll for st in self.students if q in st.roll.lower() or q in st.name.lower()]
        if not hits:
            messagebox.showinfo("Search", f"No matches for \"{query}\".")
            self._update_badges_for(None)
            return
        for rid in hits:
            self.tree.selection_add(rid); self.tree.see(rid)
        if len(hits) == 1:
            idx = self._find_student_index_by_roll(hits[0])
            if idx is not None:
                self._update_badges_for(self.students[idx])
        else:
            self._update_badges_for(None)

    def _popup_confetti(self, text: str):
        # L19: Celebration popup
        top = tk.Toplevel(self); top.title("Celebration"); top.configure(bg="white")
        lbl = tk.Label(top, text=text, font=("Segoe UI", 16, "bold"), bg="white")
        lbl.pack(padx=24, pady=24)
        top.after(1400, top.destroy)

    def show_topper(self):
        # L19: Identify topper; popup + select row
        if not self.students:
            messagebox.showinfo("Topper", "No records available.")
            return
        topper_idx = max(range(len(self.students)), key=lambda i: self.students[i].average())
        topper = self.students[topper_idx]
        messagebox.showinfo("Topper", f"Topper: {topper.roll} — {topper.name}\nAverage: {topper.average()} | Grade: {topper.grade()}")
        self.tree.selection_set(topper.roll); self.tree.see(topper.roll); self._update_badges_for(topper)
        self._popup_confetti(f"Topper: {topper.name}!")

    # ------------- File I/O (L20/L21) -------------
    def save_to_csv(self):
        if not self.students:
            messagebox.showwarning("Save CSV", "No records to save.")
            return
        path = filedialog.asksaveasfilename(title="Save CSV", defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["roll","name","marks1","marks2","marks3","total","average","grade"])
                for st in self.students:
                    writer.writerow([st.roll, st.name, st.marks[0], st.marks[1], st.marks[2],
                                     st.total(), st.average(), st.grade()])
            messagebox.showinfo("Saved", f"Saved {len(self.students)} records to:\n{path}")
        except PermissionError:
            messagebox.showerror("Permission Denied", "Close the file if it is open elsewhere and try again.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save file:\n{e}")

    def load_from_csv(self):
        path = filedialog.askopenfilename(title="Load CSV", filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        try:
            loaded: List[Student] = []
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if not header or len(header) < 8:
                    raise ValueError("Unexpected CSV format. Expected 8 columns.")
                for i, row in enumerate(reader, start=2):
                    if len(row) < 8:
                        raise ValueError(f"Row {i} is malformed: {row}")
                    roll = row[0].strip(); name = row[1].strip()
                    try:
                        m1, m2, m3 = int(row[2]), int(row[3]), int(row[4])
                    except ValueError:
                        raise ValueError(f"Row {i}: marks must be integers.")
                    for m in (m1, m2, m3):
                        if m < 0 or m > 100:
                            raise ValueError(f"Row {i}: marks out of range 0–100.")
                    loaded.append(Student(roll=roll, name=name, marks=[m1, m2, m3]))
            self.students = loaded
            self._refresh_tree(); self.clear_inputs()
            messagebox.showinfo("Loaded", f"Loaded {len(self.students)} records from:\n{path}")
        except Exception as e:
            messagebox.showerror("Load Error", f"Could not load file:\n{e}")

    def export_report(self):
        # L21: Export selected student's TXT report
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Export", "Please select a student record first.")
            return
        roll = sel[0]; idx = self._find_student_index_by_roll(roll)
        if idx is None:
            return
        st = self.students[idx]
        default_filename = f"report_{st.roll}_{st.name.replace(' ', '_')}.txt"
        path = filedialog.asksaveasfilename(title="Export Report",
                                            initialfile=default_filename,
                                            defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("=== Student Report Card ===\n")
                f.write(f"Roll No.: {st.roll}\n")
                f.write(f"Name    : {st.name}\n")
                f.write(f"Marks   : {st.marks}\n")
                f.write(f"Total   : {st.total()}\n")
                f.write(f"Average : {st.average()}\n")
                f.write(f"Grade   : {st.grade()}\n")
                # Simple remark based on grade (extension in L21)
                remark = ("Excellent" if st.grade() in ("A+","A")
                          else "Good" if st.grade()=="B"
                          else "Average" if st.grade()=="C"
                          else "Needs Improvement" if st.grade()=="D"
                          else "Fail")
                f.write(f"Remark  : {remark}\n")
            messagebox.showinfo("Exported", f"Report saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not export report:\n{e}")


# =============================================================================
# ===== Additional Activity Demos (Standalone per Lesson, simple + working) ====
# =============================================================================

def l13_library_record_demo():
    """Lesson 13 Additional Activity:
    Console program: simple LibraryRecord class storing title, author, year.
    """
    @dataclass
    class LibraryRecord:
        title: str
        author: str
        year: int
    # Demo data + print (in real class, prompt input())
    rec = LibraryRecord(title="A Wrinkle in Time", author="Madeleine L'Engle", year=1962)
    print("Library Record:", rec)


def l14_welcome_window():
    """Lesson 14 Additional Activity:
    Tkinter window that shows a simple welcome message.
    """
    root = tk.Tk(); root.title("Welcome"); root.geometry("360x160")
    tk.Label(root, text="Welcome to Python GUI", font=("Segoe UI", 14, "bold")).pack(expand=True)
    root.mainloop()


def l15_pos_neg_checker():
    """Lesson 15 Additional Activity:
    Tkinter input and check positive/negative.
    """
    def check():
        try:
            n = int(entry.get().strip())
            msg.configure(text=("Positive" if n >= 0 else "Negative"))
        except ValueError:
            msg.configure(text="Please enter an integer.")
    root = tk.Tk(); root.title("Number Checker"); root.geometry("300x160")
    tk.Label(root, text="Enter a number:").pack(pady=6)
    entry = tk.Entry(root); entry.pack()
    tk.Button(root, text="Check", command=check).pack(pady=6)
    msg = tk.Label(root, text=""); msg.pack(pady=6)
    root.mainloop()


def l16_books_table():
    """Lesson 16 Additional Activity:
    Treeview table showing five books & authors.
    """
    root = tk.Tk(); root.title("Books Table"); root.geometry("520x240")
    tree = ttk.Treeview(root, columns=("title","author"), show="headings")
    tree.pack(fill="both", expand=True, padx=10, pady=10)
    tree.heading("title", text="Title"); tree.heading("author", text="Author")
    data = [("The Giver","Lois Lowry"),
            ("Charlotte's Web","E. B. White"),
            ("Holes","Louis Sachar"),
            ("Wonder","R. J. Palacio"),
            ("A Wrinkle in Time","Madeleine L'Engle")]
    for t,a in data:
        tree.insert("", "end", values=(t,a))
    root.mainloop()


def l17_grocery_crud():
    """Lesson 17 Additional Activity:
    Simple add/delete grocery items with Tkinter Listbox.
    """
    def add_item():
        item = ent.get().strip()
        if item:
            lb.insert("end", item); ent.delete(0,"end")
    def delete_item():
        sel = lb.curselection()
        if sel:
            lb.delete(sel[0])
    root = tk.Tk(); root.title("Grocery List"); root.geometry("360x260")
    ent = tk.Entry(root); ent.pack(pady=6)
    tk.Button(root, text="Add", command=add_item).pack()
    lb = tk.Listbox(root); lb.pack(fill="both", expand=True, padx=8, pady=8)
    tk.Button(root, text="Delete", command=delete_item).pack(pady=4)
    root.mainloop()


def l18_state_search():
    """Lesson 18 Additional Activity:
    Search a U.S. state in a list (Tkinter).
    """
    states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut"]
    def do_search():
        q = ent.get().strip().lower()
        res = [s for s in states if q and q in s.lower()]
        msg.configure(text="Found: " + (", ".join(res) if res else "No match"))
    root = tk.Tk(); root.title("State Search"); root.geometry("420x180")
    tk.Label(root, text="Search state:").pack(pady=4)
    ent = tk.Entry(root); ent.pack()
    tk.Button(root, text="Search", command=do_search).pack(pady=6)
    msg = tk.Label(root, text=""); msg.pack(pady=6)
    root.mainloop()


def l19_highest_science():
    """Lesson 19 Additional Activity:
    Highlight highest scorer in Science from a given list (console)."""
    records = [
        {"name":"Aarav","Science":88},
        {"name":"Ishita","Science":94},
        {"name":"Rohan","Science":76},
        {"name":"Meera","Science":89},
    ]
    top = max(records, key=lambda r: r["Science"])
    print(f"Highest in Science: {top['name']} with {top['Science']}")


def l20_shopping_csv():
    """Lesson 20 Additional Activity:
    Save & load a shopping list to/from CSV (console)."""
    items = ["Milk","Bread","Eggs"]
    path = "shopping.csv"
    # Save
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["item"]); [w.writerow([i]) for i in items]
    # Load
    loaded = []
    with open(path, "r", encoding="utf-8") as f:
        r = csv.reader(f); next(r, None)
        for row in r:
            if row: loaded.append(row[0])
    print("Saved & Reloaded:", loaded)


def l21_homework_txt():
    """Lesson 21 Additional Activity:
    Create a text file with weekly homework schedule (console)."""
    schedule = ["Mon: Math worksheet","Tue: Science reading","Wed: Python practice",
                "Thu: History notes","Fri: Art sketch"]
    with open("weekly_homework.txt","w",encoding="utf-8") as f:
        f.write("=== Weekly Homework ===\n")
        for line in schedule:
            f.write(line+"\n")
    print("Created weekly_homework.txt")


def l22_style_demo():
    """Lesson 22 Additional Activity:
    Minimal window showing styled header colors (visual)."""
    root = tk.Tk(); root.title("Style Demo"); root.geometry("420x160")
    c = tk.Canvas(root, height=80, highlightthickness=0); c.pack(fill="x")
    # simple gradient-ish bands
    c.create_rectangle(0,0,420,40, fill=PALETTE["header_start"], outline="")
    c.create_rectangle(0,40,420,80, fill=PALETTE["header_mid"], outline="")
    tk.Label(root, text="Styled header preview", font=("Segoe UI", 12, "bold")).pack(pady=10)
    root.mainloop()


# =============================================================================
# ===== Lesson 23: Console (CLI) Capstone Showcase (CRUD/Search/Topper/IO) ====
# =============================================================================

class ConsoleTracker:
    """A simple console-based tracker for Lesson 23 homework (works from terminal)."""
    def __init__(self):
        self.students: List[Student] = []

    # ---- Reuse business logic ----
    def find_index(self, roll: str) -> Optional[int]:
        for i, st in enumerate(self.students):
            if st.roll == roll:
                return i
        return None

    def add_or_update(self, roll: str, name: str, m1: int, m2: int, m3: int):
        for m in (m1, m2, m3):
            if not (0 <= m <= 100):
                raise ValueError("Marks must be 0–100")
        idx = self.find_index(roll)
        if idx is None:
            self.students.append(Student(roll, name, [m1,m2,m3]))
            print("Added.")
        else:
            self.students[idx].name = name
            self.students[idx].marks = [m1,m2,m3]
            print("Updated.")

    def delete(self, roll: str):
        idx = self.find_index(roll)
        if idx is None:
            print("Roll not found."); return
        del self.students[idx]; print("Deleted.")

    def search(self, q: str):
        q = q.lower()
        hits = [st for st in self.students if q in st.roll.lower() or q in st.name.lower()]
        self.print_table(hits if hits else [])
        if not hits:
            print("No matches.")

    def topper(self):
        if not self.students:
            print("No records."); return
        top = max(self.students, key=lambda s: s.average())
        print(f"Topper: {top.roll} — {top.name} | Avg: {top.average()} | Grade: {top.grade()}")

    def save_csv(self, path="students_cli.csv"):
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["roll","name","m1","m2","m3","total","average","grade"])
            for st in self.students:
                w.writerow([st.roll, st.name, st.marks[0], st.marks[1], st.marks[2],
                            st.total(), st.average(), st.grade()])
        print(f"Saved to {path}")

    def load_csv(self, path="students_cli.csv"):
        loaded: List[Student] = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                r = csv.reader(f)
                next(r, None)
                for row in r:
                    roll, name, m1, m2, m3 = row[0], row[1], int(row[2]), int(row[3]), int(row[4])
                    loaded.append(Student(roll, name, [m1, m2, m3]))
            self.students = loaded
            print(f"Loaded {len(self.students)} records from {path}")
        except FileNotFoundError:
            print("CSV not found.")

    def export_txt(self, roll: str):
        idx = self.find_index(roll)
        if idx is None:
            print("Roll not found."); return
        st = self.students[idx]
        path = f"report_{st.roll}_{st.name.replace(' ', '_')}.txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write("=== Student Report Card ===\n")
            f.write(f"Roll No.: {st.roll}\n")
            f.write(f"Name    : {st.name}\n")
            f.write(f"Marks   : {st.marks}\n")
            f.write(f"Total   : {st.total()}\n")
            f.write(f"Average : {st.average()}\n")
            f.write(f"Grade   : {st.grade()}\n")
        print(f"Exported to {path}")

    # ---- Utilities ----
    def print_table(self, rows: List[Student] = None):
        rows = self.students if rows is None else rows
        if not rows:
            print("(no rows)"); return
        print(f"{'Roll':<8} {'Name':<20} {'M1':>3} {'M2':>3} {'M3':>3} {'Tot':>4} {'Avg':>5} {'Gr':>2}")
        for st in rows:
            print(f"{st.roll:<8} {st.name:<20} {st.marks[0]:>3} {st.marks[1]:>3} {st.marks[2]:>3} "
                  f"{st.total():>4} {st.average():>5} {st.grade():>2}")

    def run(self):
        print("Console Capstone (Lesson 23). Type 'help' for commands.")
        while True:
            cmd = input("> ").strip().lower()
            if cmd in ("quit","exit"):
                break
            elif cmd == "help":
                print("Commands: add, update, del, list, search, topper, save, load, report, quit")
                print(" add/update: roll name m1 m2 m3")
                print(" del: roll | search: query | report: roll")
            elif cmd in ("add","update"):
                try:
                    parts = input("Enter: roll name m1 m2 m3: ").split()
                    if len(parts) < 5: print("Need 5 parts."); continue
                    roll, name = parts[0], parts[1]
                    m1, m2, m3 = map(int, parts[2:5])
                    self.add_or_update(roll, name, m1, m2, m3)
                except Exception as e:
                    print("Error:", e)
            elif cmd == "del":
                roll = input("Enter roll: ").strip()
                self.delete(roll)
            elif cmd == "list":
                self.print_table()
            elif cmd == "search":
                q = input("Enter query: ").strip()
                self.search(q)
            elif cmd == "topper":
                self.topper()
            elif cmd == "save":
                self.save_csv()
            elif cmd == "load":
                self.load_csv()
            elif cmd == "report":
                roll = input("Enter roll: ").strip()
                self.export_txt(roll)
            else:
                print("Unknown. Try 'help'.")


# =============================================================================
# ===== Main Entrypoint: choose GUI (default), CLI, or demo activities ========
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Student Progress Tracker (Lessons 13–23)")
    parser.add_argument("--cli", action="store_true", help="Run console (Lesson 23) instead of GUI")
    parser.add_argument("--demo", type=str, default="",
                        help="Run a specific additional-activity demo: "
                             "l13_library | l14_welcome | l15_posneg | l16_books | "
                             "l17_grocery | l18_state | l19_science | l20_shop | "
                             "l21_homework | l22_style")
    args = parser.parse_args()

    if args.cli:
        ConsoleTracker().run()
        return

    demos = {
        "l13_library": l13_library_record_demo,
        "l14_welcome": l14_welcome_window,
        "l15_posneg":  l15_pos_neg_checker,
        "l16_books":   l16_books_table,
        "l17_grocery": l17_grocery_crud,
        "l18_state":   l18_state_search,
        "l19_science": l19_highest_science,
        "l20_shop":    l20_shopping_csv,
        "l21_homework": l21_homework_txt,
        "l22_style":   l22_style_demo,
    }
    if args.demo:
        fn = demos.get(args.demo.lower())
        if not fn:
            print("Unknown demo. See --help for options.")
            return
        fn()
        return

    # Default: run the full GUI (Lessons 14–23 integrated)
    app = StudentPerformanceApp()
    app.mainloop()


if __name__ == "__main__":
    main()
