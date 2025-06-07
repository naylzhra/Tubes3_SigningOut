import customtkinter as ctk
from .splash_screen import SplashScreen
from .home_page import HomePage
from .cv_summary_window import CVSummaryWindow, CVSummaryIntegration
from .about_page import AboutPage
from .developer_page import DeveloperPage

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
        
        # Initialize controllers
        self.search_controller = None
        self.init_search_controller()
        
        # Show splash screen first
        self.withdraw()  # Hide main window
        self.show_splash()
    
    def init_search_controller(self):
        """Initialize search controller for all algorithms integration"""
        try:
            from controller.searcher import SearchController
            self.search_controller = SearchController()
            print("Search controller initialized successfully with all algorithms")
        except ImportError as e:
            print(f"Warning: Could not import SearchController: {e}")
            print("Make sure controller/searcher.py exists and is properly configured")
            self.search_controller = None
        except Exception as e:
            print(f"Warning: Could not initialize search controller: {e}")
            self.search_controller = None
    
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
        header_frame = ctk.CTkFrame(self, height=80, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        # Center container untuk semua header content
        center_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        center_container.pack(expand=True, fill="both")
        
        # App title - CENTERED di atas
        title_label = ctk.CTkLabel(
            center_container,
            text="S i g n H i r e",
            font=("Inter", 20, "bold"),
            text_color="white"
        )
        title_label.pack(pady=(10, 10))
        
        # Navigation buttons - CENTERED di bawah title
        nav_frame = ctk.CTkFrame(center_container, fg_color="transparent")
        nav_frame.pack(pady=(0, 5))
        
        # Home button
        self.home_btn = ctk.CTkButton(
            nav_frame,
            text="Home",
            font=("Inter", 12, "bold"),
            fg_color="#DC2626",
            hover_color="#B91C1C",
            width=100,
            height=28,
            corner_radius=25,
            command=lambda: self.show_page('home')
        )
        self.home_btn.pack(side="left", padx=(0, 30))
        
        # About button
        self.about_btn = ctk.CTkButton(
            nav_frame,
            text="About the App",
            font=("Inter", 12, "bold"),
            fg_color="transparent",
            text_color="white",
            hover_color="#B91C1C",
            width=100,
            height=28,
            corner_radius=25,
            command=lambda: self.show_page('about')
        )
        self.about_btn.pack(side="left", padx=(0, 30))
        
        # Developer button
        self.dev_btn = ctk.CTkButton(
            nav_frame,
            text="Developer",
            font=("Inter", 12, "bold"),
            fg_color="transparent",
            text_color="white",
            hover_color="#B91C1C",
            width=100,
            height=28,
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
        self.pages['about'] = AboutPage(self.content_frame)
        self.pages['developer'] = DeveloperPage(self.content_frame)
        
        # Set main window reference for navigation and pass search controller
        self.pages['home'].set_main_window(self)
        
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
            # Home page gets search functionality through set_main_window
            pass
        
        elif page_name == 'about':
            # Any about page specific logic
            pass
        
        elif page_name == 'developer':
            # Any developer page specific logic
            pass
    
    def perform_search(self, keywords, algorithm, top_matches):
        """Handle search functionality from home page - integrated with all algorithms"""
        print(f"Main Window - Search requested:")
        print(f"  Keywords: {keywords}")
        print(f"  Algorithm: {algorithm}")
        print(f"  Top Matches: {top_matches}")
        
        if self.search_controller:
            try:
                # Call search controller with all algorithm support
                results = self.search_controller.search_cvs(keywords, algorithm, top_matches)
                
                # Update home page with real results
                home_page = self.pages['home']
                home_page.display_search_results(results)
                
                algorithm_used = results['summary']['algorithm_used']
                result_count = len(results['results'])
                
                print(f"{algorithm_used} Search completed: {result_count} results found")
                
                # Log fallback usage if applicable
                if "→" in algorithm_used:
                    print(f"Fallback mechanism activated: {algorithm_used}")
                
            except Exception as e:
                print(f"Search error: {e}")
                self.show_error_dialog("Search Error", f"An error occurred during search: {str(e)}")
        else:
            # Fallback to simulation if controller not available
            print("Search controller not available, using simulation")
            self.simulate_search_results()
    
    def simulate_search_results(self):
        """Simulate search results for testing when controller not available"""
        home_page = self.pages['home']
        
        # Create mock results for testing
        mock_results = {
            "results": [
                {
                    "cv_id": "cv_1",
                    "name": "John Doe",
                    "total_matches": 3,
                    "matched_keywords": ["• python (2)", "• javascript (1)"],
                    "match_details": {"python": 2, "javascript": 1},
                    "positions": {"python": [45, 120], "javascript": [200]}
                }
            ],
            "summary": {
                "total_cvs_searched": 6,
                "cvs_with_matches": 1,
                "search_time_ms": 15,
                "algorithm_used": "Mock Algorithm",
                "keywords_searched": 2
            }
        }
        
        home_page.display_search_results(mock_results)
        print("Search simulation completed")
    
    def show_cv_summary(self, cv_index):
        """Show CV summary window using dummy data"""        
        print(f"Main Window - Show summary for CV {cv_index}")
        
        try:
            # Always use dummy data for summary (as requested)
            cv_data = self.get_dummy_cv_data(cv_index)
            
            # Show summary window using the integration class
            summary_window = CVSummaryIntegration.show_cv_summary(self, cv_data)
            
            if summary_window:
                print(f"CV Summary window opened for CV {cv_index}")
            
        except Exception as e:
            print(f"Error showing CV summary: {e}")
            self.show_error_dialog("CV Summary Error", f"Could not open CV summary: {str(e)}")
    
    def view_cv_file(self, cv_index):
        """Open CV file viewer - show actual PDF from database"""
        print(f"Main Window - View CV file {cv_index}")
        
        try:
            # Get CV ID and file path from search controller
            if self.search_controller and hasattr(self.search_controller, 'cv_database'):
                cv_ids = list(self.search_controller.cv_database.keys())
                if 0 <= cv_index < len(cv_ids):
                    cv_id = cv_ids[cv_index]
                    
                    # Get actual CV file path from database
                    cv_file_path = self.search_controller.get_cv_file_path(cv_id)
                    
                    if cv_file_path:
                        # Try to open the PDF file
                        self.open_pdf_file(cv_file_path, cv_id)
                        return
                    else:
                        self.show_error_dialog("CV File Error", f"CV file not found for {cv_id}")
                        return
            
            # Fallback to showing info dialog
            self.show_info_dialog("CV Viewer", f"Opening CV file for applicant {cv_index}...\n\nThis feature will open the PDF viewer.")
            
        except Exception as e:
            print(f"Error viewing CV: {e}")
            self.show_error_dialog("CV Viewer Error", f"Could not open CV: {str(e)}")
    
    def open_pdf_file(self, cv_file_path, cv_id):
        """
        Open PDF file using system default application or show content in dialog
        """
        try:
            import os
            import platform
            from pathlib import Path
            
            # Convert to absolute path
            if not os.path.isabs(cv_file_path):
                project_root = Path(__file__).resolve().parents[2]
                full_path = project_root / cv_file_path
            else:
                full_path = Path(cv_file_path)
            
            if not full_path.exists():
                self.show_error_dialog("File Not Found", f"CV file not found:\n{full_path}")
                return
            
            # Try to open with system default application
            system = platform.system()
            
            if system == "Windows":
                os.startfile(str(full_path))
            elif system == "Darwin":  # macOS
                os.system(f"open '{full_path}'")
            elif system == "Linux":
                os.system(f"xdg-open '{full_path}'")
            else:
                # Fallback: show extracted content in dialog
                self.show_pdf_content_dialog(cv_file_path, cv_id)
            
            print(f"Opened CV file: {full_path}")
            
        except Exception as e:
            print(f"Error opening PDF: {e}")
            # Fallback to content dialog
            self.show_pdf_content_dialog(cv_file_path, cv_id)
    
    def show_pdf_content_dialog(self, cv_file_path, cv_id):
        """
        Show PDF content extracted as text in a dialog window
        """
        try:
            # Extract content using the CV data manager
            if self.search_controller and hasattr(self.search_controller, 'cv_data_manager'):
                content = self.search_controller.cv_data_manager.extract_cv_content(cv_file_path, use_regex=True)
            else:
                content = f"Could not extract content from {cv_file_path}"
            
            # Show in dialog
            self.show_cv_content_dialog(cv_id, content)
            
        except Exception as e:
            print(f"Error extracting PDF content: {e}")
            self.show_error_dialog("PDF Extract Error", f"Could not extract PDF content: {str(e)}")
    
    def get_cv_content_from_controller(self, cv_index):
        """Get CV content from search controller if available"""
        try:
            if self.search_controller and hasattr(self.search_controller, 'cv_database'):
                cv_ids = list(self.search_controller.cv_database.keys())
                if 0 <= cv_index < len(cv_ids):
                    cv_id = cv_ids[cv_index]
                    return self.search_controller.get_cv_content(cv_id)
            return None
        except Exception as e:
            print(f"Error getting CV content from controller: {e}")
            return None
    
    def show_cv_content_dialog(self, cv_id, content):
        """Show CV content in a dialog window"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"CV Content - {cv_id}")
        dialog.geometry("700x500")
        dialog.configure(fg_color="#18206F")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        self.center_dialog(dialog, 700, 500)
        
        # Header
        header_label = ctk.CTkLabel(
            dialog,
            text=f"CV Content - {cv_id.replace('_', ' ').title()}",
            font=("Inter", 16, "bold"),
            text_color="white"
        )
        header_label.pack(pady=(20, 10))
        
        # Content text widget
        text_widget = ctk.CTkTextbox(
            dialog,
            width=660,
            height=380,
            fg_color="#F5E2C8",
            text_color="#7C2D12",
            font=("Inter", 11),
            wrap="word"
        )
        text_widget.pack(padx=20, pady=(10, 10))
        
        # Insert content
        text_widget.insert("1.0", content)
        text_widget.configure(state="disabled")  # Read-only
        
        # Close button
        close_btn = ctk.CTkButton(
            dialog,
            text="Close",
            command=dialog.destroy,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            width=100,
            height=35
        )
        close_btn.pack(pady=(10, 20))
    
    def get_dummy_cv_data(self, cv_index):
        """Get dummy CV data for summary - kept as original implementation"""
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
            },
            {
                "full_name": "David Wilson",
                "birth_date": "22-11-1993",
                "address": "Jl. Merdeka No. 45, Surabaya",
                "phone_number": "0877-2345-6789",
                "skills": ["JavaScript", "TypeScript", "React", "Node.js", "MongoDB", "Express"],
                "work_experience": [
                    {
                        "title": "Full Stack Developer",
                        "period": "2021 - 2024",
                        "description": "Developed end-to-end web applications using MERN stack. Implemented real-time features and optimized application performance."
                    }
                ],
                "education": [
                    {
                        "degree": "Bachelor of Software Engineering - Institut Teknologi Sepuluh Nopember",
                        "period": "2015 - 2019"
                    }
                ]
            },
            {
                "full_name": "Lisa Wang",
                "birth_date": "08-07-1991",
                "address": "Jl. Asia Afrika No. 88, Bandung",
                "phone_number": "0895-7654-3210",
                "skills": ["Python", "Machine Learning", "TensorFlow", "Data Analysis", "SQL", "Pandas"],
                "work_experience": [
                    {
                        "title": "Data Scientist",
                        "period": "2019 - 2024",
                        "description": "Analyzed large datasets and built machine learning models for business insights. Specialized in predictive analytics and data visualization."
                    }
                ],
                "education": [
                    {
                        "degree": "Master of Data Science - Universitas Indonesia",
                        "period": "2017 - 2019"
                    }
                ]
            },
            {
                "full_name": "Emily Rodriguez",
                "birth_date": "14-02-1994",
                "address": "Jl. Diponegoro No. 12, Yogyakarta",
                "phone_number": "0813-9876-5432",
                "skills": ["AWS", "Docker", "Kubernetes", "DevOps", "Linux", "Terraform"],
                "work_experience": [
                    {
                        "title": "DevOps Engineer",
                        "period": "2020 - 2024",
                        "description": "Managed cloud infrastructure and CI/CD pipelines. Automated deployment processes and improved system reliability."
                    }
                ],
                "education": [
                    {
                        "degree": "Bachelor of Information Technology - Universitas Gadjah Mada",
                        "period": "2016 - 2020"
                    }
                ]
            }
        ]
        
        # Return data based on index, with fallback to first entry
        if 0 <= cv_index < len(sample_data):
            selected_data = sample_data[cv_index]
        else:
            selected_data = sample_data[cv_index % len(sample_data)]  # Cycle through data
        
        # Format the data for CV summary window
        formatted_data = CVSummaryIntegration.format_cv_data(selected_data)
        return formatted_data
    
    def center_dialog(self, dialog, width, height):
        """Center dialog relative to main window"""
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (width // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
    
    def show_error_dialog(self, title, message):
        """Show error dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.configure(fg_color="#4C1D95")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog relative to main window
        self.center_dialog(dialog, 400, 200)
        
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
        self.center_dialog(dialog, 400, 200)
        
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
    
    def get_search_controller(self):
        """Get search controller instance"""
        return self.search_controller