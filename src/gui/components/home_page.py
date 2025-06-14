import customtkinter as ctk

class HomePage(ctk.CTkScrollableFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill="both", expand=True)
        
        self.selected_algorithm = ctk.StringVar(value="KMP")
        self.matches_count = ctk.IntVar(value=5)  # Default to 5
        
        self.main_window = None
        self.search_controller = None
        self.current_results = []
        self.setup_ui()
    
    def set_main_window(self, main_window):
        self.main_window = main_window
        try:
            from controller.searcher import SearchController
            self.search_controller = SearchController()
            print("Search controller initialized successfully")
        except Exception as e:
            print(f"Error initializing search controller: {e}")
        
    def setup_ui(self):
        self.configure(fg_color="transparent")
        
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=5)
        
        search_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 10))
        
        keywords_label = ctk.CTkLabel(
            search_frame,
            text="Keywords (separate with commas or spaces):",
            font=("Inter", 12, "bold"),
            text_color="white"
        )
        keywords_label.pack(anchor="w", pady=(0, 3))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="e.g. python, javascript, react",
            height=30,
            width=300,
            font=("Inter", 10, "bold"),
            fg_color="#F5E2C8",
            text_color="#7C2D12",
            placeholder_text_color="#92400E",
            corner_radius=18
        )
        self.search_entry.pack(anchor="w", pady=(0, 12))
        
        algo_label = ctk.CTkLabel(
            search_frame,
            text="Search Algorithm:",
            font=("Inter", 12, "bold"),
            text_color="white"
        )
        algo_label.pack(anchor="w", pady=(0, 8))
        
        algo_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        algo_frame.pack(anchor="w", pady=(0, 12))
        
        self.kmp_btn = ctk.CTkButton(
            algo_frame,
            text="KMP",
            width=75,
            height=28,
            corner_radius=16,
            fg_color="#F5E2C8",
            text_color="#7C2D12",
            hover_color="#FDE68A",
            font=("Inter", 11, "bold"),
            command=lambda: self.select_algorithm("KMP")
        )
        self.kmp_btn.pack(side="left", padx=(0, 8))
        
        self.bm_btn = ctk.CTkButton(
            algo_frame,
            text="BM",
            width=75,
            height=28,
            corner_radius=16,
            fg_color="transparent",
            border_color="#F5E2C8",
            border_width=2,
            text_color="white",
            hover_color="#F5E2C8",
            font=("Inter", 11, "bold"),
            command=lambda: self.select_algorithm("BM")
        )
        self.bm_btn.pack(side="left", padx=(0, 8))
        
        self.aho_corasick_btn = ctk.CTkButton(
            algo_frame,
            text="Aho-Corasick",
            width=130,
            height=28,
            corner_radius=16,
            fg_color="transparent",
            border_color="#F5E2C8",
            border_width=2,
            text_color="white",
            hover_color="#F5E2C8",
            font=("Inter", 11, "bold"),
            command=lambda: self.select_algorithm("Aho-Corasick")
        )
        self.aho_corasick_btn.pack(side="left")
        
        matches_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        matches_frame.pack(anchor="w", pady=(0, 12))
        
        matches_label = ctk.CTkLabel(
            matches_frame,
            text="Top Matches:",
            font=("Inter", 12, "bold"),
            text_color="white"
        )
        matches_label.pack(side="left", padx=(0, 15), pady=10)
        
        counter_frame = ctk.CTkFrame(matches_frame, fg_color="#F5E2C8", height=28, corner_radius=16)
        counter_frame.pack(side="left")
        
        minus_btn = ctk.CTkButton(
            counter_frame,
            text="-",
            width=22,
            height=22,
            corner_radius=16,
            fg_color="transparent",
            text_color="#7C2D12",
            hover_color="#FDE68A",
            font=("Inter", 14, "bold"),
            command=self.decrease_matches
        )
        minus_btn.pack(side="left", padx=4, pady=2)
        
        self.count_label = ctk.CTkLabel(
            counter_frame,
            text="5",
            font=("Inter", 13, "bold"),
            text_color="#7C2D12",
            width=25
        )
        self.count_label.pack(side="left", pady=2)
        
        plus_btn = ctk.CTkButton(
            counter_frame,
            text="+",
            width=22,
            height=22,
            corner_radius=16,
            fg_color="transparent",
            text_color="#7C2D12",
            hover_color="#FDE68A",
            font=("Inter", 14, "bold"),
            command=self.increase_matches
        )
        plus_btn.pack(side="left", padx=4, pady=2)
        
        search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            height=28,
            width=110,
            corner_radius=18,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            font=("Inter", 12, "bold"),
            command=self.perform_search
        )
        search_btn.pack(anchor="w", pady=5)
        
        self.create_results_section(main_container)
    
    def select_algorithm(self, algorithm):
        self.selected_algorithm.set(algorithm)
        
        buttons = {
            "KMP": self.kmp_btn,
            "BM": self.bm_btn,
            "Aho-Corasick": self.aho_corasick_btn
        }
        
        for name, btn in buttons.items():
            if name == algorithm:
                btn.configure(fg_color="#F5E2C8", text_color="#7C2D12", border_width=0)
            else:
                btn.configure(fg_color="transparent", text_color="white", border_width=2, border_color="#F5E2C8")
    
    def increase_matches(self):
        current = self.matches_count.get()
        if current < 50:  # limit
            self.matches_count.set(current + 1)
            self.count_label.configure(text=str(current + 1))
    
    def decrease_matches(self):
        current = self.matches_count.get()
        if current > 1: 
            self.matches_count.set(current - 1)
            self.count_label.configure(text=str(current - 1))
    
    def perform_search(self):
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
            results = self.search_controller.search_cvs(keywords, algorithm, top_matches)
            
            self.current_results = results
            self.display_search_results(results)
            
            algorithm_used = results['summary']['algorithm_used']
            result_count = len(results['results'])
            main_time = results['timing']['search_time_ms']
            leven_time = results['timing'].get('levenshtein_time_ms')  # Optional

            print(f"{algorithm_used} search completed: {result_count} results found in {main_time}ms")
            
            if leven_time is not None:
                print(f"Levenshtein additional search took {leven_time}ms")
            
            if "+" in algorithm_used:
                print(f"Fallback mechanism activated: {algorithm_used}")
        
        except Exception as e:
            print(f"Search error: {e}")
            self.show_error_message(f"Search failed: {str(e)}")

    def show_empty_results(self):
        self.results_summary.configure(text="Please enter keywords to search")
        self.clear_results_grid()
    
    def show_error_message(self, message):
        """Show error message in results area"""
        self.results_summary.configure(text=f"Error: {message}")
        self.clear_results_grid()
    
    def clear_results_grid(self):
        for widget in self.results_grid.winfo_children():
            widget.destroy()
    
    def create_results_section(self, parent):
        results_container = ctk.CTkFrame(parent, fg_color="transparent")
        results_container.pack(fill="both", expand=True)
        
        results_label = ctk.CTkLabel(
            results_container,
            text="Results",
            font=("Inter", 20, "bold"),
            text_color="white"
        )
        results_label.pack(pady=(0, 8))
        
        self.results_summary = ctk.CTkLabel(
            results_container,
            text="Enter keywords and click search to find matching CVs",
            font=("Inter", 12),
            text_color="#E5E7EB"
        )
        self.results_summary.pack(pady=(0, 15))
        
        self.results_grid = ctk.CTkFrame(results_container, fg_color="transparent")
        self.results_grid.pack(fill="both", expand=True)
        
        for i in range(3):
            self.results_grid.grid_columnconfigure(i, weight=1, minsize=180)
    
    def display_search_results(self, results):
        self.clear_results_grid()
        
        summary = results['summary']
        timing = results.get('timing', {})
        
        algorithm = summary['algorithm_used']
        time_ms = summary['search_time_ms']
        total_cvs = summary['total_cvs_searched']
        matches = summary['cvs_with_matches']
        levenshtein_time = timing.get('levenshtein_time_ms')

        if "→" in algorithm or "+ Levenshtein" in algorithm:
            summary_text = f"{algorithm}: {matches}/{total_cvs} CVs matched\n"
            summary_text += f"Initial algorithm time: {time_ms}ms"
            if levenshtein_time is not None:
                summary_text += f"\nLevenshtein supplement time: {levenshtein_time}ms"
        else:
            summary_text = f"{algorithm}: {matches}/{total_cvs} CVs matched in {time_ms}ms"

        
        self.results_summary.configure(text=summary_text)
        
        search_results = results['results']
        
        if not search_results:
            no_results_label = ctk.CTkLabel(
                self.results_grid,
                text="No matching CVs found.\nTry different keywords or algorithms.",
                font=("Inter", 14),
                text_color="#E5E7EB",
                justify="center"
            )
            no_results_label.grid(row=0, column=1, pady=50)
            return
        
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
        card = ctk.CTkFrame(
            self.results_grid,
            width=180,
            height=180,
            fg_color="#F5E2C8",
            corner_radius=15
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        card.grid_propagate(False)
        
        # clickable
        cv_id = result["cv_id"]
        card.bind("<Button-1>", lambda event, cv_id=cv_id: self.on_card_click(cv_id))
        
        name_label = ctk.CTkLabel(
            card,
            text=result["name"],
            font=("Inter", 16, "bold"),
            text_color="#7C2D12"
        )
        name_label.pack(pady=(15, 5))
        name_label.bind("<Button-1>", lambda event, cv_id=cv_id: self.on_card_click(cv_id))
        
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
        
        matched_keywords = result["matched_keywords"][:3]  
        for keyword in matched_keywords:
            keyword_label = ctk.CTkLabel(
                keywords_frame,
                text=keyword,
                font=("Inter", 9),
                text_color="#92400E"
            )
            keyword_label.pack(anchor="w", pady=1)
            keyword_label.bind("<Button-1>", lambda event, cv_id=cv_id: self.on_card_click(cv_id))
        
        buttons_frame = ctk.CTkFrame(card, fg_color="transparent")
        buttons_frame.pack(side="bottom", fill="x", padx=15, pady=15)
        
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
        print(f"Card clicked for CV: {cv_id}")
        self.show_summary(cv_id) # refer ke summary
    
    def show_summary(self, cv_id):
        print(f"Showing summary for CV: {cv_id}")
        
        if self.main_window and self.search_controller:
            try:
                summary_data = self.search_controller.get_cv_summary_by_id(cv_id)
                
                if summary_data:
                    from .cv_summary_window import CVSummaryIntegration
                    
                    class CVDataWithID:
                        def __init__(self, data, cv_id):
                            self.cv_id = cv_id
                            for key, value in data.items():
                                setattr(self, key, value)
                        
                        def __getitem__(self, key):
                            return getattr(self, key, "N/A")
                        
                        def get(self, key, default=None):
                            return getattr(self, key, default)
                    
                    enhanced_data = CVDataWithID(summary_data, cv_id)
                    
                    summary_window = CVSummaryIntegration.show_cv_summary(
                        self.main_window, enhanced_data, self.search_controller
                    )
                    
                    if summary_window:
                        print(f"CV Summary window opened for {cv_id} with database data")
                    
                else:
                    print(f"Error showing summary: {e}")

            except Exception as e:
                print(f"Error showing database summary: {e}")
                
        else:
            print("Warning: Main window or search controller reference not set")
    
    def view_cv(self, cv_id):
        
        if self.search_controller:
            try:
                cv_path = self.search_controller.get_cv_file_path(cv_id)
                # print(f"CV file path: {cv_path}")
                cv_content = self.search_controller.cv_data_manager.extract_cv_content(cv_path, True)
                self.show_cv_content_dialog(cv_id, cv_content)
            except Exception as e:
                print(f"Error viewing CV: {e}")
        
        if self.main_window:
            print("Using main window to view CV")
            cv_index = self.cv_id_to_index(cv_id)
            self.main_window.view_cv_file(cv_index)
    
    def cv_id_to_index(self, cv_id):
        try:
            if self.search_controller and hasattr(self.search_controller, 'cv_database'):
                cv_ids = list(self.search_controller.cv_database.keys())
                if cv_id in cv_ids:
                    return cv_ids.index(cv_id)
            
            if cv_id.startswith('cv_'):
                return int(cv_id.split('_')[1]) - 1
            
            return 0
        except Exception as e:
            print(f"Error converting CV ID to index: {e}")
            return 0
    
    def show_cv_content_dialog(self, cv_id, content):
        if not self.main_window:
            return
            
        dialog = ctk.CTkToplevel(self.main_window)
        dialog.title(f"CV Content - {cv_id}")
        dialog.geometry("600x400")
        dialog.configure(fg_color="#18206F")
        dialog.transient(self.main_window)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = self.main_window.winfo_x() + 100
        y = self.main_window.winfo_y() + 100
        dialog.geometry(f"600x400+{x}+{y}")
        
        text_widget = ctk.CTkTextbox(
            dialog,
            width=560,
            height=320,
            fg_color="#F5E2C8",
            text_color="#7C2D12",
            font=("Inter", 11)
        )
        text_widget.pack(padx=20, pady=(20, 10))
        
        text_widget.insert("1.0", content)
        text_widget.configure(state="disabled") 
        
        close_btn = ctk.CTkButton(
            dialog,
            text="Close",
            command=dialog.destroy,
            fg_color="#DC2626",
            hover_color="#B91C1C"
        )
        close_btn.pack(pady=10)
    