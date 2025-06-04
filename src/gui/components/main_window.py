# main_window.py
import customtkinter as ctk
from .splash_screen import SplashScreen
from .home_page import HomePage
# from about_page import AboutPage
# from developer_page import DeveloperPage

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("SignHire - Professional ATS System")
        self.geometry("800x600")
        self.configure(fg_color="#17255A")  # Purple background
        
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
    
    def show_splash(self):
        """Display splash screen"""
        splash = SplashScreen(self, self.on_splash_complete)
    
    def on_splash_complete(self):
        """Called when splash screen finishes"""
        self.deiconify()  # Show main window
        self.setup_ui()
    
    def setup_ui(self):
        """Setup main window UI"""
        # Header with navigation
        self.create_header()
        
        # Content area
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Initialize pages
        self.initialize_pages()
        
        # Show home page by default
        self.show_page('home')
    
    def create_header(self):
        """Create navigation header with centered layout"""
        header_frame = ctk.CTkFrame(self, height=120, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 0))
        header_frame.pack_propagate(False)
        
        # Center container untuk semua header content
        center_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        center_container.pack(expand=True, fill="both")
        
        # App title - CENTERED di atas
        title_label = ctk.CTkLabel(
            center_container,
            text="SignHire",
            font=("Inter", 32, "bold"),
            text_color="white"
        )
        title_label.pack(pady=(20, 10))
        
        # Navigation buttons - CENTERED di bawah title
        nav_frame = ctk.CTkFrame(center_container, fg_color="transparent")
        nav_frame.pack(pady=(0, 20))
        
        # Home button
        self.home_btn = ctk.CTkButton(
            nav_frame,
            text="Home",
            font=("Inter", 14, "bold"),
            fg_color="#DC2626",
            hover_color="#B91C1C",
            width=100,
            height=40,
            corner_radius=20,
            command=lambda: self.show_page('home')
        )
        self.home_btn.pack(side="left", padx=(0, 40))  # Spacing yang lebih besar
        
        # About button
        self.about_btn = ctk.CTkButton(
            nav_frame,
            text="About the App",
            font=("Inter", 14),
            fg_color="transparent",
            text_color="white",
            hover_color="#B91C1C",
            width=120,
            height=40,
            command=lambda: self.show_page('about')
        )
        self.about_btn.pack(side="left", padx=(0, 40))  # Spacing yang lebih besar
        
        # Developer button
        self.dev_btn = ctk.CTkButton(
            nav_frame,
            text="Developer",
            font=("Inter", 14),
            fg_color="transparent",
            text_color="white",
            hover_color="#B91C1C",
            width=100,
            height=40,
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
        
        # TODO: Implement summary window
        # from gui.components.summary_window import SummaryWindow
        # summary_window = SummaryWindow(self, cv_index)
        # summary_window.show()
    
    def view_cv_file(self, cv_index):
        """Open CV file viewer"""
        print(f"Main Window - View CV file {cv_index}")
        
        # TODO: Implement CV viewer
        # from controller.cv_viewer import CVViewer
        # try:
        #     cv_viewer = CVViewer()
        #     cv_viewer.open_cv(cv_index)
        # except Exception as e:
        #     self.show_error_dialog("CV Viewer Error", f"Could not open CV: {str(e)}")
    
    def show_error_dialog(self, title, message):
        """Show error dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.configure(fg_color="#4C1D95")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
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


# app.py - Application entry point
if __name__ == "__main__":
    # Set CustomTkinter appearance
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Create and run application
    app = MainWindow()
    app.mainloop()