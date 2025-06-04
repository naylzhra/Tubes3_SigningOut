# home_page.py
import customtkinter as ctk

class HomePage(ctk.CTkScrollableFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Initialize variables
        self.selected_algorithm = ctk.StringVar(value="KMP")
        self.matches_count = ctk.IntVar(value=0)
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup home page UI components"""
        self.configure(fg_color="transparent")
        
        # Main container with proper spacing
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Search section
        search_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 30))
        
        # Keywords
        keywords_label = ctk.CTkLabel(
            search_frame,
            text="Keywords:",
            font=("Inter", 16, "bold"),
            text_color="white"
        )
        keywords_label.pack(anchor="w", pady=(0, 10))
        
        # Search entry
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search",
            height=40,
            width=400,
            font=("Inter", 14),
            fg_color="#F5E2C8",
            text_color="#7C2D12",
            placeholder_text_color="#92400E",
            corner_radius=20
        )
        self.search_entry.pack(anchor="w", pady=(0, 20))
        
        # Algorithm selection
        algo_label = ctk.CTkLabel(
            search_frame,
            text="Search Algorithm:",
            font=("Inter", 16, "bold"),
            text_color="white"
        )
        algo_label.pack(anchor="w", pady=(0, 10))
        
        # Algorithm buttons frame
        algo_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        algo_frame.pack(anchor="w", pady=(0, 20))
        
        # KMP Button
        self.kmp_btn = ctk.CTkButton(
            algo_frame,
            text="KMP",
            width=80,
            height=35,
            corner_radius=17,
            fg_color="#F5E2C8",
            text_color="#7C2D12",
            hover_color="#FDE68A",
            font=("Inter", 12, "bold"),
            command=lambda: self.select_algorithm("KMP")
        )
        self.kmp_btn.pack(side="left", padx=(0, 10))
        
        # BM Button
        self.bm_btn = ctk.CTkButton(
            algo_frame,
            text="BM",
            width=80,
            height=35,
            corner_radius=17,
            fg_color="transparent",
            border_color="#F5E2C8",
            border_width=2,
            text_color="white",
            hover_color="#F5E2C8",
            font=("Inter", 12, "bold"),
            command=lambda: self.select_algorithm("BM")
        )
        self.bm_btn.pack(side="left", padx=(0, 10))
        
        # Fuzzy Matching Button
        self.fuzzy_btn = ctk.CTkButton(
            algo_frame,
            text="Fuzzy Matching",
            width=140,
            height=35,
            corner_radius=17,
            fg_color="transparent",
            border_color="#F5E2C8",
            border_width=2,
            text_color="white",
            hover_color="#F5E2C8",
            font=("Inter", 12, "bold"),
            command=lambda: self.select_algorithm("Fuzzy")
        )
        self.fuzzy_btn.pack(side="left")
        
        # Top Matches section
        matches_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        matches_frame.pack(anchor="w", pady=(0, 20))
        
        matches_label = ctk.CTkLabel(
            matches_frame,
            text="Top Matches:",
            font=("Inter", 16, "bold"),
            text_color="white"
        )
        matches_label.pack(side="left", padx=(0, 20))
        
        # Counter frame
        counter_frame = ctk.CTkFrame(matches_frame, fg_color="#F5E2C8", height=35, corner_radius=17)
        counter_frame.pack(side="left")
        
        minus_btn = ctk.CTkButton(
            counter_frame,
            text="-",
            width=30,
            height=30,
            corner_radius=15,
            fg_color="transparent",
            text_color="#7C2D12",
            hover_color="#FDE68A",
            font=("Inter", 16, "bold"),
            command=self.decrease_matches
        )
        minus_btn.pack(side="left", padx=5, pady=2)
        
        self.count_label = ctk.CTkLabel(
            counter_frame,
            text="0",
            font=("Inter", 14, "bold"),
            text_color="#7C2D12",
            width=30
        )
        self.count_label.pack(side="left", pady=2)
        
        plus_btn = ctk.CTkButton(
            counter_frame,
            text="+",
            width=30,
            height=30,
            corner_radius=15,
            fg_color="transparent",
            text_color="#7C2D12",
            hover_color="#FDE68A",
            font=("Inter", 16, "bold"),
            command=self.increase_matches
        )
        plus_btn.pack(side="left", padx=5, pady=2)
        
        # Search button
        search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            height=40,
            width=120,
            corner_radius=20,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            font=("Inter", 14, "bold"),
            command=self.perform_search
        )
        search_btn.pack(anchor="w", pady=20)
        
        # Results section
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
            font=("Inter", 24, "bold"),
            text_color="white"
        )
        results_label.pack(pady=(0, 10))
        
        # Results summary
        self.results_summary = ctk.CTkLabel(
            results_container,
            text="100 CVs scanned in 100ms",
            font=("Inter", 14),
            text_color="#E5E7EB"
        )
        self.results_summary.pack(pady=(0, 20))
        
        # Results grid container with proper spacing
        self.results_grid = ctk.CTkFrame(results_container, fg_color="transparent")
        self.results_grid.pack(fill="both", expand=True)
        
        # Configure grid columns to be responsive
        for i in range(4):
            self.results_grid.grid_columnconfigure(i, weight=1, minsize=250)
        
        # Create sample result cards
        self.create_sample_results()
    
    def create_sample_results(self):
        """Create sample result cards"""
        for i in range(4):
            self.create_result_card(i)
    
    def create_result_card(self, index):
        """Create a single result card"""
        card = ctk.CTkFrame(
            self.results_grid,
            width=240,
            height=220,
            fg_color="#F5E2C8",
            corner_radius=15
        )
        card.grid(row=0, column=index, padx=10, pady=10, sticky="nsew")
        card.grid_propagate(False)
        
        # Name
        name_label = ctk.CTkLabel(
            card,
            text="Newa",
            font=("Inter", 18, "bold"),
            text_color="#7C2D12"
        )
        name_label.pack(pady=(15, 5))
        
        # Matches count
        matches_label = ctk.CTkLabel(
            card,
            text="4 Matches",
            font=("Inter", 12),
            text_color="#92400E"
        )
        matches_label.pack(pady=(0, 10))
        
        # Keywords section
        keywords_frame = ctk.CTkFrame(card, fg_color="transparent")
        keywords_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        keywords_title = ctk.CTkLabel(
            keywords_frame,
            text="Matched Keywords:",
            font=("Inter", 11, "bold"),
            text_color="#7C2D12"
        )
        keywords_title.pack(anchor="w")
        
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
            hover_color="#17255A",
            font=("Inter", 11),
            command=lambda: self.show_summary(index)
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
            hover_color="#17255A",
            font=("Inter", 11),
            command=lambda: self.view_cv(index)
        )
        view_btn.pack(side="right")
    
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
        """Show CV summary"""
        print(f"Showing summary for CV {cv_index}")
        # TODO: Connect to summary window
        # from gui.components.summary_window import SummaryWindow
        # summary_window = SummaryWindow(self, cv_index)
    
    def view_cv(self, cv_index):
        """View full CV"""
        print(f"Viewing CV {cv_index}")
        # TODO: Connect to CV viewer
        # from controller.cv_viewer import CVViewer
        # cv_viewer = CVViewer()
        # cv_viewer.open_cv(cv_index)
    
    def get_search_data(self):
        """Get current search parameters"""
        return {
            'keywords': self.search_entry.get(),
            'algorithm': self.selected_algorithm.get(),
            'top_matches': self.matches_count.get()
        }