import customtkinter as ctk
from .splash_screen import SplashScreen
from .home_page import HomePage
from .cv_summary_window import CVSummaryIntegration
from .about_page import AboutPage
from .developer_page import DeveloperPage

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("SignHire - Professional ATS System")
        self.geometry("800x600")
        self.configure(fg_color="#18206F")  
        self.resizable(False, False) 
        
        self.center_window()
        self.current_page = None
        self.pages = {}
        self.search_controller = None
        self.init_search_controller()
        self.withdraw()
        self.show_splash()
    
    def init_search_controller(self):
        try:
            from controller.searcher import SearchController
            self.search_controller = SearchController()
            print("Search controller initialized successfully with all algorithms")
        except ImportError as e:
            print(f"Could not import SearchController: {e}")
            self.search_controller = None
        except Exception as e:
            print(f"Could not initialize search controller: {e}")
            self.search_controller = None
    
    def center_window(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        self.geometry(f"800x600+{x}+{y}")
    
    def show_splash(self):
        splash = SplashScreen(self, self.on_splash_complete)
    
    def on_splash_complete(self):
        self.deiconify()  # Show main windownya
        self.center_window() 
        self.setup_ui()
    
    def setup_ui(self):
        self.create_header()
        
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(5, 20))
        self.initialize_pages()
        self.show_page('home')
    
    def create_header(self):
        header_frame = ctk.CTkFrame(self, height=80, fg_color="transparent")
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
        title_label.pack(pady=(10, 10))
        
        nav_frame = ctk.CTkFrame(center_container, fg_color="transparent")
        nav_frame.pack(pady=(0, 5))
        
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
        
        self.nav_buttons = {
            'home': self.home_btn,
            'about': self.about_btn,
            'developer': self.dev_btn
        }
    
    def initialize_pages(self):
        self.pages['home'] = HomePage(self.content_frame)
        self.pages['about'] = AboutPage(self.content_frame)
        self.pages['developer'] = DeveloperPage(self.content_frame)
        
        self.pages['home'].set_main_window(self)
        # hide dulu
        for page in self.pages.values():
            page.pack_forget()
    
    def show_page(self, page_name):
        if self.current_page and self.current_page in self.pages: # hide yang aktif page
            self.pages[self.current_page].pack_forget()
        
        if page_name in self.pages:
            self.pages[page_name].pack(fill="both", expand=True)
            self.current_page = page_name
            
            self.update_nav_buttons(page_name)
    
    def update_nav_buttons(self, active_page):
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
    
    def perform_search(self, keywords, algorithm, top_matches):
        print(f"Main Window - Search requested:")
        print(f"  Keywords: {keywords}")
        print(f"  Algorithm: {algorithm}")
        print(f"  Top Matches: {top_matches}")
        
        if self.search_controller:
            try:
                results = self.search_controller.search_cvs(keywords, algorithm, top_matches)
                
                home_page = self.pages['home']
                home_page.display_search_results(results)
                
                algorithm_used = results['summary']['algorithm_used']
                result_count = len(results['results'])
                
                print(f"{algorithm_used} Search completed: {result_count} results found")
                
            except Exception as e:
                print(f"Search error: {e}")
                self.show_error_dialog("Search Error", f"An error occurred during search: {str(e)}")
        else:
            print("Search controller not available, using simulation")
    
    
    def show_cv_summary(self, cv_index):
        print(f"Main Window - Show summary for CV {cv_index}")
        try:
            if self.search_controller and hasattr(self.search_controller, 'cv_database'):
                cv_ids = list(self.search_controller.cv_database.keys())
                if 0 <= cv_index < len(cv_ids):
                    cv_id = cv_ids[cv_index]
                    
                    cv_data = CVSummaryIntegration.format_cv_data_from_database(
                        self.search_controller, cv_id
                    )
                    
                    if cv_data:
                        summary_window = CVSummaryIntegration.show_cv_summary(
                            self, cv_data, self.search_controller
                        )
                        if summary_window:
                            print(f"CV Summary window opened for CV {cv_id} with database data")
                        return
                    else:
                        print(f"Could not get database data for {cv_id}")
               
        except Exception as e:
            print(f"Error showing CV summary: {e}")
            self.show_error_dialog("CV Summary Error", f"Could not open CV summary: {str(e)}")
            
    def view_cv_file(self, cv_index):
        print(f"Main Window - View CV file {cv_index}")
        
        try:
            if self.search_controller and hasattr(self.search_controller, 'cv_database'):
                cv_ids = list(self.search_controller.cv_database.keys())
                if 0 <= cv_index < len(cv_ids):
                    cv_id = cv_ids[cv_index]
                    
                    cv_file_path = self.search_controller.get_cv_file_path(cv_id)
                    
                    if cv_file_path:
                        self.open_pdf_file(cv_file_path, cv_id)
                        return
                    else:
                        self.show_error_dialog("CV File Error", f"CV file not found for {cv_id}")
                        return
            
            self.show_info_dialog("CV Viewer", f"Opening CV file for applicant {cv_index}...")
            
        except Exception as e:
            print(f"Error viewing CV: {e}")
            self.show_error_dialog("CV Viewer Error", f"Could not open CV: {str(e)}")
    
    def open_pdf_file(self, cv_file_path, cv_id):
        try:
            import os
            import platform
            from pathlib import Path
            
            if not os.path.isabs(cv_file_path):
                project_root = Path(__file__).resolve().parents[3]
                full_path = project_root / cv_file_path
            else:
                full_path = Path(cv_file_path)
            
            if not full_path.exists():
                self.show_error_dialog("File Not Found", f"CV file not found:\n{full_path}")
                return
            
            system = platform.system()
            
            if system == "Windows":
                os.startfile(str(full_path))
            else:
                self.show_pdf_content_dialog(cv_file_path, cv_id)
            
            print(f"Opened CV file: {full_path}")
            
        except Exception as e:
            print(f"Error opening PDF: {e}")
            self.show_pdf_content_dialog(cv_file_path, cv_id)
    
    def show_pdf_content_dialog(self, cv_file_path, cv_id):
        try:
            if self.search_controller and hasattr(self.search_controller, 'cv_data_manager'):
                content = self.search_controller.cv_data_manager.extract_cv_content(cv_file_path, use_regex=True)
            else:
                content = f"Could not extract content from {cv_file_path}"
            
            self.show_cv_content_dialog(cv_id, content)
            
        except Exception as e:
            print(f"Error extracting PDF content: {e}")
            self.show_error_dialog("PDF Extract Error", f"Could not extract PDF content: {str(e)}")
    
    def show_cv_content_dialog(self, cv_id, content):
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"CV Content - {cv_id}")
        dialog.geometry("700x500")
        dialog.configure(fg_color="#18206F")
        dialog.transient(self)
        dialog.grab_set()
        
        self.center_dialog(dialog, 700, 500)
        
        header_label = ctk.CTkLabel(
            dialog,
            text=f"CV Content - {cv_id.replace('_', ' ').title()}",
            font=("Inter", 16, "bold"),
            text_color="white"
        )
        header_label.pack(pady=(20, 10))
        
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
        
        text_widget.insert("1.0", content)
        text_widget.configure(state="disabled")  # Read-only
        
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
    
    
    def center_dialog(self, dialog, width, height):
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (width // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
    
    def show_error_dialog(self, title, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.configure(fg_color="#4C1D95")
        dialog.transient(self)
        dialog.grab_set()
        
        self.center_dialog(dialog, 400, 200)
        
        error_label = ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color="white",
            wraplength=350
        )
        error_label.pack(pady=40)
        
        ok_button = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            fg_color="#DC2626",
            hover_color="#B91C1C"
        )
        ok_button.pack(pady=20)
    
    def show_info_dialog(self, title, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.configure(fg_color="#18206F")
        dialog.transient(self)
        dialog.grab_set()
        
        self.center_dialog(dialog, 400, 200)
        
        info_label = ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color="white",
            wraplength=350
        )
        info_label.pack(pady=40)
        
        ok_button = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            fg_color="#DC2626",
            hover_color="#B91C1C"
        )
        ok_button.pack(pady=20)
    