import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime

class StudentEMRSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student EMR System - Electronic Medical Records")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f8ff')
        
        # Data storage
        self.data_file = "student_emr_data.json"
        self.students = self.load_data()
        
        # Current student ID for editing
        self.current_student_id = None
        
        self.setup_gui()
        
    def setup_gui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_add_student_tab()
        self.create_search_tab()
        self.create_view_all_tab()
        
    def create_dashboard_tab(self):
        # Dashboard Tab
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Title
        title_label = tk.Label(dashboard_frame, 
                              text="Student EMR System", 
                              font=('Arial', 20, 'bold'),
                              bg='#f0f8ff',
                              fg='#2c3e50')
        title_label.pack(pady=20)
        
        # Statistics frame
        stats_frame = tk.Frame(dashboard_frame, bg='#f0f8ff')
        stats_frame.pack(pady=20)
        
        total_students = len(self.students)
        stats_text = f"""
        System Overview:
        
        • Total Students: {total_students}
        • Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        • Data File: {self.data_file}
        
        Features:
        • Add new student medical records
        • Edit existing records
        • Search by Student ID
        • View all records
        • Automatic JSON storage
        """
        
        stats_label = tk.Label(stats_frame, 
                              text=stats_text,
                              font=('Arial', 12),
                              bg='#f0f8ff',
                              fg='#34495e',
                              justify=tk.LEFT)
        stats_label.pack()
        
        # Quick actions
        actions_frame = tk.Frame(dashboard_frame, bg='#f0f8ff')
        actions_frame.pack(pady=20)
        
        quick_actions_label = tk.Label(actions_frame,
                                      text="Quick Actions:",
                                      font=('Arial', 14, 'bold'),
                                      bg='#f0f8ff',
                                      fg='#2c3e50')
        quick_actions_label.pack(pady=10)
        
        action_buttons_frame = tk.Frame(actions_frame, bg='#f0f8ff')
        action_buttons_frame.pack()
        
        tk.Button(action_buttons_frame, 
                 text="Add New Student", 
                 command=lambda: self.notebook.select(1),
                 bg='#27ae60',
                 fg='white',
                 font=('Arial', 10),
                 padx=20,
                 pady=10).grid(row=0, column=0, padx=10)
        
        tk.Button(action_buttons_frame, 
                 text="Search Records", 
                 command=lambda: self.notebook.select(2),
                 bg='#3498db',
                 fg='white',
                 font=('Arial', 10),
                 padx=20,
                 pady=10).grid(row=0, column=1, padx=10)
        
        tk.Button(action_buttons_frame, 
                 text="View All Records", 
                 command=lambda: self.notebook.select(3),
                 bg='#9b59b6',
                 fg='white',
                 font=('Arial', 10),
                 padx=20,
                 pady=10).grid(row=0, column=2, padx=10)
    
    def create_add_student_tab(self):
        # Add/Edit Student Tab
        add_frame = ttk.Frame(self.notebook)
        self.notebook.add(add_frame, text="Add/Edit Student")
        
        # Form frame
        form_frame = tk.Frame(add_frame, bg='#f0f8ff')
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        self.add_title = tk.Label(form_frame, 
                                 text="Add New Student Record", 
                                 font=('Arial', 16, 'bold'),
                                 bg='#f0f8ff',
                                 fg='#2c3e50')
        self.add_title.pack(pady=10)
        
        # Create form fields
        fields = [
            ("Student ID*", "student_id"),
            ("Full Name*", "full_name"),
            ("Age", "age"),
            ("Gender", "gender"),
            ("Blood Pressure", "blood_pressure"),
            ("Heart Rate (bpm)", "heart_rate"),
            ("Temperature (°C)", "temperature"),
            ("Weight (kg)", "weight"),
            ("Height (cm)", "height"),
            ("Allergies", "allergies"),
            ("Medications", "medications"),
            ("Medical History", "medical_history"),
            ("Current Symptoms", "current_symptoms"),
            ("Notes", "notes")
        ]
        
        self.entries = {}
        
        for i, (label_text, field_name) in enumerate(fields):
            frame = tk.Frame(form_frame, bg='#f0f8ff')
            frame.pack(fill='x', pady=5)
            
            label = tk.Label(frame, text=label_text, width=20, anchor='w', bg='#f0f8ff')
            label.pack(side='left', padx=(0, 10))
            
            if field_name in ['medical_history', 'current_symptoms', 'notes']:
                entry = scrolledtext.ScrolledText(frame, height=3, width=40)
            else:
                entry = tk.Entry(frame, width=40)
            
            entry.pack(side='left', fill='x', expand=True)
            self.entries[field_name] = entry
        
        # Buttons frame
        buttons_frame = tk.Frame(form_frame, bg='#f0f8ff')
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, 
                 text="Save Record", 
                 command=self.save_student,
                 bg='#27ae60',
                 fg='white',
                 font=('Arial', 12),
                 padx=20,
                 pady=10).pack(side='left', padx=10)
        
        tk.Button(buttons_frame, 
                 text="Clear Form", 
                 command=self.clear_form,
                 bg='#e74c3c',
                 fg='white',
                 font=('Arial', 12),
                 padx=20,
                 pady=10).pack(side='left', padx=10)
        
        tk.Button(buttons_frame, 
                 text="Update Record", 
                 command=self.update_student,
                 bg='#3498db',
                 fg='white',
                 font=('Arial', 12),
                 padx=20,
                 pady=10).pack(side='left', padx=10)
    
    def create_search_tab(self):
        # Search Tab
        search_frame = ttk.Frame(self.notebook)
        self.notebook.add(search_frame, text="Search Student")
        
        # Search frame
        search_top_frame = tk.Frame(search_frame, bg='#f0f8ff')
        search_top_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(search_top_frame, 
                text="Search by Student ID:", 
                font=('Arial', 12, 'bold'),
                bg='#f0f8ff').pack(side='left', padx=(0, 10))
        
        self.search_entry = tk.Entry(search_top_frame, width=20, font=('Arial', 12))
        self.search_entry.pack(side='left', padx=(0, 10))
        
        tk.Button(search_top_frame, 
                 text="Search", 
                 command=self.search_student,
                 bg='#3498db',
                 fg='white',
                 font=('Arial', 10)).pack(side='left', padx=(0, 10))
        
        tk.Button(search_top_frame, 
                 text="Edit This Record", 
                 command=self.load_for_edit,
                 bg='#f39c12',
                 fg='white',
                 font=('Arial', 10)).pack(side='left')
        
        # Results frame
        self.results_text = scrolledtext.ScrolledText(search_frame, 
                                                     height=20, 
                                                     font=('Arial', 10))
        self.results_text.pack(fill='both', expand=True, padx=20, pady=10)
    
    def create_view_all_tab(self):
        # View All Tab
        view_frame = ttk.Frame(self.notebook)
        self.notebook.add(view_frame, text="View All Records")
        
        # Controls frame
        controls_frame = tk.Frame(view_frame, bg='#f0f8ff')
        controls_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(controls_frame, 
                 text="Refresh List", 
                 command=self.display_all_students,
                 bg='#3498db',
                 fg='white',
                 font=('Arial', 10)).pack(side='left', padx=(0, 10))
        
        tk.Button(controls_frame, 
                 text="Export to JSON", 
                 command=self.export_data,
                 bg='#27ae60',
                 fg='white',
                 font=('Arial', 10)).pack(side='left', padx=(0, 10))
        
        tk.Button(controls_frame, 
                 text="Delete Selected", 
                 command=self.delete_student,
                 bg='#e74c3c',
                 fg='white',
                 font=('Arial', 10)).pack(side='left')
        
        # Treeview for displaying records
        columns = ('ID', 'Name', 'Age', 'Gender', 'BP', 'Heart Rate', 'Temp')
        self.tree = ttk.Treeview(view_frame, columns=columns, show='headings', height=20)
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(view_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side='right', fill='y', padx=(0, 20), pady=10)
        
        # Display initial data
        self.display_all_students()
    
    def load_data(self):
        """Load student data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    return json.load(file)
            except (json.JSONDecodeError, Exception):
                return {}
        return {}
    
    def save_data(self):
        """Save student data to JSON file"""
        try:
            with open(self.data_file, 'w') as file:
                json.dump(self.students, file, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
            return False
    
    def save_student(self):
        """Save new student record"""
        try:
            # Get data from form
            student_data = {}
            for field, entry in self.entries.items():
                if isinstance(entry, scrolledtext.ScrolledText):
                    student_data[field] = entry.get('1.0', tk.END).strip()
                else:
                    student_data[field] = entry.get().strip()
            
            # Validate required fields
            if not student_data['student_id'] or not student_data['full_name']:
                messagebox.showwarning("Validation Error", "Student ID and Full Name are required!")
                return
            
            # Check if student ID already exists
            if student_data['student_id'] in self.students:
                messagebox.showwarning("Duplicate ID", 
                                     "Student ID already exists! Use Update instead or choose a different ID.")
                return
            
            # Add timestamp
            student_data['created_at'] = datetime.now().isoformat()
            student_data['updated_at'] = datetime.now().isoformat()
            
            # Save to memory
            self.students[student_data['student_id']] = student_data
            
            # Save to file
            if self.save_data():
                messagebox.showinfo("Success", "Student record saved successfully!")
                self.clear_form()
                self.display_all_students()
            else:
                messagebox.showerror("Error", "Failed to save student record!")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def update_student(self):
        """Update existing student record"""
        if not self.current_student_id:
            messagebox.showwarning("No Record", "No record selected for update. Please search and load a record first.")
            return
            
        try:
            # Get data from form
            updated_data = {}
            for field, entry in self.entries.items():
                if isinstance(entry, scrolledtext.ScrolledText):
                    updated_data[field] = entry.get('1.0', tk.END).strip()
                else:
                    updated_data[field] = entry.get().strip()
            
            # Validate required fields
            if not updated_data['student_id'] or not updated_data['full_name']:
                messagebox.showwarning("Validation Error", "Student ID and Full Name are required!")
                return
            
            # Update timestamp
            updated_data['updated_at'] = datetime.now().isoformat()
            updated_data['created_at'] = self.students[self.current_student_id].get('created_at', datetime.now().isoformat())
            
            # Update in memory
            self.students[updated_data['student_id']] = updated_data
            
            # If ID changed, remove old entry
            if updated_data['student_id'] != self.current_student_id:
                del self.students[self.current_student_id]
                self.current_student_id = updated_data['student_id']
            
            # Save to file
            if self.save_data():
                messagebox.showinfo("Success", "Student record updated successfully!")
                self.clear_form()
                self.display_all_students()
            else:
                messagebox.showerror("Error", "Failed to update student record!")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def search_student(self):
        """Search for student by ID"""
        student_id = self.search_entry.get().strip()
        if not student_id:
            messagebox.showwarning("Input Error", "Please enter a Student ID to search.")
            return
        
        if student_id in self.students:
            student = self.students[student_id]
            self.display_student_details(student)
            self.current_student_id = student_id
        else:
            self.results_text.delete('1.0', tk.END)
            self.results_text.insert(tk.END, f"No student found with ID: {student_id}")
            self.current_student_id = None
    
    def display_student_details(self, student):
        """Display student details in search results"""
        self.results_text.delete('1.0', tk.END)
        
        details = f"""
STUDENT MEDICAL RECORD
{'=' * 50}

Basic Information:
• Student ID: {student.get('student_id', 'N/A')}
• Full Name: {student.get('full_name', 'N/A')}
• Age: {student.get('age', 'N/A')}
• Gender: {student.get('gender', 'N/A')}

Vital Signs:
• Blood Pressure: {student.get('blood_pressure', 'N/A')}
• Heart Rate: {student.get('heart_rate', 'N/A')} bpm
• Temperature: {student.get('temperature', 'N/A')} °C
• Weight: {student.get('weight', 'N/A')} kg
• Height: {student.get('height', 'N/A')} cm

Medical Information:
• Allergies: {student.get('allergies', 'N/A')}
• Medications: {student.get('medications', 'N/A')}

Medical History:
{student.get('medical_history', 'N/A')}

Current Symptoms:
{student.get('current_symptoms', 'N/A')}

Additional Notes:
{student.get('notes', 'N/A')}

Record Information:
• Created: {student.get('created_at', 'N/A')}
• Last Updated: {student.get('updated_at', 'N/A')}
{'=' * 50}
"""
        self.results_text.insert(tk.END, details)
    
    def load_for_edit(self):
        """Load current search result into edit form"""
        if not self.current_student_id:
            messagebox.showwarning("No Record", "Please search for a student record first.")
            return
        
        student = self.students[self.current_student_id]
        self.clear_form()
        
        # Switch to Add/Edit tab
        self.notebook.select(1)
        self.add_title.config(text="Edit Student Record")
        
        # Fill form with student data
        for field, entry in self.entries.items():
            value = student.get(field, '')
            if isinstance(entry, scrolledtext.ScrolledText):
                entry.delete('1.0', tk.END)
                entry.insert('1.0', value)
            else:
                entry.delete(0, tk.END)
                entry.insert(0, value)
    
    def clear_form(self):
        """Clear all form fields"""
        for field, entry in self.entries.items():
            if isinstance(entry, scrolledtext.ScrolledText):
                entry.delete('1.0', tk.END)
            else:
                entry.delete(0, tk.END)
        
        self.current_student_id = None
        self.add_title.config(text="Add New Student Record")
    
    def display_all_students(self):
        """Display all students in the treeview"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add students to treeview
        for student_id, student in self.students.items():
            self.tree.insert('', tk.END, values=(
                student.get('student_id', ''),
                student.get('full_name', ''),
                student.get('age', ''),
                student.get('gender', ''),
                student.get('blood_pressure', ''),
                student.get('heart_rate', ''),
                student.get('temperature', '')
            ))
    
    def delete_student(self):
        """Delete selected student record"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a student record to delete.")
            return
        
        # Get student ID from selected item
        student_id = self.tree.item(selected_item[0])['values'][0]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete record for Student ID: {student_id}?"):
            try:
                del self.students[student_id]
                if self.save_data():
                    messagebox.showinfo("Success", "Student record deleted successfully!")
                    self.display_all_students()
                else:
                    messagebox.showerror("Error", "Failed to delete student record!")
            except KeyError:
                messagebox.showerror("Error", "Student record not found!")
    
    def export_data(self):
        """Export data to a separate JSON file"""
        try:
            export_filename = f"student_emr_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(export_filename, 'w') as file:
                json.dump(self.students, file, indent=4)
            messagebox.showinfo("Export Successful", 
                              f"Data exported successfully to:\n{export_filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")

def main():
    root = tk.Tk()
    app = StudentEMRSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()