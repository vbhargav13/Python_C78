"""
Student Performance Tracker 🎓📊 (Colorful + Emoji Edition)
==========================================================
Features
- Add / Update / Delete student records ➕✏️🗑️
- Validate inputs (name, roll, marks) ✅
- Compute Total, Average, Grade live 🧮
- Search students (by roll or name) 🔍
- Show topper with celebratory popup 🏆🎉
- Save/Load CSV with robust error handling 💾📂
- Export a text report for any student 🧾
- Polished UI: gradient header, colorful badges, emoji labels, Treeview with grade-colored rows 🌈

Run:
    python student_performance_tracker_colorful.py
"""

import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from dataclasses import dataclass, field
from typing import List, Optional


# ---------- Domain Model ----------
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


# ---------- UI Helpers ----------
PALETTE = {
    "bg": "#F7FAFC",
    "header_start": "#7F7FD5",
    "header_mid":   "#86A8E7",
    "header_end":   "#91EAE4",
    "accent": "#2563EB",      # blue-600
    "success": "#16A34A",     # green-600
    "warn": "#F59E0B",        # amber-500
    "danger": "#DC2626",      # red-600
    "muted": "#64748B",       # slate-500
    "card": "#FFFFFF",
    "border": "#E5E7EB",
}

GRADE_TAGS = {
    "A+": ("#065F46", "#D1FAE5"),   # text, background
    "A":  ("#065F46", "#D1FAE5"),
    "B":  ("#1E40AF", "#DBEAFE"),
    "C":  ("#92400E", "#FEF3C7"),
    "D":  ("#92400E", "#FEF3C7"),
    "F":  ("#7F1D1D", "#FEE2E2"),
}


def grade_to_tag(grade: str) -> str:
    return grade  # tags named as grade strings


# ---------- Main App ----------
class StudentPerformanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎓📊 Student Performance Tracker — Colorful Edition")
        self.geometry("1100x650")
        self.minsize(1024, 620)
        self.configure(bg=PALETTE["bg"])

        # Data store
        self.students: List[Student] = []

        # Build UI
        self._build_styles()
        self._build_header()
        self._build_body()
        self._bind_events()

    # ----- Styles -----
    def _build_styles(self):
        style = ttk.Style(self)
        # Best cross-platform base theme
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("TFrame", background=PALETTE["bg"])
        style.configure("Card.TFrame", background=PALETTE["card"], relief="groove")
        style.configure("TLabel", background=PALETTE["bg"], foreground="#111827", font=("Segoe UI", 10))
        style.configure("Header.TLabel", background=PALETTE["bg"], foreground="#111827", font=("Segoe UI", 14, "bold"))
        style.configure("Muted.TLabel", background=PALETTE["bg"], foreground=PALETTE["muted"], font=("Segoe UI", 10, "italic"))
        style.configure("TButton", font=("Segoe UI Emoji", 10, "bold"), padding=6)
        style.map("TButton", foreground=[("active", "#111827")])

        # Treeview style
        style.configure("Treeview",
                        background=PALETTE["card"],
                        fieldbackground=PALETTE["card"],
                        bordercolor=PALETTE["border"],
                        rowheight=26,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    # ----- Header (Gradient Canvas) -----
    def _build_header(self):
        header_h = 90
        self.header_canvas = tk.Canvas(self, height=header_h, highlightthickness=0, bd=0)
        self.header_canvas.pack(fill="x")

        # Draw horizontal gradient
        self._draw_gradient(self.header_canvas, 0, 0, self.winfo_screenwidth(), header_h,
                            PALETTE["header_start"], PALETTE["header_mid"], PALETTE["header_end"])

        # Title + Subtitle
        self.header_title = self.header_canvas.create_text(
            24, header_h//2 - 10, anchor="w",
            text="🎓📊 Student Performance Tracker",
            font=("Segoe UI Emoji", 20, "bold"),
            fill="white"
        )
        self.header_sub = self.header_canvas.create_text(
            24, header_h//2 + 18, anchor="w",
            text="Add • Update • Search • Grade • Save/Load • Export  —  Now with 🌈 color & emojis!",
            font=("Segoe UI", 11),
            fill="#F8FAFC"
        )

    def _draw_gradient(self, canvas, x1, y1, x2, y2, c1, c2, c3, steps=256):
        # simple three-point gradient
        r1, g1, b1 = self.winfo_rgb(c1)
        r2, g2, b2 = self.winfo_rgb(c2)
        r3, g3, b3 = self.winfo_rgb(c3)
        # two segments: c1->c2 and c2->c3
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

    # ----- Body -----
    def _build_body(self):
        root = ttk.Frame(self)
        root.pack(fill="both", expand=True, padx=12, pady=12)

        # Left column: Inputs + Actions
        left = ttk.Frame(root, style="Card.TFrame")
        left.pack(side="left", fill="y", padx=(0, 10), pady=0, ipadx=6, ipady=6)

        # Right column: Table + Stats
        right = ttk.Frame(root)
        right.pack(side="left", fill="both", expand=True)

        # --- Inputs
        title = ttk.Label(left, text="📝 Student Input", font=("Segoe UI Emoji", 12, "bold"))
        title.pack(anchor="w", pady=(2, 8))

        frm = ttk.Frame(left)
        frm.pack(fill="x")

        ttk.Label(frm, text="🧾 Roll No.").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.roll_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.roll_var, width=20).grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(frm, text="👩‍🎓 Name").grid(row=0, column=2, sticky="w", padx=6, pady=6)
        self.name_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.name_var, width=22).grid(row=0, column=3, padx=6, pady=6)

        ttk.Label(frm, text="🧮 Marks (0–100) →").grid(row=1, column=0, sticky="w", padx=6, pady=(6,2))

        self.m1_var = tk.StringVar(); self.m2_var = tk.StringVar(); self.m3_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.m1_var, width=8).grid(row=1, column=1, sticky="w", padx=6, pady=2)
        ttk.Entry(frm, textvariable=self.m2_var, width=8).grid(row=1, column=2, sticky="w", padx=6, pady=2)
        ttk.Entry(frm, textvariable=self.m3_var, width=8).grid(row=1, column=3, sticky="w", padx=6, pady=2)

        # --- Buttons
        btns = ttk.Frame(left)
        btns.pack(fill="x", pady=(10, 4))

        self.add_update_btn = ttk.Button(btns, text="➕ Add / Update", command=self.add_or_update_student)
        self.add_update_btn.grid(row=0, column=0, padx=4, pady=4, sticky="ew")

        self.delete_btn = ttk.Button(btns, text="🗑️ Delete", command=self.delete_student)
        self.delete_btn.grid(row=0, column=1, padx=4, pady=4, sticky="ew")

        self.clear_btn = ttk.Button(btns, text="🧹 Clear Inputs", command=self.clear_inputs)
        self.clear_btn.grid(row=0, column=2, padx=4, pady=4, sticky="ew")

        self.search_btn = ttk.Button(btns, text="🔍 Search", command=self.search_student)
        self.search_btn.grid(row=1, column=0, padx=4, pady=4, sticky="ew")

        self.topper_btn = ttk.Button(btns, text="🏆 Show Topper", command=self.show_topper)
        self.topper_btn.grid(row=1, column=1, padx=4, pady=4, sticky="ew")

        self.reset_btn = ttk.Button(btns, text="♻️ Reset All", command=self.reset_all)
        self.reset_btn.grid(row=1, column=2, padx=4, pady=4, sticky="ew")

        self.save_btn = ttk.Button(btns, text="💾 Save CSV", command=self.save_to_csv)
        self.save_btn.grid(row=2, column=0, padx=4, pady=4, sticky="ew")

        self.load_btn = ttk.Button(btns, text="📂 Load CSV", command=self.load_from_csv)
        self.load_btn.grid(row=2, column=1, padx=4, pady=4, sticky="ew")

        self.export_btn = ttk.Button(btns, text="🧾 Export Report", command=self.export_report)
        self.export_btn.grid(row=2, column=2, padx=4, pady=4, sticky="ew")

        for i in range(3):
            btns.grid_columnconfigure(i, weight=1)

        # --- Table (Treeview)
        table_lbl = ttk.Label(right, text="📚 Student Records", style="Header.TLabel")
        table_lbl.pack(anchor="w", pady=(0, 6))

        columns = ("roll", "name", "m1", "m2", "m3", "total", "average", "grade")
        self.tree = ttk.Treeview(right, columns=columns, show="headings", selectmode="browse")
        self.tree.pack(fill="both", expand=True)

        self.tree.heading("roll", text="Roll No.")
        self.tree.heading("name", text="Name")
        self.tree.heading("m1", text="Marks 1")
        self.tree.heading("m2", text="Marks 2")
        self.tree.heading("m3", text="Marks 3")
        self.tree.heading("total", text="Total")
        self.tree.heading("average", text="Average")
        self.tree.heading("grade", text="Grade")

        self.tree.column("roll", width=110, anchor="center")
        self.tree.column("name", width=220, anchor="w")
        self.tree.column("m1", width=90, anchor="center")
        self.tree.column("m2", width=90, anchor="center")
        self.tree.column("m3", width=90, anchor="center")
        self.tree.column("total", width=90, anchor="center")
        self.tree.column("average", width=100, anchor="center")
        self.tree.column("grade", width=90, anchor="center")

        # Tag styles per grade (foreground/background)
        for g, (fg, bg) in GRADE_TAGS.items():
            self.tree.tag_configure(g, foreground=fg, background=bg)

        # --- Stats Bar
        stats = ttk.Frame(right)
        stats.pack(fill="x", pady=(8, 0))

        self.total_var = tk.StringVar(value="Total: —")
        self.avg_var = tk.StringVar(value="Average: —")
        self.grade_var = tk.StringVar(value="Grade: —")

        self.total_badge = tk.Label(stats, textvariable=self.total_var, bg="#E0E7FF", fg="#1E3A8A",
                                    font=("Segoe UI", 10, "bold"), padx=10, pady=6)
        self.total_badge.pack(side="left", padx=(0, 8))

        self.avg_badge = tk.Label(stats, textvariable=self.avg_var, bg="#FEF3C7", fg="#92400E",
                                  font=("Segoe UI", 10, "bold"), padx=10, pady=6)
        self.avg_badge.pack(side="left", padx=8)

        self.grade_badge = tk.Label(stats, textvariable=self.grade_var, bg="#DCFCE7", fg="#065F46",
                                    font=("Segoe UI", 10, "bold"), padx=10, pady=6)
        self.grade_badge.pack(side="left", padx=8)

        helper = ttk.Label(right, text="💡 Pro tip: Click a row to auto-fill inputs. Use 🔍 Search with Roll/Name, then 🏆 to spotlight the topper!",
                           style="Muted.TLabel", wraplength=680, justify="left")
        helper.pack(anchor="w", pady=(8, 0))

    def _bind_events(self):
        self.tree.bind("<<TreeviewSelect>>", self.on_select_record)

    # ----- Data Ops -----
    def _find_student_index_by_roll(self, roll: str) -> Optional[int]:
        for i, st in enumerate(self.students):
            if st.roll == roll:
                return i
        return None

    def _parse_marks(self, m1: str, m2: str, m3: str) -> List[int]:
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

        # Clear
        for iid in self.tree.get_children():
            self.tree.delete(iid)

        # Insert
        for st in self.students:
            tag = grade_to_tag(st.grade())
            self.tree.insert("", "end", iid=st.roll,
                             values=(st.roll, st.name, st.marks[0], st.marks[1], st.marks[2],
                                     st.total(), st.average(), st.grade()),
                             tags=(tag,))

        # Reselect
        if keep_selection and selected_id and self.tree.exists(selected_id):
            self.tree.selection_set(selected_id)
            self.tree.see(selected_id)

    def _update_badges_for(self, st: Optional[Student]):
        if not st:
            self.total_var.set("Total: —")
            self.avg_var.set("Average: —")
            self.grade_var.set("Grade: —")
            self.grade_badge.configure(bg="#E5E7EB", fg="#111827")
            return

        self.total_var.set(f"Total: {st.total()}")
        self.avg_var.set(f"Average: {st.average()}")
        g = st.grade()
        self.grade_var.set(f"Grade: {g}")
        # Color badge by grade
        fg, bg = GRADE_TAGS.get(g, ("#111827", "#E5E7EB"))
        self.grade_badge.configure(bg=bg, fg=fg)

    # ----- Event Handlers -----
    def on_select_record(self, _evt=None):
        sel = self.tree.selection()
        if not sel:
            return
        roll = sel[0]
        idx = self._find_student_index_by_roll(roll)
        if idx is None:
            return
        st = self.students[idx]

        self.roll_var.set(st.roll)
        self.name_var.set(st.name)
        self.m1_var.set(str(st.marks[0]))
        self.m2_var.set(str(st.marks[1]))
        self.m3_var.set(str(st.marks[2]))

        self._update_badges_for(st)

    # ----- CRUD & Utilities -----
    def clear_inputs(self):
        self.roll_var.set("")
        self.name_var.set("")
        self.m1_var.set("")
        self.m2_var.set("")
        self.m3_var.set("")
        self.tree.selection_remove(self.tree.selection())
        self._update_badges_for(None)

    def reset_all(self):
        if messagebox.askyesno("♻️ Reset All", "This will remove ALL student records. Continue?"):
            self.students.clear()
            self._refresh_tree()
            self.clear_inputs()

    def add_or_update_student(self):
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
                messagebox.showinfo("Added ✅", f"Student added:\n{roll} — {name}")
            else:
                st = self.students[idx]
                st.name = name
                st.marks = marks
                messagebox.showinfo("Updated ✏️", f"Student updated:\n{roll} — {name}")

            self._refresh_tree()
            # Select the row
            self.tree.selection_set(roll)
            self.tree.see(roll)
            self._update_badges_for(self.students[self._find_student_index_by_roll(roll)])

        except Exception as e:
            messagebox.showerror("Input Error ⚠️", str(e))

    def delete_student(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select Record", "Please select a record to delete.")
            return
        roll = sel[0]
        idx = self._find_student_index_by_roll(roll)
        if idx is None:
            return
        st = self.students[idx]
        if messagebox.askyesno("Delete 🗑️", f"Delete {st.roll} — {st.name}?"):
            del self.students[idx]
            self._refresh_tree()
            self.clear_inputs()

    def search_student(self):
        query = self.roll_var.get().strip() or self.name_var.get().strip()
        if not query:
            messagebox.showinfo("Search 🔍", "Type a Roll No. or Name (or part of it) in the input boxes, then click Search.")
            return

        query_lower = query.lower()
        self.tree.selection_remove(self.tree.selection())
        hits = []
        for st in self.students:
            if query_lower in st.roll.lower() or query_lower in st.name.lower():
                hits.append(st.roll)

        if not hits:
            messagebox.showinfo("Search 🔍", f"No matches for “{query}”.")
            self._update_badges_for(None)
            return

        # Select first hit and show all hits selected
        for rid in hits:
            self.tree.selection_add(rid)
            self.tree.see(rid)

        # Update badges for single hit; clear for multiple
        if len(hits) == 1:
            idx = self._find_student_index_by_roll(hits[0])
            if idx is not None:
                self._update_badges_for(self.students[idx])
        else:
            self._update_badges_for(None)

    def _popup_confetti(self, text: str):
        top = tk.Toplevel(self)
        top.title("🎉 Celebration!")
        top.configure(bg="white")
        lbl = tk.Label(top, text=f"🎉🎊 {text} 🎊🎉", font=("Segoe UI Emoji", 16, "bold"), bg="white")
        lbl.pack(padx=24, pady=24)
        top.after(1400, top.destroy)

    def show_topper(self):
        if not self.students:
            messagebox.showinfo("Topper 🏆", "No records available.")
            return
        topper_idx = max(range(len(self.students)), key=lambda i: self.students[i].average())
        topper = self.students[topper_idx]

        messagebox.showinfo(
            "Topper 🏆",
            f"Topper: {topper.roll} — {topper.name}\n"
            f"Average: {topper.average()} | Grade: {topper.grade()}"
        )
        self.tree.selection_set(topper.roll)
        self.tree.see(topper.roll)
        self._update_badges_for(topper)
        self._popup_confetti(f"Topper: {topper.name}! 🏆")

    # ----- File I/O -----
    def save_to_csv(self):
        if not self.students:
            messagebox.showwarning("Save CSV 💾", "No records to save.")
            return
        path = filedialog.asksaveasfilename(
            title="Save CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return

        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["roll", "name", "marks1", "marks2", "marks3", "total", "average", "grade"])
                for st in self.students:
                    writer.writerow([st.roll, st.name, st.marks[0], st.marks[1], st.marks[2], st.total(), st.average(), st.grade()])
            messagebox.showinfo("Saved 💾", f"Saved {len(self.students)} records to:\n{path}")
        except PermissionError:
            messagebox.showerror("Permission Denied", "Close the file if it is open elsewhere and try again.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save file:\n{e}")

    def load_from_csv(self):
        path = filedialog.askopenfilename(
            title="Load CSV",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return

        try:
            loaded: List[Student] = []
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if not header or len(header) < 8:
                    raise ValueError("Unexpected CSV format. Expected 8 columns (roll,name,m1,m2,m3,total,average,grade).")
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
            self._refresh_tree()
            self.clear_inputs()
            messagebox.showinfo("Loaded 📂", f"Loaded {len(self.students)} records from:\n{path}")
        except Exception as e:
            messagebox.showerror("Load Error", f"Could not load file:\n{e}")

    def export_report(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Export 🧾", "Please select a student record first.")
            return
        roll = sel[0]
        idx = self._find_student_index_by_roll(roll)
        if idx is None:
            return
        st = self.students[idx]

        default_filename = f"report_{st.roll}_{st.name.replace(' ', '_')}.txt"
        path = filedialog.asksaveasfilename(
            title="Export Report",
            initialfile=default_filename,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
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
            messagebox.showinfo("Exported 🧾", f"Report saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not export report:\n{e}")


if __name__ == "__main__":
    app = StudentPerformanceApp()
    app.mainloop()
