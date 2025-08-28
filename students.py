import customtkinter as ctk
import mysql.connector
from mysql.connector import Error
import os
import tkinter.messagebox as messagebox
from tkinter import ttk
import hashlib
from datetime import datetime
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
            self.connection.rollback()
            messagebox.showerror("Database Error", f"Update execution failed: {e}")
            return False

class StudentLoginPage(ctk.CTkFrame):
    """Login page UI for students."""
    
    def __init__(self, parent, db_manager: DatabaseManager, on_login_success):
        super().__init__(parent)
        self.db_manager = db_manager
        self.on_login_success = on_login_success
        self.setup_ui()

    def setup_ui(self):
        """Setup login UI components."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        login_frame = ctk.CTkFrame(self, width=400, height=300)
        login_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        login_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(login_frame, text="MCA Voting System", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        subtitle_label = ctk.CTkLabel(login_frame, text="Student Login", 
                                     font=ctk.CTkFont(size=16))
        subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 20))
        
        self.student_id_entry = ctk.CTkEntry(login_frame, placeholder_text="Student ID", width=300)
        self.student_id_entry.grid(row=2, column=0, padx=20, pady=10)
        
        self.password_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", 
                                          show="*", width=300)
        self.password_entry.grid(row=3, column=0, padx=20, pady=10)
        
        login_button = ctk.CTkButton(login_frame, text="Login", command=self.login, width=300)
        login_button.grid(row=4, column=0, padx=20, pady=(20, 10))
        
        self.student_id_entry.bind("<Return>", lambda e: self.login())
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        self.student_id_entry.focus()

    def login(self):
        """Handle student login attempt."""
        student_id = self.student_id_entry.get().strip()
        password = self.password_entry.get().strip()

        if not student_id or not password:
            messagebox.showerror("Error", "Please enter both Student ID and password.")
            return

        try:
            query = "SELECT id, password_hash, has_voted FROM students WHERE student_id = %s AND is_active = 1"
            result = self.db_manager.execute_query(query, (student_id,))

            if result:
                db_id, stored_hash, has_voted = result[0]
                
                # For demo purposes, we assume a simple password check if no hash is stored
                # In a real system, all passwords should be hashed.
                password_valid = False
                if stored_hash:
                    # Compare hashed password
                    password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
                    if password_hash == stored_hash:
                        password_valid = True
                else:
                    # Fallback for plain text password (not recommended)
                    if password == stored_hash:
                         password_valid = True

                if password_valid:
                    if has_voted:
                        messagebox.showinfo("Already Voted", "You have already cast your vote. You cannot vote again.")
                    else:
                        messagebox.showinfo("Success", "Login successful!")
                        self.on_login_success(db_id, student_id)
                else:
                    messagebox.showerror("Error", "Incorrect password. Please try again.")
                    self.password_entry.delete(0, "end")
            else:
                messagebox.showerror("Error", "Student ID not found or inactive. Please try again.")
        except Exception as e:
            messagebox.showerror("Login Error", f"An unexpected error occurred: {e}")


class VotingPage(ctk.CTkFrame):
    """Voting page UI."""
    
    def __init__(self, parent, db_manager: DatabaseManager, db_student_id: int, student_id_str: str, on_logout):
        super().__init__(parent)
        self.db_manager = db_manager
        self.db_student_id = db_student_id
        self.student_id_str = student_id_str
        self.on_logout = on_logout
        self.votes_to_cast = {} # {position_id: candidate_id}
        
        self.setup_ui()

    def setup_ui(self):
        """Setup voting UI components."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(header_frame, text="Cast Your Vote", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        logout_btn = ctk.CTkButton(header_frame, text="Logout", command=self.on_logout, fg_color="red", hover_color="darkred")
        logout_btn.grid(row=0, column=1, padx=20, pady=10, sticky="e")

        scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Select one candidate for each position")
        scrollable_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        scrollable_frame.grid_columnconfigure(0, weight=1)

        try:
            positions_query = "SELECT id, position_name FROM positions WHERE is_active = 1 ORDER BY display_order"
            positions = self.db_manager.execute_query(positions_query)

            if not positions:
                ctk.CTkLabel(scrollable_frame, text="No voting positions are currently available.", font=ctk.CTkFont(size=16)).pack(pady=50)
                return

            for pos_id, pos_name in positions:
                pos_frame = ctk.CTkFrame(scrollable_frame)
                pos_frame.pack(fill="x", padx=10, pady=10)
                ctk.CTkLabel(pos_frame, text=pos_name, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=20, pady=(5,0))
                
                candidates_query = "SELECT id, candidate_name FROM candidates WHERE position_id = %s AND is_active = 1"
                candidates = self.db_manager.execute_query(candidates_query, (pos_id,))
                
                if candidates:
                    vote_var = ctk.StringVar()
                    for cand_id, cand_name in candidates:
                        rb = ctk.CTkRadioButton(pos_frame, text=cand_name, variable=vote_var, value=str(cand_id),
                                                command=lambda p=pos_id, c=cand_id: self.select_candidate(p, c))
                        rb.pack(anchor="w", padx=40, pady=5)
                else:
                    ctk.CTkLabel(pos_frame, text="No candidates for this position.").pack(anchor="w", padx=40, pady=5)

            self.submit_button = ctk.CTkButton(self, text="Submit All Votes", command=self.submit_votes, height=40)
            self.submit_button.grid(row=2, column=0, padx=20, pady=20)

        except Exception as e:
            ctk.CTkLabel(scrollable_frame, text=f"Error loading ballot: {e}", font=ctk.CTkFont(size=16)).pack(pady=50)

    def select_candidate(self, position_id, candidate_id):
        """Store the selected candidate for a given position."""
        self.votes_to_cast[position_id] = candidate_id

    def submit_votes(self):
        """Handle vote submission for all selected positions."""
        if not self.votes_to_cast:
            messagebox.showwarning("Warning", "Please select at least one candidate to vote for.")
            return

        if not messagebox.askyesno("Confirm Vote", f"You are about to cast {len(self.votes_to_cast)} vote(s). This action cannot be undone. Proceed?"):
            return

        try:
            # Insert all votes
            vote_query = "INSERT INTO votes (student_id, position_id, candidate_id, vote_timestamp, ip_address) VALUES (%s, %s, %s, %s, %s)"
            timestamp = datetime.now()
            ip_address = "127.0.0.1" # Placeholder IP

            for pos_id, cand_id in self.votes_to_cast.items():
                params = (self.db_student_id, pos_id, cand_id, timestamp, ip_address)
                if not self.db_manager.execute_update(vote_query, params):
                    # Error message is shown by db_manager, so we just stop
                    return

            # Mark the student as having voted
            update_student_query = "UPDATE students SET has_voted = 1 WHERE id = %s"
            if not self.db_manager.execute_update(update_student_query, (self.db_student_id,)):
                return

            messagebox.showinfo("Success", "Thank you for your vote! Your votes have been recorded.")
            self.on_logout() # Log out automatically after voting

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while submitting your votes: {e}")


class StudentApp(ctk.CTk):
    """Main application window for the student portal."""
    
    def __init__(self):
        super().__init__()
        
        self.title("Student Voting Portal")
        self.geometry("800x600")
        self.minsize(600, 500)
        
        self.db_manager = DatabaseManager()
        if not self.db_manager.connect():
            self.after(100, self.destroy) # Schedule destroy to allow messagebox to show
            return

        self.current_db_student_id = None
        self.current_student_id_str = None
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.show_login_page()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show_login_page(self):
        """Display the login page."""
        for widget in self.winfo_children():
            widget.destroy()
        
        self.login_page = StudentLoginPage(self, self.db_manager, self.on_login_success)
        self.login_page.grid(row=0, column=0, sticky="nsew")

    def on_login_success(self, db_student_id: int, student_id_str: str):
        """Handle successful login."""
        self.current_db_student_id = db_student_id
        self.current_student_id_str = student_id_str
        self.show_voting_page()

    def show_voting_page(self):
        """Display the main voting page."""
        for widget in self.winfo_children():
            widget.destroy()
            
        self.voting_page = VotingPage(self, self.db_manager, self.current_db_student_id, self.current_student_id_str, self.logout)
        self.voting_page.grid(row=0, column=0, sticky="nsew")

    def logout(self):
        """Handle logout."""
        self.current_db_student_id = None
        self.current_student_id_str = None
        self.show_login_page()

    def on_closing(self):
        """Handle application closing."""
        self.db_manager.disconnect()
        self.destroy()


if __name__ == "__main__":
    app = StudentApp()
    app.mainloop()