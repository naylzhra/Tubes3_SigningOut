# home_page.py
import customtkinter as ctk

class HomePage(ctk.CTkScrollableFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill="both", expand=True)
        
        # Initialize variables
        self.selected_algorithm = ctk.StringVar(value="KMP")
        self.matches_count = ctk.IntVar(value=0)
        
        # Reference to main window for navigation
        self.main_window = None
        
        # Setup UI
        self.setup_ui()
    
    def set_main_window(self, main_window):
        """Set reference to main window for navigation"""
        self.main_window = main_window
        
    def setup_ui(self):
        """Setup home page UI components"""
        self.configure(fg_color="transparent")
        
        # Main container with adjusted spacing
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=5)  # Reduced padding
        
        # Search section with compact layout
        search_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 10))  # Reduced padding
        
        # Keywords
        keywords_label = ctk.CTkLabel(
            search_frame,
            text="Keywords:",
            font=("Inter", 12, "bold"),  # Reduced font size
            text_color="white"
        )
        keywords_label.pack(anchor="w", pady=(0, 3))  # Reduced padding
        
        # Search entry
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search",
            height=30,  # Reduced height
            width=200,
            font=("Inter", 10, "bold"),  # Reduced font size
            fg_color="#F5E2C8",
            text_color="#7C2D12",
            placeholder_text_color="#92400E",
            corner_radius=18  # Adjusted corner radius
        )
        self.search_entry.pack(anchor="w", pady=(0, 12))  # Reduced padding
        
        # Algorithm selection
        algo_label = ctk.CTkLabel(
            search_frame,
            text="Search Algorithm:",
            font=("Inter", 12, "bold"),  # Reduced font size
            text_color="white"
        )
        algo_label.pack(anchor="w", pady=(0, 8))  # Reduced padding
        
        # Algorithm buttons frame
        algo_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        algo_frame.pack(anchor="w", pady=(0, 12))  # Reduced padding
        
        # KMP Button
        self.kmp_btn = ctk.CTkButton(
            algo_frame,
            text="KMP",
            width=75,  # Reduced width
            height=28,  # Reduced height
            corner_radius=16,
            fg_color="#F5E2C8",
            text_color="#7C2D12",
            hover_color="#FDE68A",
            font=("Inter", 11, "bold"),  # Reduced font size
            command=lambda: self.select_algorithm("KMP")
        )
        self.kmp_btn.pack(side="left", padx=(0, 8))  # Reduced padding
        
        # BM Button
        self.bm_btn = ctk.CTkButton(
            algo_frame,
            text="BM",
            width=75,  # Reduced width
            height=28,  # Reduced height
            corner_radius=16,
            fg_color="transparent",
            border_color="#F5E2C8",
            border_width=2,
            text_color="white",
            hover_color="#F5E2C8",
            font=("Inter", 11, "bold"),  # Reduced font size
            command=lambda: self.select_algorithm("BM")
        )
        self.bm_btn.pack(side="left", padx=(0, 8))  # Reduced padding
        
        # Fuzzy Matching Button
        self.fuzzy_btn = ctk.CTkButton(
            algo_frame,
            text="Fuzzy Matching",
            width=130,  # Reduced width
            height=28,  # Reduced height
            corner_radius=16,
            fg_color="transparent",
            border_color="#F5E2C8",
            border_width=2,
            text_color="white",
            hover_color="#F5E2C8",
            font=("Inter", 11, "bold"),  # Reduced font size
            command=lambda: self.select_algorithm("Fuzzy")
        )
        self.fuzzy_btn.pack(side="left")
        
        # Top Matches section
        matches_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        matches_frame.pack(anchor="w", pady=(0, 12))  # Reduced padding
        
        matches_label = ctk.CTkLabel(
            matches_frame,
            text="Top Matches:",
            font=("Inter", 12, "bold"),  # Reduced font size
            text_color="white"
        )
        matches_label.pack(side="left", padx=(0, 15), pady = 10)  # Reduced padding
        
        # Counter frame
        counter_frame = ctk.CTkFrame(matches_frame, fg_color="#F5E2C8", height=28, corner_radius=16)  # Reduced height
        counter_frame.pack(side="left")
        
        minus_btn = ctk.CTkButton(
            counter_frame,
            text="-",
            width=22,  # Reduced width
            height=22,  # Reduced height
            corner_radius=16,
            fg_color="transparent",
            text_color="#7C2D12",
            hover_color="#FDE68A",
            font=("Inter", 14, "bold"),
            command=self.decrease_matches
        )
        minus_btn.pack(side="left", padx=4, pady=2)  # Reduced padding
        
        self.count_label = ctk.CTkLabel(
            counter_frame,
            text="0",
            font=("Inter", 13, "bold"),  # Reduced font size
            text_color="#7C2D12",
            width=25  # Reduced width
        )
        self.count_label.pack(side="left", pady=2)
        
        plus_btn = ctk.CTkButton(
            counter_frame,
            text="+",
            width=22,  # Reduced width
            height=22,  # Reduced height
            corner_radius=16,
            fg_color="transparent",
            text_color="#7C2D12",
            hover_color="#FDE68A",
            font=("Inter", 14, "bold"),
            command=self.increase_matches
        )
        plus_btn.pack(side="left", padx=4, pady=2)  # Reduced padding
        
        # Search button
        search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            height=28,  # Reduced height
            width=110,  # Reduced width
            corner_radius=18,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            font=("Inter", 12, "bold"),  # Reduced font size
            command=self.perform_search
        )
        search_btn.pack(anchor="w", pady=5) # Reduced padding
        
        # Results section with reduced spacing
        self.create_results_section(main_container)
    
    def select_algorithm(self, algorithm):
        """Handle algorithm button selection"""
        self.selected_algorithm.set(algorithm)
        
        # Update button styles
        buttons = {
            "KMP": self.kmp_btn,
            "BM": self.bm_btn,
            "Fuzzy": self.fuzzy_btn
        }
        
        for name, btn in buttons.items():
            if name == algorithm:
                btn.configure(fg_color="#F5E2C8", text_color="#7C2D12", border_width=0)
            else:
                btn.configure(fg_color="transparent", text_color="white", border_width=2, border_color="#F5E2C8")
    
    def increase_matches(self):
        """Increase matches count"""
        current = self.matches_count.get()
        if current < 50:  # Set max limit
            self.matches_count.set(current + 1)
            self.count_label.configure(text=str(current + 1))
    
    def decrease_matches(self):
        """Decrease matches count"""
        current = self.matches_count.get()
        if current > 0:
            self.matches_count.set(current - 1)
            self.count_label.configure(text=str(current - 1))
    
    def perform_search(self):
        """Handle search button click"""
        keywords = self.search_entry.get()
        algorithm = self.selected_algorithm.get()
        top_matches = self.matches_count.get()
        
        print(f"Searching for: {keywords}")
        print(f"Algorithm: {algorithm}")
        print(f"Top matches: {top_matches}")
        
        # TODO: Connect to search controller
        # from controller.searcher import SearchController
        # search_controller = SearchController()
        # results = search_controller.search_cvs(keywords, algorithm, top_matches)
        # self.display_search_results(results)
        
        # For now, just update the results display
        self.update_results_display()
    
    def create_results_section(self, parent):
        """Create the results display section"""
        results_container = ctk.CTkFrame(parent, fg_color="transparent")
        results_container.pack(fill="both", expand=True)
        
        # Results header
        results_label = ctk.CTkLabel(
            results_container,
            text="Results",
            font=("Inter", 20, "bold"),  # Reduced font size
            text_color="white"
        )
        results_label.pack(pady=(0, 8))  # Reduced padding
        
        # Results summary
        self.results_summary = ctk.CTkLabel(
            results_container,
            text="100 CVs scanned in 100ms",
            font=("Inter", 12),  # Reduced font size
            text_color="#E5E7EB"
        )
        self.results_summary.pack(pady=(0, 15))  # Reduced padding
        
        # Results grid container with adjusted spacing
        self.results_grid = ctk.CTkFrame(results_container, fg_color="transparent")
        self.results_grid.pack(fill="both", expand=True)
        
        # Configure grid columns to be responsive with adjusted minimum size
        for i in range(3):
            self.results_grid.grid_columnconfigure(i, weight=1, minsize=180)  # Reduced minsize
        
        # Create sample result cards
        self.create_sample_results()
    
    def create_sample_results(self):
        """Create sample result cards"""
        for i in range(3):
            self.create_result_card(i)
    
    def create_result_card(self, index):
        """Create a single result card with click navigation"""
        card = ctk.CTkFrame(
            self.results_grid,
            width=180,  # Reduced width
            height=180,  # Reduced height
            fg_color="#F5E2C8",
            corner_radius=15
        )
        card.grid(row=0, column=index, padx=10, pady=10, sticky="nsew")
        card.grid_propagate(False)
        
        # Make the entire card clickable by binding click events
        card.bind("<Button-1>", lambda event, idx=index: self.on_card_click(idx))
        
        # Name (also make clickable)
        name_label = ctk.CTkLabel(
            card,
            text="Newa",
            font=("Inter", 18, "bold"),
            text_color="#7C2D12"
        )
        name_label.pack(pady=(15, 5))
        name_label.bind("<Button-1>", lambda event, idx=index: self.on_card_click(idx))
        
        # Matches count
        matches_label = ctk.CTkLabel(
            card,
            text="4 Matches",
            font=("Inter", 12),
            text_color="#92400E"
        )
        matches_label.pack(pady=(0, 10))
        matches_label.bind("<Button-1>", lambda event, idx=index: self.on_card_click(idx))
        
        # Keywords section
        keywords_frame = ctk.CTkFrame(card, fg_color="transparent")
        keywords_frame.pack(fill="x", padx=15, pady=(0, 15))
        keywords_frame.bind("<Button-1>", lambda event, idx=index: self.on_card_click(idx))
        
        keywords_title = ctk.CTkLabel(
            keywords_frame,
            text="Matched Keywords:",
            font=("Inter", 11, "bold"),
            text_color="#7C2D12"
        )
        keywords_title.pack(anchor="w")
        keywords_title.bind("<Button-1>", lambda event, idx=index: self.on_card_click(idx))
        
        # Keywords list
        keywords = ["• Chef (1)", "• International (1)", "• Food (1)"]
        for keyword in keywords:
            keyword_label = ctk.CTkLabel(
                keywords_frame,
                text=keyword,
                font=("Inter", 10),
                text_color="#92400E"
            )
            keyword_label.pack(anchor="w", pady=1)
            keyword_label.bind("<Button-1>", lambda event, idx=index: self.on_card_click(idx))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(card, fg_color="transparent")
        buttons_frame.pack(side="bottom", fill="x", padx=15, pady=15)
        
        # Summary button
        summary_btn = ctk.CTkButton(
            buttons_frame,
            text="Summary",
            width=80,
            height=30,
            corner_radius=15,
            fg_color="#18206F",
            hover_color="#18206F",
            font=("Inter", 11),
            command=lambda idx=index: self.show_summary(idx)
        )
        summary_btn.pack(side="left", padx=(0, 5))
        
        # View CV button
        view_btn = ctk.CTkButton(
            buttons_frame,
            text="View CV",
            width=80,
            height=30,
            corner_radius=15,
            fg_color="#18206F",
            hover_color="#18206F",
            font=("Inter", 11),
            command=lambda idx=index: self.view_cv(idx)
        )
        view_btn.pack(side="right")
    
    def on_card_click(self, cv_index):
        """Handle card click - navigate to CV summary"""
        print(f"Card {cv_index} clicked - navigating to CV summary")
        self.show_summary(cv_index)
    
    def update_results_display(self):
        """Update results after search"""
        # TODO: Update with real search results
        self.results_summary.configure(text="25 CVs scanned in 45ms")
    
    def display_search_results(self, results):
        """Display search results from controller"""
        # TODO: Implement real results display
        # Clear existing results
        # for widget in self.results_grid.winfo_children():
        #     widget.destroy()
        # 
        # # Create new result cards based on results
        # for i, result in enumerate(results['results']):
        #     self.create_real_result_card(i, result)
        # 
        # # Update summary
        # timing = results['timing']
        # summary_text = f"Exact Match: {timing['total_cvs']} CVs scanned in {timing['exact_match_ms']}ms.\n"
        # summary_text += f"Fuzzy Match: {timing['total_cvs']} CVs scanned in {timing['fuzzy_match_ms']}ms."
        # self.results_summary.configure(text=summary_text)
        pass
    
    def show_summary(self, cv_index):
        """Show CV summary - navigate to summary window"""
        print(f"Showing summary for CV {cv_index}")
        
        if self.main_window:
            # Call the main window's method to show CV summary
            self.main_window.show_cv_summary(cv_index)
        else:
            print("Warning: Main window reference not set")
            # Fallback - try to create summary window directly
            try:
                from .cv_summary_window import CVSummaryWindow
                # Get the root window
                root = self.winfo_toplevel()
                CVSummaryWindow(root)
            except Exception as e:
                print(f"Error opening summary: {e}")
    
    def view_cv(self, cv_index):
        """View full CV"""
        print(f"Viewing CV {cv_index}")
        
        if self.main_window:
            # Call the main window's method to view CV file
            self.main_window.view_cv_file(cv_index)
        else:
            print("Warning: Main window reference not set")
            # TODO: Implement fallback CV viewer
    
    def get_search_data(self):
        """Get current search parameters"""
        return {
            'keywords': self.search_entry.get(),
            'algorithm': self.selected_algorithm.get(),
            'top_matches': self.matches_count.get()
        }