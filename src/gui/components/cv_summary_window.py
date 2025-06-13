import customtkinter as ctk
from tkinter import messagebox
import os
from PIL import Image

class CVSummaryWindow:
    def __init__(self, parent, cv_data=None, search_controller=None):
        self.parent = parent
        self.search_controller = search_controller
        self.cv_data = cv_data 
        
        self.window = ctk.CTkToplevel(parent)
        self.setup_window()
        self.create_ui()
        
    def setup_window(self):
        self.window.title("SignHire - CV Summary")
        self.window.geometry("800x600")  
        self.window.configure(fg_color="#18206F")  
        self.window.resizable(False, False) 
        
        self.window.transient(self.parent)
        self.window.grab_set()
        
        self.center_window_same_position()
        self.window.focus()
    
    def center_window_same_position(self):
        self.window.update_idletasks()
        
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        
        self.window.geometry(f"800x600+{parent_x}+{parent_y}")
    
    def create_ui(self):
        self.create_header()
        
        self.content_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(5, 20))
        
        self.create_content_area()
    
    def create_header(self):
        header_frame = ctk.CTkFrame(self.window, height=80, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        center_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        center_container.pack(expand=True, fill="both")
        
        title_label = ctk.CTkLabel(
            center_container,
            text="S i g n H i r e",
            font=("Inter", 20, "bold"),
            text_color="white"
        )
        title_label.pack(pady=(10, 5))
        
        summary_frame = ctk.CTkFrame(center_container, fg_color="transparent")
        summary_frame.pack(pady=(0, 5))
        
        icon_frame = ctk.CTkFrame(
            summary_frame, 
            width=20, 
            height=20, 
            fg_color="#FFA500",
            corner_radius=3
        )
        icon_frame.pack(side="left", padx=(0, 8))
        icon_frame.pack_propagate(False)
        
        summary_label = ctk.CTkLabel(
            summary_frame,
            text="CV Summary",
            font=("Inter", 14),
            text_color="white"
        )
        summary_label.pack(side="left")
    
    def create_content_area(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent",
            scrollbar_fg_color="#18206F",
            scrollbar_button_color="#DC2626",
            scrollbar_button_hover_color="#B91C1C"
        )
        self.scrollable_frame.pack(fill="both", expand=True)
        
        self.create_personal_info_section()
        
        self.create_skills_section()
        
        self.create_job_history_section()
        
        self.create_education_section()
        
        self.create_action_buttons()
    
    def create_personal_info_section(self):
        info_container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        info_container.pack(fill="x", pady=(0, 15))
        
        icon_frame = ctk.CTkFrame(info_container, fg_color="transparent")
        icon_frame.pack(side="left", padx=(0, 15))
        
        self.create_profile_icon(icon_frame)
        
        info_card = ctk.CTkFrame(
            info_container,
            fg_color="#E8D5B7",
            corner_radius=15
        )
        info_card.pack(side="left", fill="both", expand=True)
        
        card_content = ctk.CTkFrame(info_card, fg_color="transparent")
        card_content.pack(fill="both", expand=True, padx=15, pady=15)
        
        name_label = ctk.CTkLabel(
            card_content,
            text=self.cv_data["name"],
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#2D1B69",
            anchor="w"
        )
        name_label.pack(fill="x", pady=(0, 8))
        
        details_text = f"""Birthdate    : {self.cv_data['birthdate']}
        
Address      : {self.cv_data['address']}

Phone          : {self.cv_data['phone']}

Email            : {self.cv_data.get('email', 'N/A')}

Role             : {self.cv_data.get('role', 'N/A')}"""
        
        details_label = ctk.CTkLabel(
            card_content,
            text=details_text,
            font=ctk.CTkFont(size=12),
            text_color="#2D1B69",
            anchor="w",
            justify="left"
        )
        details_label.pack(fill="x")
    
    def create_profile_icon(self, parent_frame):
        try:
            image_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "img2.png")
            
            if not os.path.exists(image_path):
                image_path = os.path.join(os.path.dirname(__file__), "..", "assets", "img2.png")

            
            if os.path.exists(image_path):
                pil_image = Image.open(image_path)
                
                pil_image = pil_image.resize((120, 120), Image.Resampling.LANCZOS)
                
                profile_image = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=(120, 120)
                )
                
                profile_icon = ctk.CTkLabel(
                    parent_frame,
                    image=profile_image,
                    text="", 
                    width=120,
                    height=120,
                    fg_color="transparent" 
                )
                profile_icon.pack()
                
                print(f"Profile icon loaded successfully from: {image_path}")
                
            else:
                print(f"Image not found at any path. Using fallback icon.")
                self.create_fallback_profile_icon(parent_frame)
                
        except Exception as e:
            print(f"Error loading profile image: {e}")
            self.create_fallback_profile_icon(parent_frame)
    
    def create_fallback_profile_icon(self, parent_frame):
        profile_icon = ctk.CTkFrame(
            parent_frame,
            width=120,
            height=120,
            fg_color="#FFA500",
            corner_radius=30
        )
        profile_icon.pack()
        profile_icon.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(
            profile_icon,
            text="👤",
            font=ctk.CTkFont(size=24),
            text_color="white"
        )
        icon_label.pack(expand=True)
    
    def create_skills_section(self):
        skills_header = ctk.CTkLabel(
            self.scrollable_frame,
            text="Skills",
            font=ctk.CTkFont(size=16, weight="bold"),  
            text_color="white",
            anchor="w"
        )
        skills_header.pack(fill="x", pady=(0, 8))  
        
        skills_container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        skills_container.pack(fill="x", pady=(0, 15)) 
        
        skills_frame = ctk.CTkFrame(skills_container, fg_color="transparent")
        skills_frame.pack(fill="x")
        
        current_row = ctk.CTkFrame(skills_frame, fg_color="transparent")
        current_row.pack(fill="x", pady=1)  
        
        skills_per_row = 5  
        for i, skill in enumerate(self.cv_data["skills"]):
            if i > 0 and i % skills_per_row == 0:
                current_row = ctk.CTkFrame(skills_frame, fg_color="transparent")
                current_row.pack(fill="x", pady=1)  
            
            skill_tag = ctk.CTkButton(
                current_row,
                text=skill,
                font=ctk.CTkFont(size=10, weight="bold"), 
                fg_color="#DC2626",
                hover_color="#B91C1C",
                text_color="white",
                corner_radius=15,  
                height=25,  
                width=100, 
            )
            skill_tag.pack(side="left", padx=(0, 8))  
    
    def create_job_history_section(self):
        job_header = ctk.CTkLabel(
            self.scrollable_frame,
            text="Job History",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white",
            anchor="w"
        )
        job_header.pack(fill="x", pady=(8, 8))  
        
        for job in self.cv_data["job_history"]:
            job_card = ctk.CTkFrame(
                self.scrollable_frame,
                fg_color="#E8D5B7",
                corner_radius=15
            )
            job_card.pack(fill="x", pady=(0, 10))  
            
            job_content = ctk.CTkFrame(job_card, fg_color="transparent")
            job_content.pack(fill="both", expand=True, padx=15, pady=12)  
            
            job_title = ctk.CTkLabel(
                job_content,
                text=job["title"],
                font=ctk.CTkFont(size=14, weight="bold"), 
                text_color="#2D1B69",
                anchor="w"
            )
            job_title.pack(fill="x")
            
            job_period = ctk.CTkLabel(
                job_content,
                text=job["period"],
                font=ctk.CTkFont(size=11),  
                text_color="#2D1B69",
                anchor="w"
            )
            job_period.pack(fill="x", pady=(1, 6))  
            
            job_desc = ctk.CTkLabel(
                job_content,
                text=job["description"],
                font=ctk.CTkFont(size=10), 
                text_color="#2D1B69",
                anchor="w",
                justify="left",
                wraplength=700  
            )
            job_desc.pack(fill="x")
    
    def create_education_section(self):
        edu_header = ctk.CTkLabel(
            self.scrollable_frame,
            text="Education",
            font=ctk.CTkFont(size=16, weight="bold"), 
            text_color="white",
            anchor="w"
        )
        edu_header.pack(fill="x", pady=(8, 8))  
        
        for education in self.cv_data["education"]:
            edu_card = ctk.CTkFrame(
                self.scrollable_frame,
                fg_color="#E8D5B7",
                corner_radius=15
            )
            edu_card.pack(fill="x", pady=(0, 10))  
            
            edu_content = ctk.CTkFrame(edu_card, fg_color="transparent")
            edu_content.pack(fill="both", expand=True, padx=15, pady=12)  
            
            edu_title = ctk.CTkLabel(
                edu_content,
                text=education["degree"],
                font=ctk.CTkFont(size=14, weight="bold"),  
                text_color="#2D1B69",
                anchor="w"
            )
            edu_title.pack(fill="x")
            
            edu_period = ctk.CTkLabel(
                edu_content,
                text=education["period"],
                font=ctk.CTkFont(size=11),  
                text_color="#2D1B69",
                anchor="w"
            )
            edu_period.pack(fill="x", pady=(1, 0))  
    
    def create_action_buttons(self):
        button_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(15, 0))  
        
        close_btn = ctk.CTkButton(
            button_frame,
            text="Close",
            font=ctk.CTkFont(size=12, weight="bold"),  
            fg_color="#DC2626",
            hover_color="#B91C1C",
            text_color="white",
            corner_radius=20,  
            width=100,  
            height=35,  
            command=self.close_window
        )
        close_btn.pack(side="right", padx=(8, 0))  
        
        view_cv_btn = ctk.CTkButton(
            button_frame,
            text="View CV File",
            font=ctk.CTkFont(size=12, weight="bold"),  
            fg_color="transparent",
            text_color="white",
            hover_color="#B91C1C",
            border_width=2,
            border_color="white",
            corner_radius=20,  
            width=100,  
            height=35, 
            command=self.view_cv_file
        )
        view_cv_btn.pack(side="right")
    
    def close_window(self):
        self.window.destroy()
    
    def view_cv_file(self):
        if self.search_controller and hasattr(self.cv_data, 'cv_id'):
            cv_id = getattr(self.cv_data, 'cv_id', None)
            if cv_id:
                try:
                    cv_file_path = self.search_controller.get_cv_file_path(cv_id)
                    if cv_file_path:
                        self.open_cv_file(cv_file_path)
                        return
                except Exception as e:
                    print(f"Error getting CV file: {e}")
        
        messagebox.showinfo(
            "View CV File", 
            f"Opening CV file for {self.cv_data['name']}..."
        )
    
    def open_cv_file(self, cv_file_path):
        try:
            import os
            import platform
            from pathlib import Path
            
            if not os.path.isabs(cv_file_path):
                current_dir = Path(__file__).resolve().parent
                project_root = current_dir.parent.parent
                full_path = project_root / cv_file_path
            else:
                full_path = Path(cv_file_path)
            
            if not full_path.exists():
                messagebox.showerror("File Not Found", f"CV file not found:\n{full_path}")
                return
            
            system = platform.system()
            if system == "Windows":
                os.startfile(str(full_path))
            else:
                messagebox.showinfo("File Found", f"CV file located at:\n{full_path}")
            
            print(f"Opened CV file: {full_path}")
            
        except Exception as e:
            print(f"Error opening CV file: {e}")
            messagebox.showerror("Error", f"Could not open CV file: {str(e)}")
    
    
class CVSummaryIntegration:

    def show_cv_summary(parent_window, cv_data=None, search_controller=None):
        try:
            summary_window = CVSummaryWindow(parent_window, cv_data, search_controller)
            return summary_window
        except Exception as e:
            messagebox.showerror("Error", f"Could not open CV Summary: {str(e)}")
            return None

    def format_cv_data_from_database(search_controller, cv_id):
        try:
            if search_controller and hasattr(search_controller, 'get_applicant_summary_data'):
                detail_id = int(cv_id.split('_')[1]) if cv_id.startswith('cv_') else int(cv_id)
                summary_data = search_controller.get_applicant_summary_data(detail_id)
                
                class CVDataWithID:
                    def __init__(self, data, cv_id):
                        self.cv_id = cv_id
                        for key, value in data.items():
                            setattr(self, key, value)
                    
                    def __getitem__(self, key):
                        return getattr(self, key, "N/A")
                    
                    def get(self, key, default=None):
                        return getattr(self, key, default)
                
                return CVDataWithID(summary_data, cv_id)
            else:
                return None
        except Exception as e:
            print(f"Error formatting CV data from database: {e}")
            return None