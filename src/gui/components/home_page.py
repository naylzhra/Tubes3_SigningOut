# home_page.py
import customtkinter as ctk

class HomePage(ctk.CTkScrollableFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill="both", expand=True)
        
        # Initialize variables
        self.selected_algorithm = ctk.StringVar(value="KMP")
        self.matches_count = ctk.IntVar(value=5)  # Default to 5
        
        # Reference to main window for navigation
        self.main_window = None
        
        # Search controller
        self.search_controller = None
        
        # Current search results
        self.current_results = []
        
        # Setup UI
        self.setup_ui()
    
    def set_main_window(self, main_window):
        """Set reference to main window for navigation"""
        self.main_window = main_window
        
        # Initialize search controller
        try:
            from controller.searcher import SearchController
            self.search_controller = SearchController()
            print("Search controller initialized successfully")
        except Exception as e:
            print(f"Error initializing search controller: {e}")
            # Create a mock controller for testing
            self.search_controller = self.create_mock_controller()
    
    def create_mock_controller(self):
        """Create mock controller if real one fails"""
        class MockController:
            def search_cvs(self, keywords, algorithm, top_n):
                return {
                    "results": [],
                    "summary": {
                        "total_cvs_searched": 6,
                        "cvs_with_matches": 0,
                        "search_time_ms": 0,
                        "algorithm_used": algorithm,
                        "keywords_searched": 0
                    }
                }
        return MockController()
        
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
            text="Keywords (separate with commas or spaces):",
            font=("Inter", 12, "bold"),  # Reduced font size
            text_color="white"
        )
        keywords_label.pack(anchor="w", pady=(0, 3))  # Reduced padding
        
        # Search entry with example placeholder
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="e.g. python, javascript, react",
            height=30,  # Reduced height
            width=300,  # Increased width for better visibility
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
            text="5",  # Default value
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
        if current > 1:  # Minimum 1
            self.matches_count.set(current - 1)
            self.count_label.configure(text=str(current - 1))
    
    def perform_search(self):
        """Handle search button click - now with real KMP integration"""
        keywords = self.search_entry.get().strip()
        algorithm = self.selected_algorithm.get()
        top_matches = self.matches_count.get()
        
        print(f"Searching for: '{keywords}'")
        print(f"Algorithm: {algorithm}")
        print(f"Top matches: {top_matches}")
        
        if not keywords:
            print("No keywords entered")
            self.show_empty_results()
            return
        
        try:
            # Perform actual search using the controller
            results = self.search_controller.search_cvs(keywords, algorithm, top_matches)
            
            # Store results and display them
            self.current_results = results
            self.display_search_results(results)
            
            print(f"Search completed: {results['summary']}")
            
        except Exception as e:
            print(f"Search error: {e}")
            self.show_error_message(f"Search failed: {str(e)}")
    
    def show_empty_results(self):
        """Show empty results when no keywords provided"""
        self.results_summary.configure(text="Please enter keywords to search")
        # Clear existing results
        self.clear_results_grid()
    
    def show_error_message(self, message):
        """Show error message in results area"""
        self.results_summary.configure(text=f"Error: {message}")
        self.clear_results_grid()
    
    def clear_results_grid(self):
        """Clear all result cards from grid"""
        for widget in self.results_grid.winfo_children():
            widget.destroy()
    
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
            text="Enter keywords and click search to find matching CVs",
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
    
    def display_search_results(self, results):
        """Display real search results from KMP algorithm"""
        # Clear existing results
        self.clear_results_grid()
        
        # Update summary
        summary = results['summary']
        algorithm = summary['algorithm_used']
        time_ms = summary['search_time_ms']
        total_cvs = summary['total_cvs_searched']
        matches = summary['cvs_with_matches']
        
        summary_text = f"{algorithm}: {matches}/{total_cvs} CVs matched in {time_ms}ms"
        self.results_summary.configure(text=summary_text)
        
        # Display result cards
        search_results = results['results']
        
        if not search_results:
            # Show no results message
            no_results_label = ctk.CTkLabel(
                self.results_grid,
                text="No matching CVs found.\nTry different keywords or algorithms.",
                font=("Inter", 14),
                text_color="#E5E7EB",
                justify="center"
            )
            no_results_label.grid(row=0, column=1, pady=50)
            return
        
        # Show result cards in grid
        row = 0
        col = 0
        max_cols = 3
        
        for i, result in enumerate(search_results):
            self.create_real_result_card(result, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def create_real_result_card(self, result, row, col):
        """Create a result card with real data from search"""
        card = ctk.CTkFrame(
            self.results_grid,
            width=180,  # Reduced width
            height=180,  # Reduced height
            fg_color="#F5E2C8",
            corner_radius=15
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        card.grid_propagate(False)
        
        # Make the entire card clickable
        cv_id = result["cv_id"]
        card.bind("<Button-1>", lambda event, cv_id=cv_id: self.on_card_click(cv_id))
        
        # Name (from search results)
        name_label = ctk.CTkLabel(
            card,
            text=result["name"],
            font=("Inter", 16, "bold"),  # Slightly smaller
            text_color="#7C2D12"
        )
        name_label.pack(pady=(15, 5))
        name_label.bind("<Button-1>", lambda event, cv_id=cv_id: self.on_card_click(cv_id))
        
        # Matches count
        total_matches = result["total_matches"]
        matches_text = f"{total_matches} Match{'es' if total_matches != 1 else ''}"
        matches_label = ctk.CTkLabel(
            card,
            text=matches_text,
            font=("Inter", 12),
            text_color="#92400E"
        )
        matches_label.pack(pady=(0, 10))
        matches_label.bind("<Button-1>", lambda event, cv_id=cv_id: self.on_card_click(cv_id))
        
        # Keywords section
        keywords_frame = ctk.CTkFrame(card, fg_color="transparent")
        keywords_frame.pack(fill="x", padx=15, pady=(0, 15))
        keywords_frame.bind("<Button-1>", lambda event, cv_id=cv_id: self.on_card_click(cv_id))
        
        keywords_title = ctk.CTkLabel(
            keywords_frame,
            text="Matched Keywords:",
            font=("Inter", 11, "bold"),
            text_color="#7C2D12"
        )
        keywords_title.pack(anchor="w")
        keywords_title.bind("<Button-1>", lambda event, cv_id=cv_id: self.on_card_click(cv_id))
        
        # Keywords list (limit to 3 for space)
        matched_keywords = result["matched_keywords"][:3]  # Show max 3
        for keyword in matched_keywords:
            keyword_label = ctk.CTkLabel(
                keywords_frame,
                text=keyword,
                font=("Inter", 9),  # Smaller font
                text_color="#92400E"
            )
            keyword_label.pack(anchor="w", pady=1)
            keyword_label.bind("<Button-1>", lambda event, cv_id=cv_id: self.on_card_click(cv_id))
        
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
            hover_color="#1E40AF",
            font=("Inter", 11),
            command=lambda cv_id=cv_id: self.show_summary(cv_id)
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
            hover_color="#1E40AF",
            font=("Inter", 11),
            command=lambda cv_id=cv_id: self.view_cv(cv_id)
        )
        view_btn.pack(side="right")
    
    def on_card_click(self, cv_id):
        """Handle card click - navigate to CV summary"""
        print(f"Card clicked for CV: {cv_id}")
        self.show_summary(cv_id)
    
    def show_summary(self, cv_id):
        """Show CV summary - navigate to summary window"""
        print(f"Showing summary for CV: {cv_id}")
        
        if self.main_window:
            # Convert CV ID to index for compatibility with existing summary system
            cv_index = self.cv_id_to_index(cv_id)
            self.main_window.show_cv_summary(cv_index)
        else:
            print("Warning: Main window reference not set")
    
    def view_cv(self, cv_id):
        """View full CV content"""
        print(f"Viewing CV: {cv_id}")
        
        if self.search_controller:
            try:
                cv_content = self.search_controller.get_cv_content(cv_id)
                self.show_cv_content_dialog(cv_id, cv_content)
            except Exception as e:
                print(f"Error viewing CV: {e}")
        
        if self.main_window:
            cv_index = self.cv_id_to_index(cv_id)
            self.main_window.view_cv_file(cv_index)
    
    def cv_id_to_index(self, cv_id):
        """Convert CV ID to index for compatibility"""
        # Simple mapping for compatibility with existing summary system
        cv_mapping = {
            "cv_1": 0,
            "cv_2": 1,
            "cv_3": 2,
            "cv_4": 3,
            "cv_5": 4,
            "cv_6": 5
        }
        return cv_mapping.get(cv_id, 0)
    
    def show_cv_content_dialog(self, cv_id, content):
        """Show CV content in a dialog"""
        if not self.main_window:
            return
            
        # Create dialog window
        dialog = ctk.CTkToplevel(self.main_window)
        dialog.title(f"CV Content - {cv_id}")
        dialog.geometry("600x400")
        dialog.configure(fg_color="#18206F")
        dialog.transient(self.main_window)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = self.main_window.winfo_x() + 100
        y = self.main_window.winfo_y() + 100
        dialog.geometry(f"600x400+{x}+{y}")
        
        # Content text widget
        text_widget = ctk.CTkTextbox(
            dialog,
            width=560,
            height=320,
            fg_color="#F5E2C8",
            text_color="#7C2D12",
            font=("Inter", 11)
        )
        text_widget.pack(padx=20, pady=(20, 10))
        
        # Insert content
        text_widget.insert("1.0", content)
        text_widget.configure(state="disabled")  # Read-only
        
        # Close button
        close_btn = ctk.CTkButton(
            dialog,
            text="Close",
            command=dialog.destroy,
            fg_color="#DC2626",
            hover_color="#B91C1C"
        )
        close_btn.pack(pady=10)
    
    def get_search_data(self):
        """Get current search parameters"""
        return {
            'keywords': self.search_entry.get(),
            'algorithm': self.selected_algorithm.get(),
            'top_matches': self.matches_count.get()
        }
    
    def get_current_results(self):
        """Get current search results"""
        return self.current_results