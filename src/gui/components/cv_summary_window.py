# cv_summary_window.py
import customtkinter as ctk
from tkinter import messagebox
import os
from PIL import Image

class CVSummaryWindow:
    def __init__(self, parent, cv_data=None):
        self.parent = parent
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
        
        # Personal details
        details_text = f"""Birthdate    : {self.cv_data['birthdate']}
        
Address      : {self.cv_data['address']}

Phone          : {self.cv_data['phone']}"""
        
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
        """Handle view CV file action"""
        messagebox.showinfo(
            "View CV File", 
            f"Opening CV file for {self.cv_data['name']}...\n\nThis feature will open the original CV document."
        )
        # Here you would implement the actual CV file viewing logic
        # For example: opening a PDF viewer or document viewer
    
    def get_sample_data(self):
        """Return sample CV data for testing"""
        return {
            "name": "Naylaaaa",
            "birthdate": "HH-MM-YYYY",
            "address": "Labtek V",
            "phone": "XXXX - XXXX - XXXX",
            "skills": ["Python", "Java", "React", "Node.js", "SQL", "Git", "Docker", "AWS"],
            "job_history": [
                {
                    "title": "Senior Software Engineer",
                    "period": "2020 - 2024",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi."
                },
                {
                    "title": "Full Stack Developer", 
                    "period": "2018 - 2020",
                    "description": "Developed and maintained web applications using modern frameworks. Collaborated with cross-functional teams to deliver high-quality software solutions."
                }
            ],
            "education": [
                {
                    "degree": "Master of Computer Science - MIT",
                    "period": "2020 - 2024"
                },
                {
                    "degree": "Bachelor of Information Technology - Stanford University",
                    "period": "2016 - 2020"
                }
            ]
        }

# Example usage and integration with main window
class CVSummaryIntegration:
    """Helper class to integrate CV Summary with main application"""
    
    @staticmethod
    def show_cv_summary(parent_window, cv_data=None):
        """Show CV summary window"""
        try:
            summary_window = CVSummaryWindow(parent_window, cv_data)
            return summary_window
        except Exception as e:
            messagebox.showerror("Error", f"Could not open CV Summary: {str(e)}")
            return None
    
    @staticmethod
    def format_cv_data(raw_cv_data):
        """Format raw CV data for the summary window"""
        # This method would convert your database/search results 
        # into the format expected by CVSummaryWindow
        formatted_data = {
            "name": raw_cv_data.get("full_name", "N/A"),
            "birthdate": raw_cv_data.get("birth_date", "N/A"),
            "address": raw_cv_data.get("address", "N/A"),
            "phone": raw_cv_data.get("phone_number", "N/A"),
            "skills": raw_cv_data.get("skills", []),
            "job_history": raw_cv_data.get("work_experience", []),
            "education": raw_cv_data.get("education", [])
        }
        return formatted_data