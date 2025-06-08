# cv_summary_window.py - Updated with Database Integration
import customtkinter as ctk
from tkinter import messagebox
import os
from PIL import Image

class CVSummaryWindow:
    def __init__(self, parent, cv_data=None, search_controller=None):
        self.parent = parent
        self.search_controller = search_controller
        self.cv_data = cv_data or self.get_sample_data()
        
        # Create the window
        self.window = ctk.CTkToplevel(parent)
        self.setup_window()
        self.create_ui()
        
    def setup_window(self):
        """Configure the summary window with same size as main window"""
        self.window.title("SignHire - CV Summary")
        self.window.geometry("800x600")  # Same size as main window
        self.window.configure(fg_color="#18206F")  # Same purple as main window
        self.window.resizable(False, False)  # Prevent window resize
        
        # Make window modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Center window at same position as main window
        self.center_window_same_position()
        
        # Focus on window
        self.window.focus()
    
    def center_window_same_position(self):
        """Position window exactly where main window is"""
        self.window.update_idletasks()
        
        # Get parent window position and size
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        
        # Set window to exact same position as parent
        self.window.geometry(f"800x600+{parent_x}+{parent_y}")
    
    def create_ui(self):
        """Create the user interface with same layout as main window"""
        # Header section (same as main window)
        self.create_header()
        
        # Main content area (same padding as main window)
        self.content_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(5, 20))
        
        # Scrollable content area
        self.create_content_area()
    
    def create_header(self):
        """Create header with same style as main window"""
        header_frame = ctk.CTkFrame(self.window, height=80, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        # Center container
        center_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        center_container.pack(expand=True, fill="both")
        
        # App title - same style as main window
        title_label = ctk.CTkLabel(
            center_container,
            text="S i g n H i r e",
            font=("Inter", 20, "bold"),
            text_color="white"
        )
        title_label.pack(pady=(10, 5))
        
        # CV Summary subtitle
        summary_frame = ctk.CTkFrame(center_container, fg_color="transparent")
        summary_frame.pack(pady=(0, 5))
        
        # Icon (using a simple rectangle as placeholder for folder icon)
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
        """Create scrollable content area"""
        # Create scrollable frame with reduced size to fit in 800x600
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent",
            scrollbar_fg_color="#18206F",
            scrollbar_button_color="#DC2626",
            scrollbar_button_hover_color="#B91C1C"
        )
        self.scrollable_frame.pack(fill="both", expand=True)
        
        # Personal Information Section
        self.create_personal_info_section()
        
        # Skills Section
        self.create_skills_section()
        
        # Job History Section
        self.create_job_history_section()
        
        # Education Section
        self.create_education_section()
        
        # Action Buttons
        self.create_action_buttons()
    
    def create_personal_info_section(self):
        """Create personal information section with icon outside the card"""
        # Container for icon and card side by side
        info_container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        info_container.pack(fill="x", pady=(0, 15))
        
        # Profile icon (outside card, on the left)
        icon_frame = ctk.CTkFrame(info_container, fg_color="transparent")
        icon_frame.pack(side="left", padx=(0, 15))
        
        # Profile icon using image from img2.png
        self.create_profile_icon(icon_frame)
        
        # Personal info card (only covers the text area)
        info_card = ctk.CTkFrame(
            info_container,
            fg_color="#E8D5B7",
            corner_radius=15
        )
        info_card.pack(side="left", fill="both", expand=True)
        
        # Card content with personal details only
        card_content = ctk.CTkFrame(info_card, fg_color="transparent")
        card_content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Name
        name_label = ctk.CTkLabel(
            card_content,
            text=self.cv_data["name"],
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#2D1B69",
            anchor="w"
        )
        name_label.pack(fill="x", pady=(0, 8))
        
        # Personal details - Updated to include email and role
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
        """Create profile icon using img2.png image without background"""
        try:
            # Try to load the image from the assets folder
            image_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "img2.png")
            
            # If not found, try alternative paths
            if not os.path.exists(image_path):
                # Try in src/assets/
                image_path = os.path.join(os.path.dirname(__file__), "..", "assets", "img2.png")
            
            if not os.path.exists(image_path):
                # Try in root assets/
                image_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets", "img2.png")
            
            if not os.path.exists(image_path):
                # Try relative to current directory
                image_path = "assets/img2.png"
            
            if os.path.exists(image_path):
                # Load and resize the image
                pil_image = Image.open(image_path)
                
                # Resize image to fit the icon size (60x60)
                pil_image = pil_image.resize((120, 120), Image.Resampling.LANCZOS)
                
                # Convert to CTkImage
                profile_image = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=(120, 120)
                )
                
                # Create the profile icon label with transparent background
                profile_icon = ctk.CTkLabel(
                    parent_frame,
                    image=profile_image,
                    text="",  # No text since we have image
                    width=120,
                    height=120,
                    fg_color="transparent"  # No background
                )
                profile_icon.pack()
                
                print(f"Profile icon loaded successfully from: {image_path}")
                
            else:
                # Fallback to default icon if image not found
                print(f"Image not found at any path. Using fallback icon.")
                self.create_fallback_profile_icon(parent_frame)
                
        except Exception as e:
            print(f"Error loading profile image: {e}")
            # Fallback to default icon
            self.create_fallback_profile_icon(parent_frame)
    
    def create_fallback_profile_icon(self, parent_frame):
        """Create fallback profile icon when image is not available"""
        # Create circular icon (fallback still has some styling but minimal)
        profile_icon = ctk.CTkFrame(
            parent_frame,
            width=120,
            height=120,
            fg_color="#FFA500",
            corner_radius=30
        )
        profile_icon.pack()
        profile_icon.pack_propagate(False)
        
        # Add person icon text
        icon_label = ctk.CTkLabel(
            profile_icon,
            text="👤",
            font=ctk.CTkFont(size=24),
            text_color="white"
        )
        icon_label.pack(expand=True)
    
    def create_skills_section(self):
        """Create skills section with compact layout"""
        # Section header with reduced size
        skills_header = ctk.CTkLabel(
            self.scrollable_frame,
            text="Skills",
            font=ctk.CTkFont(size=16, weight="bold"),  # Reduced size
            text_color="white",
            anchor="w"
        )
        skills_header.pack(fill="x", pady=(0, 8))  # Reduced padding
        
        # Skills container
        skills_container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        skills_container.pack(fill="x", pady=(0, 15))  # Reduced padding
        
        # Create skill tags
        skills_frame = ctk.CTkFrame(skills_container, fg_color="transparent")
        skills_frame.pack(fill="x")
        
        # Add skills in rows with more skills per row to fit better
        current_row = ctk.CTkFrame(skills_frame, fg_color="transparent")
        current_row.pack(fill="x", pady=1)  # Reduced padding
        
        skills_per_row = 5  # Increased from 4 to 5
        for i, skill in enumerate(self.cv_data["skills"]):
            if i > 0 and i % skills_per_row == 0:
                current_row = ctk.CTkFrame(skills_frame, fg_color="transparent")
                current_row.pack(fill="x", pady=1)  # Reduced padding
            
            skill_tag = ctk.CTkButton(
                current_row,
                text=skill,
                font=ctk.CTkFont(size=10, weight="bold"),  # Reduced size
                fg_color="#DC2626",
                hover_color="#B91C1C",
                text_color="white",
                corner_radius=15,  # Reduced radius
                height=25,  # Reduced height
                width=100,  # Reduced width
                # state="disabled"  # Make it non-clickable
            )
            skill_tag.pack(side="left", padx=(0, 8))  # Reduced padding
    
    def create_job_history_section(self):
        """Create job history section with compact layout"""
        # Section header with reduced size
        job_header = ctk.CTkLabel(
            self.scrollable_frame,
            text="Job History",
            font=ctk.CTkFont(size=16, weight="bold"),  # Reduced size
            text_color="white",
            anchor="w"
        )
        job_header.pack(fill="x", pady=(8, 8))  # Reduced padding
        
        # Job history cards with reduced spacing
        for job in self.cv_data["job_history"]:
            job_card = ctk.CTkFrame(
                self.scrollable_frame,
                fg_color="#E8D5B7",
                corner_radius=15
            )
            job_card.pack(fill="x", pady=(0, 10))  # Reduced padding
            
            # Job card content with reduced padding
            job_content = ctk.CTkFrame(job_card, fg_color="transparent")
            job_content.pack(fill="both", expand=True, padx=15, pady=12)  # Reduced padding
            
            # Job title with reduced size
            job_title = ctk.CTkLabel(
                job_content,
                text=job["title"],
                font=ctk.CTkFont(size=14, weight="bold"),  # Reduced size
                text_color="#2D1B69",
                anchor="w"
            )
            job_title.pack(fill="x")
            
            # Job period with reduced size
            job_period = ctk.CTkLabel(
                job_content,
                text=job["period"],
                font=ctk.CTkFont(size=11),  # Reduced size
                text_color="#2D1B69",
                anchor="w"
            )
            job_period.pack(fill="x", pady=(1, 6))  # Reduced padding
            
            # Job description with reduced size and wraplength
            job_desc = ctk.CTkLabel(
                job_content,
                text=job["description"],
                font=ctk.CTkFont(size=10),  # Reduced size
                text_color="#2D1B69",
                anchor="w",
                justify="left",
                wraplength=700  # Reduced wraplength to fit 800px width
            )
            job_desc.pack(fill="x")
    
    def create_education_section(self):
        """Create education section with compact layout"""
        # Section header with reduced size
        edu_header = ctk.CTkLabel(
            self.scrollable_frame,
            text="Education",
            font=ctk.CTkFont(size=16, weight="bold"),  # Reduced size
            text_color="white",
            anchor="w"
        )
        edu_header.pack(fill="x", pady=(8, 8))  # Reduced padding
        
        # Education cards with reduced spacing
        for education in self.cv_data["education"]:
            edu_card = ctk.CTkFrame(
                self.scrollable_frame,
                fg_color="#E8D5B7",
                corner_radius=15
            )
            edu_card.pack(fill="x", pady=(0, 10))  # Reduced padding
            
            # Education card content with reduced padding
            edu_content = ctk.CTkFrame(edu_card, fg_color="transparent")
            edu_content.pack(fill="both", expand=True, padx=15, pady=12)  # Reduced padding
            
            # Degree/Institution with reduced size
            edu_title = ctk.CTkLabel(
                edu_content,
                text=education["degree"],
                font=ctk.CTkFont(size=14, weight="bold"),  # Reduced size
                text_color="#2D1B69",
                anchor="w"
            )
            edu_title.pack(fill="x")
            
            # Period with reduced size
            edu_period = ctk.CTkLabel(
                edu_content,
                text=education["period"],
                font=ctk.CTkFont(size=11),  # Reduced size
                text_color="#2D1B69",
                anchor="w"
            )
            edu_period.pack(fill="x", pady=(1, 0))  # Reduced padding
    
    def create_action_buttons(self):
        """Create action buttons at the bottom with compact layout"""
        button_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(15, 0))  # Reduced padding
        
        # Close button with reduced size
        close_btn = ctk.CTkButton(
            button_frame,
            text="Close",
            font=ctk.CTkFont(size=12, weight="bold"),  # Reduced size
            fg_color="#DC2626",
            hover_color="#B91C1C",
            text_color="white",
            corner_radius=20,  # Reduced radius
            width=100,  # Reduced width
            height=35,  # Reduced height
            command=self.close_window
        )
        close_btn.pack(side="right", padx=(8, 0))  # Reduced padding
        
        # View CV File button with reduced size
        view_cv_btn = ctk.CTkButton(
            button_frame,
            text="View CV File",
            font=ctk.CTkFont(size=12, weight="bold"),  # Reduced size
            fg_color="transparent",
            text_color="white",
            hover_color="#B91C1C",
            border_width=2,
            border_color="white",
            corner_radius=20,  # Reduced radius
            width=100,  # Reduced width
            height=35,  # Reduced height
            command=self.view_cv_file
        )
        view_cv_btn.pack(side="right")
    
    def close_window(self):
        """Close the summary window"""
        self.window.destroy()
    
    def view_cv_file(self):
        """Handle view CV file action - now integrated with search controller"""
        if self.search_controller and hasattr(self.cv_data, 'cv_id'):
            # Get CV ID from data
            cv_id = getattr(self.cv_data, 'cv_id', None)
            if cv_id:
                try:
                    # Get CV file path from search controller
                    cv_file_path = self.search_controller.get_cv_file_path(cv_id)
                    if cv_file_path:
                        # Open the CV file
                        self.open_cv_file(cv_file_path)
                        return
                except Exception as e:
                    print(f"Error getting CV file: {e}")
        
        # Fallback message
        messagebox.showinfo(
            "View CV File", 
            f"Opening CV file for {self.cv_data['name']}...\n\nThis feature will open the original CV document."
        )
    
    def open_cv_file(self, cv_file_path):
        """Open CV file using system default application"""
        try:
            import os
            import platform
            from pathlib import Path
            
            # Convert to absolute path if needed
            if not os.path.isabs(cv_file_path):
                # Try to find the file in project directory
                current_dir = Path(__file__).resolve().parent
                project_root = current_dir.parent.parent
                full_path = project_root / cv_file_path
            else:
                full_path = Path(cv_file_path)
            
            if not full_path.exists():
                messagebox.showerror("File Not Found", f"CV file not found:\n{full_path}")
                return
            
            # Open with system default application
            system = platform.system()
            if system == "Windows":
                os.startfile(str(full_path))
            elif system == "Darwin":  # macOS
                os.system(f"open '{full_path}'")
            elif system == "Linux":
                os.system(f"xdg-open '{full_path}'")
            else:
                messagebox.showinfo("File Found", f"CV file located at:\n{full_path}")
            
            print(f"Opened CV file: {full_path}")
            
        except Exception as e:
            print(f"Error opening CV file: {e}")
            messagebox.showerror("Error", f"Could not open CV file: {str(e)}")
    
    def get_sample_data(self):
        """Return sample CV data for testing"""
        return {
            "name": "Sample Applicant",
            "birthdate": "01-01-1990",
            "address": "Sample Address",
            "phone": "1234567890",
            "email": "sample@email.com",
            "role": "Software Engineer",
            "skills": ["Python", "Java", "React", "Node.js", "SQL", "Git", "Docker", "AWS"],
            "job_history": [
                {
                    "title": "Senior Software Engineer",
                    "period": "2020 - 2024",
                    "description": "Developed and maintained software applications using modern technologies and frameworks."
                }
            ],
            "education": [
                {
                    "degree": "Bachelor of Computer Science",
                    "period": "2016 - 2020"
                }
            ]
        }

# Updated integration class with database support
class CVSummaryIntegration:
    """Helper class to integrate CV Summary with main application and database"""
    
    @staticmethod
    def show_cv_summary(parent_window, cv_data=None, search_controller=None):
        """Show CV summary window with database integration"""
        try:
            summary_window = CVSummaryWindow(parent_window, cv_data, search_controller)
            return summary_window
        except Exception as e:
            messagebox.showerror("Error", f"Could not open CV Summary: {str(e)}")
            return None
    
    @staticmethod
    def format_cv_data_from_database(search_controller, cv_id):
        """Format CV data from database for the summary window"""
        try:
            if search_controller and hasattr(search_controller, 'get_applicant_summary_data'):
                # Get data from database via search controller
                detail_id = int(cv_id.split('_')[1]) if cv_id.startswith('cv_') else int(cv_id)
                summary_data = search_controller.get_applicant_summary_data(detail_id)
                
                # Add cv_id for file viewing
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
    
    @staticmethod
    def format_cv_data(raw_cv_data):
        """Format raw CV data for the summary window (fallback method)"""
        formatted_data = {
            "name": raw_cv_data.get("full_name", raw_cv_data.get("name", "N/A")),
            "birthdate": raw_cv_data.get("birth_date", raw_cv_data.get("birthdate", "N/A")),
            "address": raw_cv_data.get("address", raw_cv_data.get("applicant_address", "N/A")),
            "phone": raw_cv_data.get("phone_number", raw_cv_data.get("phone", "N/A")),
            "email": raw_cv_data.get("email", "N/A"),
            "role": raw_cv_data.get("role", raw_cv_data.get("applicant_role", "N/A")),
            "skills": raw_cv_data.get("skills", []),
            "job_history": raw_cv_data.get("work_experience", raw_cv_data.get("job_history", [])),
            "education": raw_cv_data.get("education", [])
        }
        return formatted_data