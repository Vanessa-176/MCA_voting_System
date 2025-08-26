# requirements.txt
# customtkinter==5.2.0
# mysql-connector-python==8.1.0
# Pillow==10.0.0

import customtkinter as ctk
import mysql.connector
from mysql.connector import Error
import tkinter.messagebox as messagebox
from tkinter import ttk
import hashlib
from datetime import datetime
import threading
from typing import Optional, List, Dict, Any

# Set appearance mode and color theme
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class DatabaseManager:
    """Handles database connections and operations"""
    
    def __init__(self):
        self.host = "localhost"
        self.database = "mca_voting_system"
        self.user = "root"
        self.password = ""
        self.connection = None
    
    def connect(self) -> bool:
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return True
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[List[tuple]]:
        """Execute SELECT query and return results"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return None
            
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            messagebox.showerror("Database Error", f"Query execution failed: {e}")
            return None
    
    def execute_update(self, query: str, params: tuple = None) -> bool:
        """Execute INSERT, UPDATE, DELETE queries"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return False
            
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            messagebox.showerror("Database Error", f"Update execution failed: {e}")
            return False


class User:
    """User model for authentication"""
    
    def __init__(self, user_id: int, username: str, email: str, full_name: str, role: str):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.full_name = full_name
        self.role = role


class AuthService:
    """Handles user authentication"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate user credentials"""
        # Hash the password (assuming bcrypt-like hashing in production)
        # For demo purposes, we'll check against stored hash
        query = """
        SELECT id, username, email, full_name, role 
        FROM admin_users 
        WHERE username = %s AND is_active = 1
        """
        
        result = self.db_manager.execute_query(query, (username,))
        
        if result:
            user_data = result[0]
            # In production, properly verify hashed password
            # For demo, we'll assume password verification passed
            return User(*user_data)
        
        return None


class DashboardMetrics:
    """Calculate dashboard metrics"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_total_students(self) -> int:
        """Get total number of registered students"""
        query = "SELECT COUNT(*) FROM students WHERE is_active = 1"
        result = self.db_manager.execute_query(query)
        return result[0][0] if result else 0
    
    def get_total_candidates(self) -> int:
        """Get total number of candidates"""
        query = "SELECT COUNT(*) FROM candidates WHERE is_active = 1"
        result = self.db_manager.execute_query(query)
        return result[0][0] if result else 0
    
    def get_total_votes(self) -> int:
        """Get total number of votes cast"""
        query = "SELECT COUNT(*) FROM votes"
        result = self.db_manager.execute_query(query)
        return result[0][0] if result else 0
    
    def get_voter_turnout(self) -> float:
        """Calculate voter turnout percentage"""
        total_students = self.get_total_students()
        voted_students = self.db_manager.execute_query("SELECT COUNT(DISTINCT student_id) FROM votes")
        
        if total_students > 0 and voted_students:
            return (voted_students[0][0] / total_students) * 100
        return 0.0
    
    def get_position_vote_counts(self) -> List[Dict[str, Any]]:
        """Get vote counts per position"""
        query = """
        SELECT p.position_name, COUNT(v.id) as vote_count
        FROM positions p
        LEFT JOIN votes v ON p.id = v.position_id
        WHERE p.is_active = 1
        GROUP BY p.id, p.position_name
        ORDER BY p.display_order
        """
        
        result = self.db_manager.execute_query(query)
        return [{"position": row[0], "votes": row[1]} for row in result] if result else []


class LoginPage(ctk.CTkFrame):
    """Login page UI"""
    
    def __init__(self, parent, auth_service: AuthService, on_login_success):
        super().__init__(parent)
        self.auth_service = auth_service
        self.on_login_success = on_login_success
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup login UI components"""
        # Center the login form
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Login frame
        login_frame = ctk.CTkFrame(self, width=400, height=300)
        login_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        login_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(login_frame, text="MCA Voting System", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        subtitle_label = ctk.CTkLabel(login_frame, text="Admin Login", 
                                     font=ctk.CTkFont(size=16))
        subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 20))
        
        # Username field
        self.username_entry = ctk.CTkEntry(login_frame, placeholder_text="Username", width=300)
        self.username_entry.grid(row=2, column=0, padx=20, pady=10)
        
        # Password field
        self.password_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", 
                                          show="*", width=300)
        self.password_entry.grid(row=3, column=0, padx=20, pady=10)
        
        # Login button
        login_button = ctk.CTkButton(login_frame, text="Login", command=self.login, width=300)
        login_button.grid(row=4, column=0, padx=20, pady=(20, 10))
        
        # Bind Enter key to login
        self.username_entry.bind("<Return>", lambda e: self.login())
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # Focus on username field
        self.username_entry.focus()
    
    def login(self):
        """Handle login attempt"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Authenticate user
        user = self.auth_service.authenticate(username, password)
        
        if user:
            self.on_login_success(user)
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_entry.delete(0, "end")


class Sidebar(ctk.CTkFrame):
    """Navigation sidebar"""
    
    def __init__(self, parent, on_page_select):
        super().__init__(parent, width=200)
        self.on_page_select = on_page_select
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup sidebar UI"""
        self.grid_rowconfigure(20, weight=1)  # Spacer
        
        # Title
        title_label = ctk.CTkLabel(self, text="Navigation", 
                                  font=ctk.CTkFont(size=18, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(20, 30), sticky="w")
        
        # Navigation buttons
        nav_items = [
            ("Dashboard", "dashboard"),
            ("Students", "students"),
            ("Candidates", "candidates"),
            ("Positions", "positions"),
            ("Votes", "votes"),
            ("Settings", "settings"),
            ("Admin Users", "admin_users")
        ]
        
        self.nav_buttons = {}
        for i, (text, page_id) in enumerate(nav_items, 1):
            btn = ctk.CTkButton(self, text=text, command=lambda p=page_id: self.select_page(p),
                               width=160, height=35)
            btn.grid(row=i, column=0, padx=20, pady=5, sticky="w")
            self.nav_buttons[page_id] = btn
        
        # Logout button
        logout_btn = ctk.CTkButton(self, text="Logout", command=self.logout,
                                  width=160, height=35, fg_color="red", hover_color="darkred")
        logout_btn.grid(row=21, column=0, padx=20, pady=(20, 20), sticky="w")
        
        # NOTE: do NOT call self.select_page here — parent will show default page
    def select_page(self, page_id: str):
        """Handle page selection"""
        # Reset all button colors
        for btn in self.nav_buttons.values():
            btn.configure(fg_color=("gray75", "gray25"))
        
        # Highlight selected button
        if page_id in self.nav_buttons:
            self.nav_buttons[page_id].configure(fg_color=("blue", "blue"))
        
        # Notify parent
        self.on_page_select(page_id)
    
    def logout(self):
        """Handle logout"""
        self.on_page_select("logout")


class DashboardPage(ctk.CTkFrame):
    """Dashboard page with metrics"""
    
    def __init__(self, parent, db_manager: DatabaseManager):
        super().__init__(parent)
        self.db_manager = db_manager
        self.metrics = DashboardMetrics(db_manager)
        
        self.setup_ui()
        self.load_metrics()
    
    def setup_ui(self):
        """Setup dashboard UI"""
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(self, text="Dashboard", 
                                  font=ctk.CTkFont(size=28, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")
        
        # Metrics frame
        metrics_frame = ctk.CTkFrame(self)
        metrics_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        metrics_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Metric cards
        self.total_students_label = self.create_metric_card(metrics_frame, "Total Students", "0", 0)
        self.total_candidates_label = self.create_metric_card(metrics_frame, "Total Candidates", "0", 1)
        self.total_votes_label = self.create_metric_card(metrics_frame, "Total Votes", "0", 2)
        self.turnout_label = self.create_metric_card(metrics_frame, "Voter Turnout", "0%", 3)
        
        # Position votes frame
        votes_frame = ctk.CTkFrame(self)
        votes_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        votes_frame.grid_columnconfigure(0, weight=1)
        votes_frame.grid_rowconfigure(1, weight=1)
        
        votes_title = ctk.CTkLabel(votes_frame, text="Votes by Position", 
                                  font=ctk.CTkFont(size=18, weight="bold"))
        votes_title.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        # Votes treeview
        self.votes_tree = ttk.Treeview(votes_frame, columns=("Position", "Votes"), show="headings", height=10)
        self.votes_tree.heading("Position", text="Position")
        self.votes_tree.heading("Votes", text="Votes Cast")
        self.votes_tree.column("Position", width=200)
        self.votes_tree.column("Votes", width=100)
        self.votes_tree.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        # Refresh button
        refresh_btn = ctk.CTkButton(self, text="Refresh Data", command=self.load_metrics)
        refresh_btn.grid(row=3, column=0, padx=20, pady=10, sticky="w")
    
    def create_metric_card(self, parent, title: str, value: str, column: int) -> ctk.CTkLabel:
        """Create a metric card"""
        card_frame = ctk.CTkFrame(parent)
        card_frame.grid(row=0, column=column, padx=10, pady=10, sticky="ew")
        
        title_label = ctk.CTkLabel(card_frame, text=title, font=ctk.CTkFont(size=14))
        title_label.grid(row=0, column=0, padx=20, pady=(15, 5))
        
        value_label = ctk.CTkLabel(card_frame, text=value, font=ctk.CTkFont(size=24, weight="bold"))
        value_label.grid(row=1, column=0, padx=20, pady=(5, 15))
        
        return value_label
    
    def load_metrics(self):
        """Load and display metrics"""
        # Fetch data in background, then update UI via .after (thread-safe)
        def fetch_data():
            try:
                total_students = self.metrics.get_total_students()
                total_candidates = self.metrics.get_total_candidates()
                total_votes = self.metrics.get_total_votes()
                turnout = self.metrics.get_voter_turnout()
                position_votes = self.metrics.get_position_vote_counts()
            except Exception as e:
                # Schedule an error message on the main thread if needed
                def _err():
                    messagebox.showerror("Error", f"Failed to load metrics: {e}")
                self.after(0, _err)
                return
            
            def update_ui():
                # Update metric cards
                self.total_students_label.configure(text=str(total_students))
                self.total_candidates_label.configure(text=str(total_candidates))
                self.total_votes_label.configure(text=str(total_votes))
                self.turnout_label.configure(text=f"{turnout:.1f}%")
                
                # Update votes by position
                for item in self.votes_tree.get_children():
                    self.votes_tree.delete(item)
                
                for data in position_votes:
                    self.votes_tree.insert("", "end", values=(data["position"], data["votes"]))
            
            self.after(0, update_ui)
        
        threading.Thread(target=fetch_data, daemon=True).start()


class StudentsPage(ctk.CTkFrame):
    """Students management page"""
    
    def __init__(self, parent, db_manager: DatabaseManager):
        super().__init__(parent)
        self.db_manager = db_manager
        
        self.setup_ui()
        self.load_students()
    
    def setup_ui(self):
        """Setup students page UI"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Title and controls
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1)
        
        title_label = ctk.CTkLabel(header_frame, text="Students Management", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        refresh_btn = ctk.CTkButton(header_frame, text="Refresh", command=self.load_students)
        refresh_btn.grid(row=0, column=2, padx=20, pady=20, sticky="e")
        
        # Students table
        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        columns = ("ID", "Student ID", "Full Name", "Email", "Program", "Year", "Has Voted", "Status")
        self.students_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.students_tree.yview)
        self.students_tree.configure(yscrollcommand=scrollbar.set)
        
        self.students_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
    
    def load_students(self):
        """Load students data"""
        # Clear existing data
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        query = """
        SELECT id, student_id, full_name, email, program, year_of_study, 
               has_voted, is_active 
        FROM students 
        ORDER BY student_id
        """
        
        result = self.db_manager.execute_query(query)
        if result:
            for row in result:
                # Convert boolean values to readable text
                has_voted = "Yes" if row[6] else "No"
                is_active = "Active" if row[7] else "Inactive"
                
                display_row = (*row[:6], has_voted, is_active)
                self.students_tree.insert("", "end", values=display_row)


class CandidatesPage(ctk.CTkFrame):
    """Candidates management page with basic CRUD"""
    def __init__(self, parent, db_manager: DatabaseManager):
        super().__init__(parent)
        self.db_manager = db_manager
        self.positions = []
        self.setup_ui()
        self.load_positions()
        self.load_candidates()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        header.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(header, text="Candidates Management", font=ctk.CTkFont(size=20, weight="bold"))
        title.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        btn_frame = ctk.CTkFrame(header)
        btn_frame.grid(row=0, column=2, sticky="e", padx=10)
        add_btn = ctk.CTkButton(btn_frame, text="Add", command=self.add_candidate)
        edit_btn = ctk.CTkButton(btn_frame, text="Edit", command=self.edit_candidate)
        del_btn = ctk.CTkButton(btn_frame, text="Delete", command=self.delete_candidate)
        refresh_btn = ctk.CTkButton(btn_frame, text="Refresh", command=self.load_candidates)
        add_btn.grid(row=0, column=0, padx=5)
        edit_btn.grid(row=0, column=1, padx=5)
        del_btn.grid(row=0, column=2, padx=5)
        refresh_btn.grid(row=0, column=3, padx=5)

        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0,20))
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        cols = ("ID","Name","Student ID","Position","Program","Year","Status")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def load_positions(self):
        q = "SELECT id, position_name FROM positions WHERE is_active = 1 ORDER BY display_order"
        res = self.db_manager.execute_query(q)
        self.positions = res if res else []

    def load_candidates(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        q = """
        SELECT c.id, c.candidate_name, c.student_id, p.position_name, c.program, c.year_of_study, c.is_active
        FROM candidates c
        LEFT JOIN positions p ON c.position_id = p.id
        ORDER BY p.display_order, c.candidate_name
        """
        res = self.db_manager.execute_query(q)
        if not res:
            return
        for r in res:
            status = "Active" if r[6] else "Inactive"
            self.tree.insert("", "end", values=(r[0], r[1], r[2], r[3] or "", r[4], r[5], status))

    def _open_candidate_modal(self, title="New Candidate", data=None):
        modal = ctk.CTkToplevel(self)
        modal.title(title)
        modal.geometry("420x360")
        modal.resizable(False, False)

        labels = ["Name","Student ID","Position","Program","Year","Active"]
        entries = {}

        ctk.CTkLabel(modal, text=title, font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10,5))
        frame = ctk.CTkFrame(modal)
        frame.pack(padx=10, pady=5, fill="both", expand=True)

        # Name
        ctk.CTkLabel(frame, text="Name").grid(row=0,column=0,sticky="w", padx=5, pady=5)
        entries["name"] = ctk.CTkEntry(frame, width=300)
        entries["name"].grid(row=0,column=1,padx=5,pady=5)

        # Student ID
        ctk.CTkLabel(frame, text="Student ID").grid(row=1,column=0,sticky="w", padx=5, pady=5)
        entries["student_id"] = ctk.CTkEntry(frame, width=300)
        entries["student_id"].grid(row=1,column=1,padx=5,pady=5)

        # Position (combo)
        ctk.CTkLabel(frame, text="Position").grid(row=2,column=0,sticky="w", padx=5, pady=5)
        pos_names = [p[1] for p in self.positions] or []
        entries["position"] = ttk.Combobox(frame, values=pos_names, state="readonly")
        entries["position"].grid(row=2,column=1,padx=5,pady=5)

        # Program
        ctk.CTkLabel(frame, text="Program").grid(row=3,column=0,sticky="w", padx=5, pady=5)
        entries["program"] = ctk.CTkEntry(frame, width=300)
        entries["program"].grid(row=3,column=1,padx=5,pady=5)

        # Year
        ctk.CTkLabel(frame, text="Year").grid(row=4,column=0,sticky="w", padx=5, pady=5)
        entries["year"] = ctk.CTkEntry(frame, width=300)
        entries["year"].grid(row=4,column=1,padx=5,pady=5)

        # Active checkbox
        entries["active_var"] = ctk.BooleanVar(value=True)
        entries["active"] = ctk.CTkCheckBox(frame, text="Active", variable=entries["active_var"])
        entries["active"].grid(row=5,column=1,padx=5,pady=5, sticky="w")

        # Prefill if editing
        if data:
            entries["name"].insert(0, data.get("candidate_name",""))
            entries["student_id"].insert(0, data.get("student_id",""))
            if data.get("position_name"):
                entries["position"].set(data.get("position_name"))
            entries["program"].insert(0, data.get("program",""))
            entries["year"].insert(0, str(data.get("year_of_study","")))
            entries["active_var"].set(bool(data.get("is_active",1)))

        btn_frame = ctk.CTkFrame(modal)
        btn_frame.pack(pady=10)
        def on_save():
            name = entries["name"].get().strip()
            student_id = entries["student_id"].get().strip()
            pos = entries["position"].get().strip()
            program = entries["program"].get().strip()
            year = entries["year"].get().strip()
            active = 1 if entries["active_var"].get() else 0

            if not (name and student_id and pos):
                messagebox.showerror("Error", "Name, Student ID and Position are required")
                return

            # find position id
            pos_id = None
            for p in self.positions:
                if p[1] == pos:
                    pos_id = p[0]
                    break
            if pos_id is None:
                messagebox.showerror("Error", "Selected position not found")
                return

            if data:  # update
                q = """UPDATE candidates SET position_id=%s, candidate_name=%s, student_id=%s, program=%s, year_of_study=%s, is_active=%s WHERE id=%s"""
                ok = self.db_manager.execute_update(q, (pos_id, name, student_id, program, year or 0, active, data["id"]))
            else:  # insert
                q = """INSERT INTO candidates (position_id, candidate_name, student_id, program, year_of_study, is_active) VALUES (%s,%s,%s,%s,%s,%s)"""
                ok = self.db_manager.execute_update(q, (pos_id, name, student_id, program, year or 0, active))
            if ok:
                modal.destroy()
                self.load_candidates()

        save_btn = ctk.CTkButton(btn_frame, text="Save", command=on_save)
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=modal.destroy)
        save_btn.grid(row=0,column=0,padx=5)
        cancel_btn.grid(row=0,column=1,padx=5)

    def add_candidate(self):
        self.load_positions()
        self._open_candidate_modal("Add Candidate")

    def edit_candidate(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a candidate to edit")
            return
        vals = self.tree.item(sel[0], "values")
        data = {
            "id": vals[0],
            "candidate_name": vals[1],
            "student_id": vals[2],
            "position_name": vals[3],
            "program": vals[4],
            "year_of_study": vals[5],
            "is_active": 1 if vals[6]=="Active" else 0
        }
        self.load_positions()
        self._open_candidate_modal("Edit Candidate", data=data)

    def delete_candidate(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a candidate to delete")
            return
        vals = self.tree.item(sel[0], "values")
        cid = vals[0]
        if messagebox.askyesno("Confirm", "Delete selected candidate?"):
            q = "DELETE FROM candidates WHERE id=%s"
            ok = self.db_manager.execute_update(q, (cid,))
            if ok:
                self.load_candidates()

class PositionsPage(ctk.CTkFrame):
    """Positions management page"""
    def __init__(self, parent, db_manager: DatabaseManager):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setup_ui()
        self.load_positions()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        title = ctk.CTkLabel(header, text="Positions Management", font=ctk.CTkFont(size=20, weight="bold"))
        title.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        btn_frame = ctk.CTkFrame(header)
        btn_frame.grid(row=0, column=1, sticky="e", padx=10)
        ctk.CTkButton(btn_frame, text="Add", command=self.add_position).grid(row=0,column=0,padx=5)
        ctk.CTkButton(btn_frame, text="Edit", command=self.edit_position).grid(row=0,column=1,padx=5)
        ctk.CTkButton(btn_frame, text="Delete", command=self.delete_position).grid(row=0,column=2,padx=5)
        ctk.CTkButton(btn_frame, text="Refresh", command=self.load_positions).grid(row=0,column=3,padx=5)

        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0,20))
        cols = ("ID","Position","Description","Order","Active")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140)
        self.tree.grid(row=0,column=0,sticky="nsew")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0,column=1,sticky="ns")

    def load_positions(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        q = "SELECT id, position_name, position_description, display_order, is_active FROM positions ORDER BY display_order"
        res = self.db_manager.execute_query(q)
        if not res:
            return
        for r in res:
            self.tree.insert("", "end", values=(r[0], r[1], r[2] or "", r[3] or 0, "Active" if r[4] else "Inactive"))

    def _open_modal(self, title="Position", data=None):
        modal = ctk.CTkToplevel(self)
        modal.title(title)
        modal.geometry("480x320")
        frame = ctk.CTkFrame(modal)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=14, weight="bold")).grid(row=0,column=0,columnspan=2,pady=5)
        ctk.CTkLabel(frame, text="Name").grid(row=1,column=0,sticky="w", padx=5, pady=5)
        name = ctk.CTkEntry(frame, width=320); name.grid(row=1,column=1,padx=5,pady=5)
        ctk.CTkLabel(frame, text="Description").grid(row=2,column=0,sticky="w", padx=5, pady=5)
        desc = ctk.CTkEntry(frame, width=320); desc.grid(row=2,column=1,padx=5,pady=5)
        ctk.CTkLabel(frame, text="Order").grid(row=3,column=0,sticky="w", padx=5, pady=5)
        order = ctk.CTkEntry(frame, width=120); order.grid(row=3,column=1,padx=5,pady=5, sticky="w")
        active_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(frame, text="Active", variable=active_var).grid(row=4,column=1,padx=5,pady=5, sticky="w")

        if data:
            name.insert(0, data.get("position_name",""))
            desc.insert(0, data.get("position_description",""))
            order.insert(0, str(data.get("display_order","0")))
            active_var.set(bool(data.get("is_active",1)))

        def on_save():
            n = name.get().strip()
            d = desc.get().strip()
            o = order.get().strip() or 0
            a = 1 if active_var.get() else 0
            if not n:
                messagebox.showerror("Error", "Name required")
                return
            if data:
                q = "UPDATE positions SET position_name=%s, position_description=%s, display_order=%s, is_active=%s WHERE id=%s"
                ok = self.db_manager.execute_update(q, (n,d,o,a,data["id"]))
            else:
                q = "INSERT INTO positions (position_name, position_description, display_order, is_active) VALUES (%s,%s,%s,%s)"
                ok = self.db_manager.execute_update(q, (n,d,o,a))
            if ok:
                modal.destroy()
                self.load_positions()

        btn_frame = ctk.CTkFrame(modal); btn_frame.pack(pady=8)
        ctk.CTkButton(btn_frame, text="Save", command=on_save).grid(row=0,column=0,padx=6)
        ctk.CTkButton(btn_frame, text="Cancel", command=modal.destroy).grid(row=0,column=1,padx=6)

    def add_position(self):
        self._open_modal("Add Position")

    def edit_position(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a position to edit")
            return
        vals = self.tree.item(sel[0],"values")
        data = {"id":vals[0],"position_name":vals[1],"position_description":vals[2],"display_order":vals[3],"is_active": 1 if vals[4]=="Active" else 0}
        self._open_modal("Edit Position", data=data)

    def delete_position(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a position to delete")
            return
        if messagebox.askyesno("Confirm", "Delete selected position? This will cascade delete candidates/votes due to FK."):
            vals = self.tree.item(sel[0],"values")
            q = "DELETE FROM positions WHERE id=%s"
            ok = self.db_manager.execute_update(q, (vals[0],))
            if ok:
                self.load_positions()

class VotesPage(ctk.CTkFrame):
    """Votes review page (delete only)"""
    def __init__(self, parent, db_manager: DatabaseManager):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setup_ui()
        self.load_votes()

    def setup_ui(self):
        header = ctk.CTkFrame(self); header.grid(row=0,column=0,sticky="ew", padx=20, pady=10)
        ctk.CTkLabel(header, text="Votes", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0,column=0,sticky="w")
        ctk.CTkButton(header, text="Refresh", command=self.load_votes).grid(row=0,column=1,sticky="e")
        ctk.CTkButton(header, text="Delete Vote", command=self.delete_vote).grid(row=0,column=2,sticky="e", padx=6)

        table_frame = ctk.CTkFrame(self); table_frame.grid(row=1,column=0,sticky="nsew", padx=20, pady=(0,20))
        cols = ("ID","Student ID","Position","Candidate","Timestamp","IP")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c,text=c)
            self.tree.column(c,width=140)
        self.tree.grid(row=0,column=0,sticky="nsew")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0,column=1,sticky="ns")

    def load_votes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        q = """
        SELECT v.id, v.student_id, p.position_name, c.candidate_name, v.vote_timestamp, v.ip_address
        FROM votes v
        LEFT JOIN positions p ON v.position_id = p.id
        LEFT JOIN candidates c ON v.candidate_id = c.id
        ORDER BY v.vote_timestamp DESC
        """
        res = self.db_manager.execute_query(q)
        if not res:
            return
        for r in res:
            self.tree.insert("", "end", values=r)

    def delete_vote(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a vote to delete")
            return
        vals = self.tree.item(sel[0],"values")
        if messagebox.askyesno("Confirm", "Delete selected vote?"):
            q = "DELETE FROM votes WHERE id=%s"
            ok = self.db_manager.execute_update(q, (vals[0],))
            if ok:
                self.load_votes()

class SettingsPage(ctk.CTkFrame):
    """Election settings (edit values)"""
    def __init__(self, parent, db_manager: DatabaseManager):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        header = ctk.CTkFrame(self); header.grid(row=0,column=0,sticky="ew", padx=20, pady=10)
        ctk.CTkLabel(header, text="Election Settings", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0,column=0,sticky="w")
        ctk.CTkButton(header, text="Add", command=self.add_setting).grid(row=0,column=1,padx=6)
        ctk.CTkButton(header, text="Edit", command=self.edit_setting).grid(row=0,column=2,padx=6)
        ctk.CTkButton(header, text="Delete", command=self.delete_setting).grid(row=0,column=3,padx=6)
        ctk.CTkButton(header, text="Refresh", command=self.load_settings).grid(row=0,column=4,padx=6)

        table_frame = ctk.CTkFrame(self); table_frame.grid(row=1,column=0,sticky="nsew", padx=20, pady=(0,20))
        cols = ("ID","Name","Value","Description")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=16)
        for c in cols:
            self.tree.heading(c,text=c)
            self.tree.column(c,width=200)
        self.tree.grid(row=0,column=0,sticky="nsew")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0,column=1,sticky="ns")

    def load_settings(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        q = "SELECT id, setting_name, setting_value, description FROM election_settings ORDER BY id"
        res = self.db_manager.execute_query(q)
        if not res:
            return
        for r in res:
            self.tree.insert("", "end", values=(r[0], r[1], r[2], r[3] or ""))

    def _open_modal(self, title="Setting", data=None):
        modal = ctk.CTkToplevel(self); modal.title(title); modal.geometry("520x260")
        frame = ctk.CTkFrame(modal); frame.pack(padx=10,pady=10,fill="both",expand=True)
        ctk.CTkLabel(frame,text=title,font=ctk.CTkFont(size=14,weight="bold")).grid(row=0,column=0,columnspan=2,pady=6)
        ctk.CTkLabel(frame,text="Name").grid(row=1,column=0,sticky="w",padx=5,pady=5)
        name = ctk.CTkEntry(frame,width=360); name.grid(row=1,column=1,padx=5,pady=5)
        ctk.CTkLabel(frame,text="Value").grid(row=2,column=0,sticky="w",padx=5,pady=5)
        value = ctk.CTkEntry(frame,width=360); value.grid(row=2,column=1,padx=5,pady=5)
        ctk.CTkLabel(frame,text="Description").grid(row=3,column=0,sticky="w",padx=5,pady=5)
        desc = ctk.CTkEntry(frame,width=360); desc.grid(row=3,column=1,padx=5,pady=5)

        if data:
            name.insert(0, data.get("setting_name",""))
            value.insert(0, data.get("setting_value",""))
            desc.insert(0, data.get("description",""))

        def on_save():
            n = name.get().strip(); v = value.get().strip(); d = desc.get().strip()
            if not (n and v):
                messagebox.showerror("Error", "Name and Value are required")
                return
            if data:
                q = "UPDATE election_settings SET setting_value=%s, description=%s WHERE id=%s"
                ok = self.db_manager.execute_update(q, (v,d,data["id"]))
            else:
                q = "INSERT INTO election_settings (setting_name, setting_value, description) VALUES (%s,%s,%s)"
                ok = self.db_manager.execute_update(q, (n,v,d))
            if ok:
                modal.destroy()
                self.load_settings()
        btn = ctk.CTkFrame(modal); btn.pack(pady=8)
        ctk.CTkButton(btn, text="Save", command=on_save).grid(row=0,column=0,padx=6)
        ctk.CTkButton(btn, text="Cancel", command=modal.destroy).grid(row=0,column=1,padx=6)

    def add_setting(self):
        self._open_modal("Add Setting")

    def edit_setting(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a setting to edit")
            return
        vals = self.tree.item(sel[0],"values")
        data = {"id":vals[0],"setting_name":vals[1],"setting_value":vals[2],"description":vals[3]}
        self._open_modal("Edit Setting", data=data)

    def delete_setting(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a setting to delete")
            return
        vals = self.tree.item(sel[0],"values")
        if messagebox.askyesno("Confirm", "Delete selected setting?"):
            q = "DELETE FROM election_settings WHERE id=%s"
            ok = self.db_manager.execute_update(q,(vals[0],))
            if ok:
                self.load_settings()

class AdminUsersPage(ctk.CTkFrame):
    """Admin users CRUD (password stored as sha256 for demo)"""
    def __init__(self, parent, db_manager: DatabaseManager):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setup_ui()
        self.load_users()

    def setup_ui(self):
        header = ctk.CTkFrame(self); header.grid(row=0,column=0,sticky="ew",padx=20,pady=10)
        ctk.CTkLabel(header,text="Admin Users", font=ctk.CTkFont(size=20,weight="bold")).grid(row=0,column=0,sticky="w")
        ctk.CTkButton(header, text="Add", command=self.add_user).grid(row=0,column=1,padx=6)
        ctk.CTkButton(header, text="Edit", command=self.edit_user).grid(row=0,column=2,padx=6)
        ctk.CTkButton(header, text="Delete", command=self.delete_user).grid(row=0,column=3,padx=6)
        ctk.CTkButton(header, text="Refresh", command=self.load_users).grid(row=0,column=4,padx=6)

        table_frame = ctk.CTkFrame(self); table_frame.grid(row=1,column=0,sticky="nsew",padx=20,pady=(0,20))
        cols = ("ID","Username","Email","Full Name","Role","Active")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=16)
        for c in cols:
            self.tree.heading(c,text=c)
            self.tree.column(c,width=160)
        self.tree.grid(row=0,column=0,sticky="nsew")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0,column=1,sticky="ns")

    def load_users(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        q = "SELECT id, username, email, full_name, role, is_active FROM admin_users ORDER BY id"
        res = self.db_manager.execute_query(q)
        if not res:
            return
        for r in res:
            self.tree.insert("", "end", values=(r[0], r[1], r[2], r[3] or "", r[4] or "admin", "Active" if r[5] else "Inactive"))

    def _open_modal(self, title="Admin User", data=None):
        modal = ctk.CTkToplevel(self); modal.title(title); modal.geometry("520x360")
        frame = ctk.CTkFrame(modal); frame.pack(padx=10,pady=10,fill="both",expand=True)
        ctk.CTkLabel(frame,text=title,font=ctk.CTkFont(size=14,weight="bold")).grid(row=0,column=0,columnspan=2,pady=6)
        ctk.CTkLabel(frame,text="Username").grid(row=1,column=0,sticky="w",padx=5,pady=5)
        username = ctk.CTkEntry(frame,width=360); username.grid(row=1,column=1,padx=5,pady=5)
        ctk.CTkLabel(frame,text="Email").grid(row=2,column=0,sticky="w",padx=5,pady=5)
        email = ctk.CTkEntry(frame,width=360); email.grid(row=2,column=1,padx=5,pady=5)
        ctk.CTkLabel(frame,text="Full Name").grid(row=3,column=0,sticky="w",padx=5,pady=5)
        full = ctk.CTkEntry(frame,width=360); full.grid(row=3,column=1,padx=5,pady=5)
        ctk.CTkLabel(frame,text="Role").grid(row=4,column=0,sticky="w",padx=5,pady=5)
        role = ttk.Combobox(frame, values=["super_admin","admin","moderator"], state="readonly"); role.grid(row=4,column=1,padx=5,pady=5)
        ctk.CTkLabel(frame,text="Password").grid(row=5,column=0,sticky="w",padx=5,pady=5)
        pwd = ctk.CTkEntry(frame, show="*", width=360); pwd.grid(row=5,column=1,padx=5,pady=5)
        active_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(frame, text="Active", variable=active_var).grid(row=6,column=1,padx=5,pady=5, sticky="w")

        if data:
            username.insert(0, data.get("username",""))
            email.insert(0, data.get("email",""))
            full.insert(0, data.get("full_name",""))
            role.set(data.get("role","admin"))
            active_var.set(bool(data.get("is_active",1)))

        def on_save():
            u = username.get().strip(); e = email.get().strip(); f = full.get().strip()
            r = role.get().strip() or "admin"; p = pwd.get().strip()
            a = 1 if active_var.get() else 0
            if not (u and e):
                messagebox.showerror("Error", "Username and Email are required")
                return
            if data:
                # if password provided, update it; otherwise leave existing hash
                if p:
                    ph = hashlib.sha256(p.encode("utf-8")).hexdigest()
                    q = "UPDATE admin_users SET username=%s, email=%s, password_hash=%s, full_name=%s, role=%s, is_active=%s WHERE id=%s"
                    ok = self.db_manager.execute_update(q,(u,e,ph,f,r,a,data["id"]))
                else:
                    q = "UPDATE admin_users SET username=%s, email=%s, full_name=%s, role=%s, is_active=%s WHERE id=%s"
                    ok = self.db_manager.execute_update(q,(u,e,f,r,a,data["id"]))
            else:
                if not p:
                    messagebox.showerror("Error", "Password required for new user")
                    return
                ph = hashlib.sha256(p.encode("utf-8")).hexdigest()
                q = "INSERT INTO admin_users (username, email, password_hash, full_name, role, is_active) VALUES (%s,%s,%s,%s,%s,%s)"
                ok = self.db_manager.execute_update(q,(u,e,ph,f,r,a))
            if ok:
                modal.destroy()
                self.load_users()

        btn = ctk.CTkFrame(modal); btn.pack(pady=8)
        ctk.CTkButton(btn, text="Save", command=on_save).grid(row=0,column=0,padx=6)
        ctk.CTkButton(btn, text="Cancel", command=modal.destroy).grid(row=0,column=1,padx=6)

    def add_user(self):
        self._open_modal("Add Admin User")

    def edit_user(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a user to edit")
            return
        vals = self.tree.item(sel[0],"values")
        data = {"id":vals[0],"username":vals[1],"email":vals[2],"full_name":vals[3],"role":vals[4],"is_active": 1 if vals[5]=="Active" else 0}
        self._open_modal("Edit Admin User", data=data)

    def delete_user(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a user to delete")
            return
        vals = self.tree.item(sel[0],"values")
        if messagebox.askyesno("Confirm", "Delete selected admin user?"):
            q = "DELETE FROM admin_users WHERE id=%s"
            ok = self.db_manager.execute_update(q,(vals[0],))
            if ok:
                self.load_users()

class MainApplication(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        self.title("MCA Voting System")
        self.geometry("1200x800")
        self.minsize(1000, 600)
        
        # Initialize database
        self.db_manager = DatabaseManager()
        if not self.db_manager.connect():
            self.destroy()
            return
        
        # Initialize services
        self.auth_service = AuthService(self.db_manager)
        self.current_user = None
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Show login page
        self.show_login()
    
    def show_login(self):
        """Display login page"""
        # Clear current content
        for widget in self.winfo_children():
            widget.destroy()
        
        # Create login page
        self.login_page = LoginPage(self, self.auth_service, self.on_login_success)
        self.login_page.grid(row=0, column=0, sticky="nsew")
    
    def on_login_success(self, user: User):
        """Handle successful login"""
        self.current_user = user
        self.show_dashboard()
    
    def show_dashboard(self):
        """Display main dashboard with sidebar"""
        # Clear current content
        for widget in self.winfo_children():
            widget.destroy()
        
        # Configure main grid
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main content area FIRST so page switching callbacks can use it
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Create sidebar (it will NOT auto-select a page now)
        self.sidebar = Sidebar(self, self.on_page_select)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Show dashboard page by default
        self.show_page("dashboard")
    
    def on_page_select(self, page_id: str):
        """Handle page selection from sidebar"""
        if page_id == "logout":
            self.logout()
        else:
            self.show_page(page_id)
    
    def show_page(self, page_id: str):
        """Display selected page"""
        # Clear current page
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create appropriate page
        if page_id == "dashboard":
            page = DashboardPage(self.content_frame, self.db_manager)
        elif page_id == "students":
            page = StudentsPage(self.content_frame, self.db_manager)
        elif page_id == "candidates":
            page = CandidatesPage(self.content_frame, self.db_manager)
        elif page_id == "positions":
            page = PositionsPage(self.content_frame, self.db_manager)
        elif page_id == "votes":
            page = VotesPage(self.content_frame, self.db_manager)
        elif page_id == "settings":
            page = SettingsPage(self.content_frame, self.db_manager)
        elif page_id == "admin_users":
            page = AdminUsersPage(self.content_frame, self.db_manager)
        else:
            page = ctk.CTkLabel(self.content_frame, text="Page Not Found",
                               font=ctk.CTkFont(size=24))

        page.grid(row=0, column=0, sticky="nsew")
    
    def logout(self):
        """Handle logout"""
        self.current_user = None
        self.grid_columnconfigure(1, weight=0)  # Reset grid
        self.show_login()
    
    def on_closing(self):
        """Handle application closing"""
        self.db_manager.disconnect()
        self.destroy()


if __name__ == "__main__":
    app = MainApplication()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()