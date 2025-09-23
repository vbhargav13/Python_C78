# Student Progress Tracker — Unified Single-Window (Lessons 13–23)
# ============================================================================
# GOAL
# ----
# This version keeps EVERYTHING inside ONE Tkinter window and adds
# RICH, SEQUENTIAL COMMENT BLOCKS to map code to lessons (L13–L23) and
# additional activities. Search for:  <<< LESSON XX START >>>  /  <<< LESSON XX END >>>
# and  <<< LESSON XX ACTIVITY START >>> / <<< LESSON XX ACTIVITY END >>>
#
# TEACHING FLOW (ILO MAPPING)
# ---------------------------
# L13  Dataclass Student with total(), average(), grade(); VS Code intro; project setup.
# L14  Tkinter basics: main window, title, geometry; labels/entries for inputs.
# L15  StringVar, Entry, validation, messagebox for errors.
# L16  Treeview table (roll, name, marks, total, average, grade) + computed columns.
# L17  CRUD (Add/Update/Delete/Clear), dynamic table refresh.
# L18  Search by roll/name; highlight selection in table.
# L19  Topper identification; in-window celebration banner.
# L20  Save/Load CSV with file dialogs; error handling.
# L21  Export TXT report for a selected student.
# L22  UI polish: ttk styles, gradient header, colored badges, grade tags.
# L23  Showcase: All features integrated; discuss debugging & reflections.
# ============================================================================

# <<< COMMON IMPORTS START (USED ACROSS LESSONS 13–23) >>>
import csv                                      # L20: CSV save/load
import tkinter as tk                            # L14: Tkinter base
from tkinter import ttk, messagebox, filedialog # L14–L21: widgets, dialogs
from dataclasses import dataclass, field        # L13: dataclass model
from typing import List, Optional               # Helpful types for clarity
# <<< COMMON IMPORTS END >>>

# <<< LESSON 13 START: DATA MODEL (DATACLASS + ANALYTICS) >>>
@dataclass
class Student:
    """L13: Core domain entity with marks analytics used across GUI.
    ILOs: define attributes (roll, name, marks), implement total(), average(), grade().
    """
    roll: str                                   # Unique roll-id (string for simplicity)
    name: str                                   # Student name
    marks: List[int] = field(default_factory=lambda: [0, 0, 0])  # 3 subjects

    def total(self) -> int:
        """Return sum of marks (used in table + exports)."""
        return sum(self.marks)

    def average(self) -> float:
        """Return average rounded to 2 decimals; safe for empty list."""
        return round(self.total() / len(self.marks), 2) if self.marks else 0.0

    def grade(self) -> str:
        """Simple rubric based on average()."""
        avg = self.average()
        if avg >= 90:   return "A+"
        elif avg >= 80: return "A"
        elif avg >= 70: return "B"
        elif avg >= 60: return "C"
        elif avg >= 50: return "D"
        else:           return "F"
# <<< LESSON 13 END >>>


# <<< LESSON 22 START: GLOBAL STYLES / THEME (POLISH) >>>
PALETTE = {
    "bg": "#F7FAFC", "header_start": "#7F7FD5", "header_mid": "#86A8E7", "header_end": "#91EAE4",
    "accent": "#2563EB", "success": "#16A34A", "warn": "#F59E0B", "danger": "#DC2626",
    "muted": "#64748B", "card": "#FFFFFF", "border": "#E5E7EB",
}

GRADE_TAGS = {
    "A+": ("#065F46", "#D1FAE5"),
    "A":  ("#065F46", "#D1FAE5"),
    "B":  ("#1E40AF", "#DBEAFE"),
    "C":  ("#92400E", "#FEF3C7"),
    "D":  ("#92400E", "#FEF3C7"),
    "F":  ("#7F1D1D", "#FEE2E2"),
}
# <<< LESSON 22 END >>>


# ======================= Main App: Single Window ============================
# <<< L14–L23 START: UNIFIED ROOT WINDOW, TABS, HEADER >>>
class UnifiedApp(tk.Tk):
    """One Tk root with two primary tabs:
       1) Tracker: the full capstone GUI (L14–L23).
       2) Activities: sub-tabs for each additional activity (L13–L22).
    """
    def __init__(self):
        super().__init__()  # Create the Tk root window
        # <<< LESSON 14 START: BASE WINDOW (TITLE, SIZE, BACKGROUND) >>>
        self.title("Student Performance — L13–L23 (Unified Single Window)")
        self.geometry("1180x720")
        self.minsize(1080, 660)
        self.configure(bg=PALETTE["bg"])
        # <<< LESSON 14 END >>>

        # <<< LESSON 22 START: APPLY TTK STYLES GLOBALLY >>>
        self._build_styles()
        # <<< LESSON 22 END >>>

        # <<< LESSON 22 START: HEADER (CANVAS GRADIENT + SUBTITLE) >>>
        self._build_header()
        # <<< LESSON 22 END >>>

        # <<< LESSON 14 START: TAB LAYOUT (NOTEBOOK WITH 2 TABS) >>>
        self.nb = ttk.Notebook(self)         # Notebook provides tabbed UI
        self.nb.pack(fill="both", expand=True, padx=12, pady=12)

        # --- Tracker Tab (Main Project) ---
        self.tab_tracker = ttk.Frame(self.nb)
        self.nb.add(self.tab_tracker, text="Tracker (L14–L23)")
        self.tracker = TrackerFrame(self.tab_tracker)  # Instantiate tracker UI
        self.tracker.pack(fill="both", expand=True)

        # --- Activities Tab (All Additional Activities) ---
        self.tab_activities = ttk.Frame(self.nb)
        self.nb.add(self.tab_activities, text="Activities (L13–L22)")
        self.activities = ActivitiesFrame(self.tab_activities)
        self.activities.pack(fill="both", expand=True)
        # <<< LESSON 14 END >>>

    # ----- L22: Styles + header gradient -----
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
                                       text="Student Performance Tracker — Unified Window",
                                       font=("Segoe UI", 20, "bold"), fill="white")
        self.header_canvas.create_text(24, header_h//2 + 16, anchor="w",
                                       text="Tracker, Search, Topper, CSV, Reports + All Activities in tabs",
                                       font=("Segoe UI", 11), fill="#F8FAFC")

    def _draw_gradient(self, canvas, x1, y1, x2, y2, c1, c2, c3, steps=256):
        # Paint a vertical gradient (two-stage) on a canvas
        r1, g1, b1 = self.winfo_rgb(c1); r2, g2, b2 = self.winfo_rgb(c2); r3, g3, b3 = self.winfo_rgb(c3)
        for i in range(steps//2):
            r = int(r1 + (r2 - r1) * i / (steps//2)); g = int(g1 + (g2 - g1) * i / (steps//2)); b = int(b1 + (b2 - b1) * i / (steps//2))
            color = f"#{r//256:02x}{g//256:02x}{b//256:02x}"
            y = y1 + (y2 - y1) * i / steps
            canvas.create_rectangle(x1, y, x2, y + (y2-y1)/steps, outline="", fill=color)
        for i in range(steps//2):
            r = int(r2 + (r3 - r2) * i / (steps//2)); g = int(g2 + (g3 - g2) * i / (steps//2)); b = int(b2 + (b3 - b2) * i / (steps//2))
            color = f"#{r//256:02x}{g//256:02x}{b//256:02x}"
            y = y1 + (y2 - y1) * (i + steps//2) / steps
            canvas.create_rectangle(x1, y, x2, y + (y2-y1)/steps, outline="", fill=color)
# <<< L14–L23 END: UNIFIED ROOT WINDOW, TABS, HEADER >>>


# -------------------- Tracker Frame (L14–L23) -------------------------------
# <<< L14–L23 START: TRACKER TAB (MAIN PROJECT UI) >>>
class TrackerFrame(ttk.Frame):
    """Encapsulates the main project GUI so it can live inside a tab."""
    def __init__(self, parent):
        super().__init__(parent, style="TFrame")
        # In-memory list of Student objects
        self.students: List[Student] = []

        # UI build in sections
        self._build_body()
        self._bind_events()

    # Build input panel + table + badges + buttons
    def _build_body(self):
        root = ttk.Frame(self, style="TFrame"); root.pack(fill="both", expand=True)
        # LEFT: input + buttons
        left = ttk.Frame(root, style="Card.TFrame"); left.pack(side="left", fill="y", padx=(0,10), pady=8)
        # RIGHT: table + badges
        right = ttk.Frame(root, style="TFrame"); right.pack(side="left", fill="both", expand=True, pady=8)

        # <<< LESSON 14 START: INPUT WIDGETS (LABELS/ENTRIES) >>>
        # <<< LESSON 15 START: STRINGVAR BINDINGS (FOR VALIDATION LATER) >>>
        title = ttk.Label(left, text="Student Input", font=("Segoe UI", 12, "bold")); title.pack(anchor="w", pady=(6,6), padx=8)
        frm = ttk.Frame(left, style="TFrame"); frm.pack(fill="x", padx=8)

        ttk.Label(frm, text="Roll No.").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.roll_var = tk.StringVar(); ttk.Entry(frm, textvariable=self.roll_var, width=20).grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(frm, text="Name").grid(row=0, column=2, sticky="w", padx=6, pady=6)
        self.name_var = tk.StringVar(); ttk.Entry(frm, textvariable=self.name_var, width=22).grid(row=0, column=3, padx=6, pady=6)

        ttk.Label(frm, text="Marks (0–100)").grid(row=1, column=0, sticky="w", padx=6, pady=(6,2))
        self.m1_var = tk.StringVar(); self.m2_var = tk.StringVar(); self.m3_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.m1_var, width=8).grid(row=1, column=1, sticky="w", padx=6, pady=2)
        ttk.Entry(frm, textvariable=self.m2_var, width=8).grid(row=1, column=2, sticky="w", padx=6, pady=2)
        ttk.Entry(frm, textvariable=self.m3_var, width=8).grid(row=1, column=3, sticky="w", padx=6, pady=2)
        # <<< LESSON 15 END >>>
        # <<< LESSON 14 END >>>

        # <<< LESSON 17 START: BUTTONS FOR CRUD + UTILITIES >>> 
        btns = ttk.Frame(left, style="TFrame"); btns.pack(fill="x", pady=(10,6), padx=8)
        self.add_update_btn = ttk.Button(btns, text="Add / Update", command=self.add_or_update_student); self.add_update_btn.grid(row=0, column=0, padx=4, pady=4, sticky="ew")
        self.delete_btn     = ttk.Button(btns, text="Delete",       command=self.delete_student);      self.delete_btn.grid(row=0, column=1, padx=4, pady=4, sticky="ew")
        self.clear_btn      = ttk.Button(btns, text="Clear Inputs", command=self.clear_inputs);        self.clear_btn.grid(row=0, column=2, padx=4, pady=4, sticky="ew")
        # <<< LESSON 18 START: SEARCH BUTTON >>> 
        self.search_btn     = ttk.Button(btns, text="Search",       command=self.search_student);      self.search_btn.grid(row=1, column=0, padx=4, pady=4, sticky="ew")
        # <<< LESSON 18 END >>>
        # <<< LESSON 19 START: TOPPER BUTTON (CELEBRATION) >>> 
        self.topper_btn     = ttk.Button(btns, text="Show Topper",  command=self.show_topper);         self.topper_btn.grid(row=1, column=1, padx=4, pady=4, sticky="ew")
        # <<< LESSON 19 END >>>
        # <<< LESSON 23 START: RESET ALL (SHOWCASE/DEBUGGING) >>> 
        self.reset_btn      = ttk.Button(btns, text="Reset All",    command=self.reset_all);           self.reset_btn.grid(row=1, column=2, padx=4, pady=4, sticky="ew")
        # <<< LESSON 23 END >>>
        # <<< LESSON 20 START: SAVE/LOAD CSV >>> 
        self.save_btn       = ttk.Button(btns, text="Save CSV",     command=self.save_to_csv);         self.save_btn.grid(row=2, column=0, padx=4, pady=4, sticky="ew")
        self.load_btn       = ttk.Button(btns, text="Load CSV",     command=self.load_from_csv);       self.load_btn.grid(row=2, column=1, padx=4, pady=4, sticky="ew")
        # <<< LESSON 20 END >>>
        # <<< LESSON 21 START: EXPORT TXT REPORT >>> 
        self.export_btn     = ttk.Button(btns, text="Export Report",command=self.export_report);       self.export_btn.grid(row=2, column=2, padx=4, pady=4, sticky="ew")
        # <<< LESSON 21 END >>>
        for i in range(3): btns.grid_columnconfigure(i, weight=1)
        # <<< LESSON 17 END >>>

        # <<< LESSON 16 START: TREEVIEW TABLE WITH COMPUTED COLUMNS >>>
        table_lbl = ttk.Label(right, text="Student Records", style="Header.TLabel"); table_lbl.pack(anchor="w", pady=(0,6), padx=6)
        columns = ("roll", "name", "m1", "m2", "m3", "total", "average", "grade")
        self.tree = ttk.Treeview(right, columns=columns, show="headings", selectmode="browse")
        self.tree.pack(fill="both", expand=True, padx=6)
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
        # <<< LESSON 16 END >>>

        # <<< LESSON 22 START: BADGES + CELEBRATION BANNER (UI POLISH) >>>
        stats = ttk.Frame(right, style="TFrame"); stats.pack(fill="x", pady=(8,0), padx=6)
        self.total_var = tk.StringVar(value="Total: —"); self.avg_var = tk.StringVar(value="Average: —"); self.grade_var = tk.StringVar(value="Grade: —")
        self.total_badge = tk.Label(stats, textvariable=self.total_var, bg="#E0E7FF", fg="#1E3A8A", font=("Segoe UI", 10, "bold"), padx=10, pady=6); self.total_badge.pack(side="left", padx=(0,8))
        self.avg_badge   = tk.Label(stats, textvariable=self.avg_var,   bg="#FEF3C7", fg="#92400E", font=("Segoe UI", 10, "bold"), padx=10, pady=6); self.avg_badge.pack(side="left", padx=8)
        self.grade_badge = tk.Label(stats, textvariable=self.grade_var, bg="#DCFCE7", fg="#065F46", font=("Segoe UI", 10, "bold"), padx=10, pady=6); self.grade_badge.pack(side="left", padx=8)

        self.banner = tk.Label(right, text="", bg="#10B981", fg="white", font=("Segoe UI", 11, "bold"))  # L19: celebration banner (hidden by default)
        self.banner.pack(fill="x", padx=6, pady=(8,0)); self.banner.pack_for_ld = self.banner.pack_forget; self.banner.pack_forget()

        helper = ttk.Label(right, text="Tip: Click a row to auto-fill inputs. Use Search with Roll/Name; try Show Topper!", style="Muted.TLabel", wraplength=700, justify="left")
        helper.pack(anchor="w", pady=(8,0), padx=6)
        # <<< LESSON 22 END >>>

    def _bind_events(self):
        self.tree.bind("<<TreeviewSelect>>", self.on_select_record)

    # -------------------- Internals: find/parse/refresh ---------------------
    def _find_student_index_by_roll(self, roll: str) -> Optional[int]:
        for i, st in enumerate(self.students):
            if st.roll == roll: return i
        return None

    # <<< LESSON 15 START: VALIDATION / PARSING OF MARKS >>> 
    def _parse_marks(self, m1: str, m2: str, m3: str) -> List[int]:
        try:
            nums = [int(m1), int(m2), int(m3)]
        except ValueError:
            raise ValueError("Marks must be integers (0–100).")
        for n in nums:
            if n < 0 or n > 100:
                raise ValueError("Marks must be between 0 and 100.")
        return nums
    # <<< LESSON 15 END >>>

    # <<< LESSON 16 START: TABLE REFRESH HELPER >>> 
    def _refresh_tree(self, keep_selection: bool = False):
        selection = self.tree.selection(); selected_id = selection[0] if selection else None
        for iid in self.tree.get_children():
            self.tree.delete(iid)
        for st in self.students:
            tag = st.grade()
            self.tree.insert("", "end", iid=st.roll,
                             values=(st.roll, st.name, st.marks[0], st.marks[1], st.marks[2],
                                     st.total(), st.average(), st.grade()),
                             tags=(tag,))
        if keep_selection and selected_id and self.tree.exists(selected_id):
            self.tree.selection_set(selected_id); self.tree.see(selected_id)
    # <<< LESSON 16 END >>>

    # <<< LESSON 22 START: UPDATE BADGES (UI FEEDBACK) >>> 
    def _update_badges_for(self, st: Optional[Student]):
        if not st:
            self.total_var.set("Total: —"); self.avg_var.set("Average: —"); self.grade_var.set("Grade: —")
            self.grade_badge.configure(bg="#E5E7EB", fg="#111827")
            return
        self.total_var.set(f"Total: {st.total()}"); self.avg_var.set(f"Average: {st.average()}")
        g = st.grade(); self.grade_var.set(f"Grade: {g}")
        fg, bg = GRADE_TAGS.get(g, ("#111827", "#E5E7EB")); self.grade_badge.configure(bg=bg, fg=fg)
    # <<< LESSON 22 END >>>

    # ------------------------- Event handlers -------------------------------
    # <<< LESSON 17 START: ROW SELECTION AUTO-FILL (UX FOR CRUD) >>> 
    def on_select_record(self, _evt=None):
        sel = self.tree.selection()
        if not sel: return
        roll = sel[0]
        idx = self._find_student_index_by_roll(roll)
        if idx is None: return
        st = self.students[idx]
        self.roll_var.set(st.roll); self.name_var.set(st.name)
        self.m1_var.set(str(st.marks[0])); self.m2_var.set(str(st.marks[1])); self.m3_var.set(str(st.marks[2]))
        self._update_badges_for(st)
    # <<< LESSON 17 END >>>

    # <<< LESSON 17 START: CLEAR / RESET INPUTS (NOT DATA) >>> 
    def clear_inputs(self):
        self.roll_var.set(""); self.name_var.set("")
        self.m1_var.set(""); self.m2_var.set(""); self.m3_var.set("")
        self.tree.selection_remove(self.tree.selection())
        self._update_badges_for(None)
    # <<< LESSON 17 END >>>

    # <<< LESSON 23 START: RESET ALL DATA (SHOWCASE/DEBUGGING) >>> 
    def reset_all(self):
        if messagebox.askyesno("Reset All", "This will remove ALL student records. Continue?"):
            self.students.clear(); self._refresh_tree(); self.clear_inputs()
    # <<< LESSON 23 END >>>

    # <<< LESSON 17 + 15 START: ADD/UPDATE WITH VALIDATION >>> 
    def add_or_update_student(self):
        roll = self.roll_var.get().strip(); name = self.name_var.get().strip()
        try:
            if not roll: raise ValueError("Roll number cannot be empty.")
            if not name: raise ValueError("Name cannot be empty.")
            marks = self._parse_marks(self.m1_var.get(), self.m2_var.get(), self.m3_var.get())
            idx = self._find_student_index_by_roll(roll)
            if idx is None:
                st = Student(roll=roll, name=name, marks=marks); self.students.append(st)
                messagebox.showinfo("Added", f"Student added: {roll} — {name}")
            else:
                st = self.students[idx]; st.name = name; st.marks = marks
                messagebox.showinfo("Updated", f"Student updated: {roll} — {name}")
            self._refresh_tree(); self.tree.selection_set(roll); self.tree.see(roll)
            self._update_badges_for(self.students[self._find_student_index_by_roll(roll)])
        except Exception as e:
            messagebox.showerror("Input Error", str(e))
    # <<< LESSON 17 + 15 END >>>

    # <<< LESSON 17 START: DELETE WITH CONFIRMATION >>> 
    def delete_student(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select Record", "Please select a record to delete."); return
        roll = sel[0]; idx = self._find_student_index_by_roll(roll)
        if idx is None: return
        st = self.students[idx]
        if messagebox.askyesno("Delete", f"Delete {st.roll} — {st.name}?"):
            del self.students[idx]; self._refresh_tree(); self.clear_inputs()
    # <<< LESSON 17 END >>>

    # <<< LESSON 18 START: SEARCH (ROLL/NAME SUBSTRING) >>> 
    def search_student(self):
        query = self.roll_var.get().strip() or self.name_var.get().strip()
        if not query:
            messagebox.showinfo("Search", "Type a Roll No. or Name (or part) in inputs, then click Search."); return
        q = query.lower(); self.tree.selection_remove(self.tree.selection())
        hits = [st.roll for st in self.students if q in st.roll.lower() or q in st.name.lower()]
        if not hits:
            messagebox.showinfo("Search", f"No matches for \"{query}\"."); self._update_badges_for(None); return
        for rid in hits: self.tree.selection_add(rid); self.tree.see(rid)
        if len(hits) == 1:
            idx = self._find_student_index_by_roll(hits[0])
            if idx is not None: self._update_badges_for(self.students[idx])
        else:
            self._update_badges_for(None)
    # <<< LESSON 18 END >>>

    # <<< LESSON 19 START: TOPPER + IN-WINDOW CELEBRATION >>> 
    def _show_banner(self, text: str, color="#10B981", timeout=1400):
        """L19: Show an in-window celebration/info banner that auto-hides."""
        self.banner.configure(text=text, bg=color)
        self.banner.pack(fill="x", padx=6, pady=(8,0))
        self.after(timeout, lambda: self.banner.pack_forget())

    def show_topper(self):
        if not self.students:
            messagebox.showinfo("Topper", "No records available."); return
        topper_idx = max(range(len(self.students)), key=lambda i: self.students[i].average())
        topper = self.students[topper_idx]
        messagebox.showinfo("Topper", f"Topper: {topper.roll} — {topper.name}\nAverage: {topper.average()} | Grade: {topper.grade()}")
        self.tree.selection_set(topper.roll); self.tree.see(topper.roll); self._update_badges_for(topper)
        self._show_banner(f"🎉 Topper: {topper.name}!")
    # <<< LESSON 19 END >>>

    # <<< LESSON 20 START: SAVE / LOAD CSV >>> 
    def save_to_csv(self):
        if not self.students:
            messagebox.showwarning("Save CSV", "No records to save."); return
        path = filedialog.asksaveasfilename(title="Save CSV", defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not path: return
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["roll","name","marks1","marks2","marks3","total","average","grade"])
                for st in self.students:
                    writer.writerow([st.roll, st.name, st.marks[0], st.marks[1], st.marks[2], st.total(), st.average(), st.grade()])
            messagebox.showinfo("Saved", f"Saved {len(self.students)} records to:\n{path}")
        except PermissionError:
            messagebox.showerror("Permission Denied", "Close the file if it is open elsewhere and try again.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save file:\n{e}")

    def load_from_csv(self):
        path = filedialog.askopenfilename(title="Load CSV", filetypes=[("CSV files", "*.csv")])
        if not path: return
        try:
            loaded: List[Student] = []
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.reader(f); header = next(reader, None)
                if not header or len(header) < 8: raise ValueError("Unexpected CSV format. Expected 8 columns.")
                for i, row in enumerate(reader, start=2):
                    if len(row) < 8: raise ValueError(f"Row {i} is malformed: {row}")
                    roll = row[0].strip(); name = row[1].strip()
                    try:
                        m1, m2, m3 = int(row[2]), int(row[3]), int(row[4])
                    except ValueError:
                        raise ValueError(f"Row {i}: marks must be integers.")
                    for m in (m1, m2, m3):
                        if m < 0 or m > 100: raise ValueError(f"Row {i}: marks out of range 0–100.")
                    loaded.append(Student(roll=roll, name=name, marks=[m1, m2, m3]))
            self.students = loaded; self._refresh_tree(); self.clear_inputs()
            messagebox.showinfo("Loaded", f"Loaded {len(self.students)} records from:\n{path}")
        except Exception as e:
            messagebox.showerror("Load Error", f"Could not load file:\n{e}")
    # <<< LESSON 20 END >>>

    # <<< LESSON 21 START: EXPORT TXT REPORT WITH REMARK >>> 
    def export_report(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Export", "Please select a student record first."); return
        roll = sel[0]; idx = self._find_student_index_by_roll(roll)
        if idx is None: return
        st = self.students[idx]
        default_filename = f"report_{st.roll}_{st.name.replace(' ', '_')}.txt"
        path = filedialog.asksaveasfilename(title="Export Report", initialfile=default_filename, defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not path: return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("=== Student Report Card ===\n")
                f.write(f"Roll No.: {st.roll}\n")
                f.write(f"Name    : {st.name}\n")
                f.write(f"Marks   : {st.marks}\n")
                f.write(f"Total   : {st.total()}\n")
                f.write(f"Average : {st.average()}\n")
                f.write(f"Grade   : {st.grade()}\n")
                remark = ("Excellent" if st.grade() in ("A+","A")
                          else "Good" if st.grade()=="B"
                          else "Average" if st.grade()=="C"
                          else "Needs Improvement" if st.grade()=="D"
                          else "Fail")
                f.write(f"Remark  : {remark}\n")
            messagebox.showinfo("Exported", f"Report saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not export report:\n{e}")
    # <<< LESSON 21 END >>>
# <<< L14–L23 END: TRACKER TAB (MAIN PROJECT UI) >>>


# --------------- Activities Frame: all demos in one tab ---------------------
# <<< L13–L22 ACTIVITIES START: SUB-TABS FOR EACH ADDITIONAL ACTIVITY >>>
class ActivitiesFrame(ttk.Frame):
    """Contains a sub-notebook with one tab per activity (L13–L22).
    ILOs are supported with small, focused demos that reinforce each lesson.
    """
    def __init__(self, parent):
        super().__init__(parent, style="TFrame")
        # Sub-notebook for activities
        self.nb = ttk.Notebook(self); self.nb.pack(fill="both", expand=True)

        # Build each activity tab
        self._build_l13(); self._build_l14(); self._build_l15(); self._build_l16()
        self._build_l17(); self._build_l18(); self._build_l19(); self._build_l20()
        self._build_l21(); self._build_l22()

    # <<< LESSON 13 ACTIVITY START: LibraryRecord dataclass demo >>> 
    def _build_l13(self):
        tab = ttk.Frame(self.nb, style="TFrame"); self.nb.add(tab, text="L13 LibraryRecord")
        ttk.Label(tab, text="Lesson 13: LibraryRecord dataclass demo", style="Header.TLabel").pack(anchor="w", padx=10, pady=(10,4))

        # Inner frame for output
        out = tk.Text(tab, height=6); out.pack(fill="x", padx=10, pady=(4,10))

        @dataclass
        class LibraryRecord:
            title: str; author: str; year: int

        def run_demo():
            rec = LibraryRecord(title="A Wrinkle in Time", author="Madeleine L'Engle", year=1962)
            out.delete("1.0", "end")
            out.insert("end", f"Library Record: {rec}\n")

        ttk.Button(tab, text="Run Demo", command=run_demo).pack(padx=10, pady=(0,10))
    # <<< LESSON 13 ACTIVITY END >>>

    # <<< LESSON 14 ACTIVITY START: Welcome label (embedded) >>> 
    def _build_l14(self):
        tab = ttk.Frame(self.nb, style="TFrame"); self.nb.add(tab, text="L14 Welcome")
        ttk.Label(tab, text="Lesson 14: Minimal Welcome Window (embedded)", style="Header.TLabel").pack(anchor="w", padx=10, pady=(10,8))
        ttk.Label(tab, text="Welcome to Python GUI", font=("Segoe UI", 14, "bold")).pack(padx=10, pady=12)
    # <<< LESSON 14 ACTIVITY END >>>

    # <<< LESSON 15 ACTIVITY START: Positive/Negative checker >>> 
    def _build_l15(self):
        tab = ttk.Frame(self.nb, style="TFrame"); self.nb.add(tab, text="L15 Pos/Neg")
        ttk.Label(tab, text="Lesson 15: Positive/Negative Checker", style="Header.TLabel").pack(anchor="w", padx=10, pady=(10,4))
        frm = ttk.Frame(tab); frm.pack(padx=10, pady=8, anchor="w")
        ttk.Label(frm, text="Enter a number:").grid(row=0, column=0, padx=4)
        val = tk.StringVar(); ent = ttk.Entry(frm, textvariable=val, width=12); ent.grid(row=0, column=1, padx=4)
        msg = ttk.Label(frm, text=""); msg.grid(row=0, column=2, padx=8)
        def check():
            try: n = int(val.get().strip()); msg.configure(text=("Positive" if n >= 0 else "Negative"))
            except ValueError: msg.configure(text="Enter integer")
        ttk.Button(frm, text="Check", command=check).grid(row=0, column=3, padx=6)
    # <<< LESSON 15 ACTIVITY END >>>

    # <<< LESSON 16 ACTIVITY START: Books Treeview >>> 
    def _build_l16(self):
        tab = ttk.Frame(self.nb, style="TFrame"); self.nb.add(tab, text="L16 Books Table")
        ttk.Label(tab, text="Lesson 16: Books Table (Treeview)", style="Header.TLabel").pack(anchor="w", padx=10, pady=(10,4))
        tree = ttk.Treeview(tab, columns=("title","author"), show="headings"); tree.pack(fill="both", expand=True, padx=10, pady=10)
        tree.heading("title", text="Title"); tree.heading("author", text="Author")
        data = [("The Giver","Lois Lowry"), ("Charlotte's Web","E. B. White"), ("Holes","Louis Sachar"), ("Wonder","R. J. Palacio"), ("A Wrinkle in Time","Madeleine L'Engle")]
        for t,a in data: tree.insert("", "end", values=(t,a))
    # <<< LESSON 16 ACTIVITY END >>>

    # <<< LESSON 17 ACTIVITY START: Grocery CRUD >>> 
    def _build_l17(self):
        tab = ttk.Frame(self.nb, style="TFrame"); self.nb.add(tab, text="L17 Grocery CRUD")
        ttk.Label(tab, text="Lesson 17: List CRUD (Add/Delete)", style="Header.TLabel").pack(anchor="w", padx=10, pady=(10,4))
        frm = ttk.Frame(tab); frm.pack(fill="x", padx=10, pady=8)
        ent = ttk.Entry(frm); ent.grid(row=0, column=0, padx=4)
        lb = tk.Listbox(frm, height=8); lb.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=8)
        frm.grid_columnconfigure(0, weight=1); frm.grid_rowconfigure(1, weight=1)
        def add_item():
            item = ent.get().strip()
            if item:
                lb.insert("end", item); ent.delete(0,"end")
        def delete_item():
            sel = lb.curselection()
            if sel: lb.delete(sel[0])
        ttk.Button(frm, text="Add", command=add_item).grid(row=0, column=1, padx=4)
        ttk.Button(frm, text="Delete", command=delete_item).grid(row=0, column=2, padx=4)
    # <<< LESSON 17 ACTIVITY END >>>

    # <<< LESSON 18 ACTIVITY START: State search >>> 
    def _build_l18(self):
        tab = ttk.Frame(self.nb, style="TFrame"); self.nb.add(tab, text="L18 State Search")
        ttk.Label(tab, text="Lesson 18: Search in a List", style="Header.TLabel").pack(anchor="w", padx=10, pady=(10,4))
        frm = ttk.Frame(tab); frm.pack(padx=10, pady=8, anchor="w")
        ttk.Label(frm, text="Search state:").grid(row=0, column=0, padx=4)
        val = tk.StringVar(); ent = ttk.Entry(frm, textvariable=val); ent.grid(row=0, column=1, padx=4)
        msg = ttk.Label(frm, text=""); msg.grid(row=0, column=2, padx=8)
        states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut"]
        def do_search():
            q = val.get().strip().lower()
            res = [s for s in states if q and q in s.lower()]
            msg.configure(text="Found: " + (", ".join(res) if res else "No match"))
        ttk.Button(frm, text="Search", command=do_search).grid(row=0, column=3, padx=6)
    # <<< LESSON 18 ACTIVITY END >>>

    # <<< LESSON 19 ACTIVITY START: Highest Science >>> 
    def _build_l19(self):
        tab = ttk.Frame(self.nb, style="TFrame"); self.nb.add(tab, text="L19 Highest Science")
        ttk.Label(tab, text="Lesson 19: Highest Science Score", style="Header.TLabel").pack(anchor="w", padx=10, pady=(10,4))
        out = tk.Text(tab, height=6); out.pack(fill="x", padx=10, pady=8)
        def run_demo():
            records = [{"name":"Aarav","Science":88},{"name":"Ishita","Science":94},{"name":"Rohan","Science":76},{"name":"Meera","Science":89}]
            top = max(records, key=lambda r: r["Science"])
            out.delete("1.0","end"); out.insert("end", f"Highest in Science: {top['name']} with {top['Science']}\n")
        ttk.Button(tab, text="Run Demo", command=run_demo).pack(padx=10, pady=(0,10))
    # <<< LESSON 19 ACTIVITY END >>>

    # <<< LESSON 20 ACTIVITY START: Shopping CSV >>> 
    def _build_l20(self):
        tab = ttk.Frame(self.nb, style="TFrame"); self.nb.add(tab, text="L20 Shopping CSV")
        ttk.Label(tab, text="Lesson 20: Save & Load a CSV", style="Header.TLabel").pack(anchor="w", padx=10, pady=(10,4))
        status = ttk.Label(tab, text="Status: —"); status.pack(anchor="w", padx=10)
        items_box = tk.Text(tab, height=6); items_box.pack(fill="x", padx=10, pady=8)
        def save_demo():
            items = ["Milk","Bread","Eggs"]
            path = "shopping.csv"
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f); w.writerow(["item"]); [w.writerow([i]) for i in items]
            status.configure(text=f"Saved to {path}")
        def load_demo():
            loaded = []
            try:
                with open("shopping.csv", "r", encoding="utf-8") as f:
                    r = csv.reader(f); next(r, None)
                    for row in r:
                        if row: loaded.append(row[0])
                items_box.delete("1.0","end"); items_box.insert("end", "Loaded: " + ", ".join(loaded))
                status.configure(text="Loaded shopping.csv")
            except FileNotFoundError:
                status.configure(text="shopping.csv not found. Click Save first.")
        btns = ttk.Frame(tab); btns.pack(anchor="w", padx=10, pady=4)
        ttk.Button(btns, text="Save CSV", command=save_demo).grid(row=0, column=0, padx=4)
        ttk.Button(btns, text="Load CSV", command=load_demo).grid(row=0, column=1, padx=4)
    # <<< LESSON 20 ACTIVITY END >>>

    # <<< LESSON 21 ACTIVITY START: Weekly Homework TXT >>> 
    def _build_l21(self):
        tab = ttk.Frame(self.nb, style="TFrame"); self.nb.add(tab, text="L21 Homework TXT")
        ttk.Label(tab, text="Lesson 21: Weekly Homework Text File", style="Header.TLabel").pack(anchor="w", padx=10, pady=(10,4))
        status = ttk.Label(tab, text="Status: —"); status.pack(anchor="w", padx=10)
        def write_txt():
            schedule = ["Mon: Math worksheet","Tue: Science reading","Wed: Python practice","Thu: History notes","Fri: Art sketch"]
            with open("weekly_homework.txt","w",encoding="utf-8") as f:
                f.write("=== Weekly Homework ===\n")
                for line in schedule: f.write(line+"\n")
            status.configure(text="Created weekly_homework.txt")
        ttk.Button(tab, text="Create File", command=write_txt).pack(anchor="w", padx=10, pady=6)
    # <<< LESSON 21 ACTIVITY END >>>

    # <<< LESSON 22 ACTIVITY START: Style header preview >>> 
    def _build_l22(self):
        tab = ttk.Frame(self.nb, style="TFrame"); self.nb.add(tab, text="L22 Style Demo")
        ttk.Label(tab, text="Lesson 22: Header Style Preview", style="Header.TLabel").pack(anchor="w", padx=10, pady=(10,4))
        c = tk.Canvas(tab, height=80, highlightthickness=0); c.pack(fill="x", padx=10, pady=8)
        c.create_rectangle(0,0,1000,40, fill=PALETTE["header_start"], outline="")
        c.create_rectangle(0,40,1000,80, fill=PALETTE["header_mid"], outline="")
        ttk.Label(tab, text="Styled header preview (embedded)").pack(anchor="w", padx=10)
    # <<< LESSON 22 ACTIVITY END >>>
# <<< L13–L22 ACTIVITIES END >>>


# ------------------------------ Entrypoint ----------------------------------
# <<< LESSON 23 START: FINAL INTEGRATION & SHOWCASE (MAIN ENTRY) >>> 
def main():
    app = UnifiedApp()  # Create and show the unified window
    app.mainloop()

if __name__ == "__main__":
    main()
# <<< LESSON 23 END >>>
