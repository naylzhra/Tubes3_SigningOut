# main_window.py
import customtkinter as ctk
from .splash_screen import SplashScreen
from .home_page import HomePage
from .cv_summary_window import CVSummaryWindow, CVSummaryIntegration
# from about_page import AboutPage
# from developer_page import DeveloperPage

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("SignHire - Professional ATS System")
        self.geometry("800x600")
        self.configure(fg_color="#18206F")  # Purple background
        self.resizable(False, False)  # Prevent window resize
        
        # Center window on screen
        self.center_window()
        
        # Initialize variables
        self.current_page = None
        self.pages = {}
        
        # Initialize controllers (commented for now)
        # TODO: Uncomment when controllers are ready
        # from controller.searcher import SearchController
        # from controller.data_controller import DataController
        # self.search_controller = SearchController()
        # self.data_controller = DataController()
        
        # Show splash screen first
        self.withdraw()  # Hide main window
        self.show_splash()
    
    def center_window(self):
        """Center window on screen"""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        self.geometry(f"800x600+{x}+{y}")
    
    def show_splash(self):
        """Display splash screen"""
        splash = SplashScreen(self, self.on_splash_complete)
    
    def on_splash_complete(self):
        """Called when splash screen finishes"""
        self.deiconify()  # Show main window
        self.center_window()  # Re-center after showing
        self.setup_ui()
    
    def setup_ui(self):
        """Setup main window UI"""
        # Header with navigation - reduced height
        self.create_header()
        
        # Content area with reduced top padding
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(5, 20))
        
        # Initialize pages
        self.initialize_pages()
        
        # Show home page by default
        self.show_page('home')
    
    def create_header(self):
        """Create navigation header with centered layout"""
        header_frame = ctk.CTkFrame(self, height=80, fg_color="transparent")  # Reduced from 120 to 80
        header_frame.pack(fill="x", padx=20, pady=(10, 5))  # Reduced bottom padding
        header_frame.pack_propagate(False)
        
        # Center container untuk semua header content
        center_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        center_container.pack(expand=True, fill="both")
        
        # App title - CENTERED di atas
        title_label = ctk.CTkLabel(
            center_container,
            text="S i g n H i r e",
            font=("Inter", 20, "bold"),  # Reduced from 24 to 20
            text_color="white"
        )
        title_label.pack(pady=(10, 10))  # Reduced padding
        
        # Navigation buttons - CENTERED di bawah title
        nav_frame = ctk.CTkFrame(center_container, fg_color="transparent")
        nav_frame.pack(pady=(0, 5))  # Reduced padding
        
        # Home button
        self.home_btn = ctk.CTkButton(
            nav_frame,
            text="Home",
            font=("Inter", 12, "bold"),  # Reduced font size
            fg_color="#DC2626",
            hover_color="#B91C1C",
            width=100,  # Reduced width
            height=28,  # Reduced height
            corner_radius=25,
            command=lambda: self.show_page('home')
        )
        self.home_btn.pack(side="left", padx=(0, 30))  # Reduced spacing
        
        # About button
        self.about_btn = ctk.CTkButton(
            nav_frame,
            text="About the App",
            font=("Inter", 12),  # Reduced font size
            fg_color="transparent",
            text_color="white",
            hover_color="#B91C1C",
            width=100,  # Reduced width
            height=28,  # Reduced height
            corner_radius=25,
            command=lambda: self.show_page('about')
        )
        self.about_btn.pack(side="left", padx=(0, 30))  # Reduced spacing
        
        # Developer button
        self.dev_btn = ctk.CTkButton(
            nav_frame,
            text="Developer",
            font=("Inter", 12),  # Reduced font size
            fg_color="transparent",
            text_color="white",
            hover_color="#B91C1C",
            width=100,  # Reduced width
            height=28,  # Reduced height
            corner_radius=25,
            command=lambda: self.show_page('developer')
        )
        self.dev_btn.pack(side="left")
        
        # Store navigation buttons for styling updates
        self.nav_buttons = {
            'home': self.home_btn,
            'about': self.about_btn,
            'developer': self.dev_btn
        }
    
    def initialize_pages(self):
        """Initialize all page objects"""
        # Create page instances but don't pack them yet
        self.pages['home'] = HomePage(self.content_frame)
        
        # Set main window reference for navigation
        self.pages['home'].set_main_window(self)
        
        # self.pages['about'] = AboutPage(self.content_frame)
        # self.pages['developer'] = DeveloperPage(self.content_frame)
        
        # Hide all pages initially
        for page in self.pages.values():
            page.pack_forget()
    
    def show_page(self, page_name):
        """Switch to specified page"""
        # Hide current page
        if self.current_page and self.current_page in self.pages:
            self.pages[self.current_page].pack_forget()
        
        # Show new page
        if page_name in self.pages:
            self.pages[page_name].pack(fill="both", expand=True)
            self.current_page = page_name
            
            # Update navigation button styles
            self.update_nav_buttons(page_name)
            
            # Handle page-specific logic
            self.on_page_changed(page_name)
    
    def update_nav_buttons(self, active_page):
        """Update navigation button styles"""
        for page_name, button in self.nav_buttons.items():
            if page_name == active_page:
                button.configure(
                    fg_color="#DC2626",
                    text_color="white"
                )
            else:
                button.configure(
                    fg_color="transparent",
                    text_color="white"
                )
    
    def on_page_changed(self, page_name):
        """Handle page-specific logic when page changes"""
        if page_name == 'home':
            # Connect home page search functionality
            # TODO: Uncomment when search controller is ready
            # home_page = self.pages['home']
            # home_page.search_callback = self.perform_search
            pass
        
        elif page_name == 'about':
            # Any about page specific logic
            pass
        
        elif page_name == 'developer':
            # Any developer page specific logic
            pass
    
    def perform_search(self, keywords, algorithm, top_matches):
        """Handle search functionality from home page"""
        print(f"Main Window - Search requested:")
        print(f"  Keywords: {keywords}")
        print(f"  Algorithm: {algorithm}")
        print(f"  Top Matches: {top_matches}")
        
        # TODO: Uncomment and implement when controllers are ready
        # try:
        #     # Call search controller
        #     results = self.search_controller.search_cvs(keywords, algorithm, top_matches)
        #     
        #     # Update home page with results
        #     home_page = self.pages['home']
        #     home_page.display_search_results(results)
        #     
        #     print(f"Search completed: {len(results['results'])} results found")
        #     
        # except Exception as e:
        #     self.show_error_dialog("Search Error", f"An error occurred during search: {str(e)}")
        
        # For now, just simulate search
        self.simulate_search_results()
    
    def simulate_search_results(self):
        """Simulate search results for testing"""
        home_page = self.pages['home']
        home_page.update_results_display()
        print("Search simulation completed")
    
    def show_cv_summary(self, cv_index):
        """Show CV summary window"""        
        print(f"Main Window - Show summary for CV {cv_index}")
        
        try:
            # Get CV data (implement this method based on your data source)
            cv_data = self.get_cv_data(cv_index)
            
            # Show summary window using the integration class
            summary_window = CVSummaryIntegration.show_cv_summary(self, cv_data)
            
            if summary_window:
                print(f"CV Summary window opened for CV {cv_index}")
            
        except Exception as e:
            self.show_error_dialog("CV Summary Error", f"Could not open CV summary: {str(e)}")
    
    def view_cv_file(self, cv_index):
        """Open CV file viewer"""
        print(f"Main Window - View CV file {cv_index}")
        
        try:
            # TODO: Implement actual CV file viewer
            # For now, show a placeholder message
            self.show_info_dialog("CV Viewer", f"Opening CV file for applicant {cv_index}...\n\nThis feature will open the PDF viewer.")
            
            # TODO: Implement actual file opening logic
            # from controller.cv_viewer import CVViewer
            # cv_viewer = CVViewer()
            # cv_viewer.open_cv(cv_index)
            
        except Exception as e:
            self.show_error_dialog("CV Viewer Error", f"Could not open CV: {str(e)}")
    
    def get_cv_data(self, cv_index):
        """Get CV data for the specified index"""
        # TODO: Replace with actual database/controller call
        # For now, return sample data based on index
        
        sample_data = [
            {
                "full_name": "Newa Sagita",
                "birth_date": "15-08-1995",
                "address": "Labtek V, ITB Bandung",
                "phone_number": "0812-3456-7890",
                "skills": ["Python", "Java", "React", "Node.js", "SQL", "Git", "Docker", "AWS"],
                "work_experience": [
                    {
                        "title": "Senior Software Engineer",
                        "period": "2020 - 2024",
                        "description": "Led development of microservices architecture using Python and React. Collaborated with cross-functional teams to deliver scalable solutions for enterprise clients."
                    },
                    {
                        "title": "Full Stack Developer", 
                        "period": "2018 - 2020",
                        "description": "Developed and maintained web applications using modern frameworks. Implemented RESTful APIs and integrated with third-party services."
                    }
                ],
                "education": [
                    {
                        "degree": "Master of Computer Science - Institut Teknologi Bandung",
                        "period": "2020 - 2024"
                    },
                    {
                        "degree": "Bachelor of Information Technology - Universitas Indonesia",
                        "period": "2016 - 2020"
                    }
                ]
            },
            {
                "full_name": "Ahmad Rahman",
                "birth_date": "20-05-1992",
                "address": "Jl. Sudirman No. 123, Jakarta",
                "phone_number": "0821-9876-5432",
                "skills": ["PHP", "Laravel", "MySQL", "JavaScript", "Vue.js", "Redis"],
                "work_experience": [
                    {
                        "title": "Backend Developer",
                        "period": "2019 - 2024",
                        "description": "Developed robust backend systems using PHP Laravel framework. Optimized database queries and implemented caching strategies for improved performance."
                    },
                    {
                        "title": "Web Developer", 
                        "period": "2017 - 2019",
                        "description": "Built responsive web applications and managed database systems. Collaborated with frontend team to create seamless user experiences."
                    }
                ],
                "education": [
                    {
                        "degree": "Bachelor of Computer Science - Universitas Gadjah Mada",
                        "period": "2013 - 2017"
                    }
                ]
            },
            {
                "full_name": "Sari Dewi",
                "birth_date": "12-03-1990",
                "address": "Jl. Ganesha No. 10, Bandung",
                "phone_number": "0856-1234-5678",
                "skills": ["UI/UX Design", "Figma", "Adobe XD", "HTML", "CSS", "JavaScript"],
                "work_experience": [
                    {
                        "title": "UI/UX Designer",
                        "period": "2018 - 2024",
                        "description": "Designed user interfaces for mobile and web applications. Conducted user research and usability testing to improve user experience."
                    }
                ],
                "education": [
                    {
                        "degree": "Bachelor of Visual Communication Design - Institut Teknologi Bandung",
                        "period": "2008 - 2012"
                    }
                ]
            }
        ]
        
        # Return data based on index, with fallback to first entry
        if 0 <= cv_index < len(sample_data):
            selected_data = sample_data[cv_index]
        else:
            selected_data = sample_data[0]  # Fallback to first entry
        
        # Format the data for CV summary window
        formatted_data = CVSummaryIntegration.format_cv_data(selected_data)
        return formatted_data
        
        # TODO: Replace with actual database call
        # try:
        #     cv_data = self.data_controller.get_applicant_data(cv_index)
        #     return CVSummaryIntegration.format_cv_data(cv_data)
        # except Exception as e:
        #     print(f"Error fetching CV data: {e}")
        #     return None
    
    def show_error_dialog(self, title, message):
        """Show error dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.configure(fg_color="#4C1D95")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog relative to main window
        self.update_idletasks()
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (400 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (200 // 2)
        dialog.geometry(f"400x200+{x}+{y}")
        
        # Error message
        error_label = ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color="white",
            wraplength=350
        )
        error_label.pack(pady=40)
        
        # OK button
        ok_button = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            fg_color="#DC2626",
            hover_color="#B91C1C"
        )
        ok_button.pack(pady=20)
    
    def show_info_dialog(self, title, message):
        """Show info dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.configure(fg_color="#18206F")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog relative to main window
        self.update_idletasks()
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (400 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (200 // 2)
        dialog.geometry(f"400x200+{x}+{y}")
        
        # Info message
        info_label = ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color="white",
            wraplength=350
        )
        info_label.pack(pady=40)
        
        # OK button
        ok_button = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            fg_color="#DC2626",
            hover_color="#B91C1C"
        )
        ok_button.pack(pady=20)
    
    def get_current_page(self):
        """Get current active page"""
        return self.current_page
    
    def get_page(self, page_name):
        """Get specific page object"""
        return self.pages.get(page_name)
    
    def refresh_current_page(self):
        """Refresh current page"""
        if self.current_page:
            # You can implement page-specific refresh logic here
            pass
    
    # Database connection methods (commented for now)
    # TODO: Uncomment when database is ready
    # def connect_database(self):
    #     """Initialize database connection"""
    #     try:
    #         from database.db_manager import DatabaseManager
    #         self.db_manager = DatabaseManager()
    #         return True
    #     except Exception as e:
    #         self.show_error_dialog("Database Error", f"Could not connect to database: {str(e)}")
    #         return False
    
    # def load_cv_data(self):
    #     """Load CV data from database"""
    #     try:
    #         cv_data = self.db_manager.get_all_applications()
    #         return cv_data
    #     except Exception as e:
    #         self.show_error_dialog("Data Error", f"Could not load CV data: {str(e)}")
    #         return []