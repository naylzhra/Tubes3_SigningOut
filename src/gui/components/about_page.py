# about_page.py
import customtkinter as ctk
import os
from PIL import Image

class AboutPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill="both", expand=True)
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup about page UI components"""
        self.configure(fg_color="transparent")
        
        # Main container - no padding to reach edges
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        # About Us Section
        self.create_about_us_section(main_container)
        
        # Why Our Platform Section
        self.create_why_platform_section(main_container)
        
        # Team Section
        self.create_team_section(main_container)
    
    def create_about_us_section(self, parent):
        """Create About Us section with full width white background"""
        # About Us container - full width dark blue background
        about_container = ctk.CTkFrame(parent, fg_color="#18206f", corner_radius=0)
        about_container.pack(fill="both", expand=True, pady=(0, 0))

        # Inner content container
        inner_container = ctk.CTkFrame(about_container, fg_color="transparent")
        inner_container.pack(fill="both", expand=True, padx=40, pady=30)

        # Main image placeholder - centered
        image_container = ctk.CTkFrame(inner_container, fg_color="transparent")
        image_container.pack(fill="x", pady=(0, 20))

        self.create_main_image(image_container)

        # Content section with two columns
        content_section = ctk.CTkFrame(inner_container, fg_color="transparent")
        content_section.pack(fill="both", expand=True)

        # Left column
        left_column = ctk.CTkFrame(content_section, fg_color="transparent")
        left_column.pack(side="left", fill="both", padx=(0, 30), expand=True)

        # Vertical divider
        divider_frame = ctk.CTkFrame(content_section, fg_color="transparent")
        divider_frame.pack(side="left", fill="y", padx=(0, 30))

        divider = ctk.CTkFrame(divider_frame, width=2, fg_color="#E5E7EB")
        divider.pack(fill="y", padx=15)

        # Right column
        right_column = ctk.CTkFrame(content_section, fg_color="transparent")
        right_column.pack(side="left", fill="both", expand=True)

        # About Us title in left column (center-left)
        about_title = ctk.CTkLabel(
            left_column,
            text="About Us",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="white",
            anchor="w"
        )
        about_title.pack(anchor="w", pady=(80, 0), padx=(10, 0))

        # Right column content
        self.create_right_column_content(right_column)

    def create_main_image(self, parent):
        """Create main image section - centered"""
        try:
            image_path = self.find_image_path("img3.png")

            if image_path and os.path.exists(image_path):
                pil_image = Image.open(image_path)
                pil_image = pil_image.resize((200, 200), Image.Resampling.LANCZOS)

                main_image = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=(200, 200)
                )

                image_label = ctk.CTkLabel(
                    parent,
                    image=main_image,
                    text="",
                    width=200,
                    height=200
                )
                image_label.pack(anchor="center")
                print(f"Main image loaded successfully from: {image_path}")
            else:
                self.create_placeholder_image_centered(parent, 200, 200)

        except Exception as e:
            print(f"Error loading main image: {e}")
            self.create_placeholder_image_centered(parent, 200, 200)

    def create_placeholder_image_centered(self, parent, width, height):
        """Create centered placeholder image when actual image is not found"""
        placeholder = ctk.CTkFrame(
            parent,
            width=width,
            height=height,
            fg_color="#D1D5DB",
            corner_radius=10
        )
        placeholder.pack(anchor="center")
        placeholder.pack_propagate(False)

        placeholder_text = ctk.CTkLabel(
            placeholder,
            text="IMG",
            font=ctk.CTkFont(size=16),
            text_color="#6B7280"
        )
        placeholder_text.pack(expand=True)

    def create_right_column_content(self, parent):
        """Create content for right column"""
        # Main title
        main_title = ctk.CTkLabel(
            parent,
            text="SignHire - Professional ATS System",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white",
            justify="right",
            anchor="w"
        )
        main_title.pack(anchor="w", fill="x", pady=(0, 8))

        # Subtitle
        subtitle = ctk.CTkLabel(
            parent,
            text="Developed by Team SigningOut",
            font=ctk.CTkFont(size=14, slant="italic"),
            text_color="white",
            justify="right",
            anchor="w"
        )
        subtitle.pack(anchor="w", fill="x", pady=(0, 20))

        # Description
        description_text = (
            "SignHire is a comprehensive Applicant Tracking System (ATS) designed to "
            "revolutionize the recruitment process for HR professionals and recruiters. Our "
            "intelligent CV analysis platform transforms how organizations discover, "
            "evaluate, and manage job candidates."
        )
        description = ctk.CTkLabel(
            parent,
            text=description_text,
            font=ctk.CTkFont(size=12),
            text_color="white",
            anchor="w",
            justify="left",
            wraplength=400
        )
        description.pack(anchor="w", fill="x", pady=(0, 20))

        # Features list
        features_text = "HR Departments • Recruitment Agencies • Talent Acquisition Teams • Corporate Recruiters"
        features = ctk.CTkLabel(
            parent,
            text=features_text,
            font=ctk.CTkFont(size=11),
            text_color="white",
            anchor="w",
            wraplength=500
        )
        features.pack(anchor="w", fill="x")

    def create_why_platform_section(self, parent):
        """Create Why Our Platform section"""
        # Platform section container - no top padding to connect with white section
        platform_container = ctk.CTkFrame(parent, fg_color="#18206F", corner_radius=0)
        platform_container.pack(fill="both", expand=True)
        
        # Content with padding
        content_frame = ctk.CTkFrame(platform_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Section title
        title_label = ctk.CTkLabel(
            content_frame,
            text="Why Our Platform is\nYour Ideal Choice",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white",
            justify="center"
        )
        title_label.pack(pady=(0, 30))
        
        # Key Features container
        features_container = ctk.CTkFrame(content_frame, fg_color="#E8D5B7", corner_radius=15)
        features_container.pack(fill="x")
        
        # Key Features content
        features_content = ctk.CTkFrame(features_container, fg_color="transparent")
        features_content.pack(fill="both", expand=True, padx=30, pady=25)
        
        # Key Features label
        key_features_label = ctk.CTkLabel(
            features_content,
            text="Key Features",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#2D1B69",
            anchor="w"
        )
        key_features_label.pack(anchor="w", pady=(0, 20))
        
        # Features grid
        self.create_features_grid(features_content)
    
    def create_team_section(self, parent):
        """Create Team section"""
        # Team container - continuing purple background
        team_container = ctk.CTkFrame(parent, fg_color="#18206F", corner_radius=0)
        team_container.pack(fill="both", expand=True)
        
        # Content with padding
        content_frame = ctk.CTkFrame(team_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Team title
        team_title = ctk.CTkLabel(
            content_frame,
            text="Team SigningOut",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        team_title.pack(pady=(0, 15))
        
        # Team description
        team_desc = ctk.CTkLabel(
            content_frame,
            text="Transform your hiring process with SignHire - where\nintelligent algorithms meet intuitive design.",
            font=ctk.CTkFont(size=15),
            text_color="#E5E7EB",
            justify="center"
        )
        team_desc.pack()
    
    def create_why_platform_section(self, parent):
        """Create Why Our Platform section"""
        # Platform section container - no top padding to connect with white section
        platform_container = ctk.CTkFrame(parent, fg_color="#18206F", corner_radius=0)
        platform_container.pack(fill="both", expand=True)

        # Content with padding
        content_frame = ctk.CTkFrame(platform_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=40, pady=40)

        # Section title
        title_label = ctk.CTkLabel(
            content_frame,
            text="Why Our Platform is\nYour Ideal Choice",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="white",
            justify="center"
        )
        title_label.pack(pady=(0, 30))

        # Key Features container
        features_container = ctk.CTkFrame(content_frame, fg_color="#E8D5B7", corner_radius=15)
        features_container.pack(fill="x")

        # Key Features content
        features_content = ctk.CTkFrame(features_container, fg_color="transparent")
        features_content.pack(fill="both", expand=True, padx=30, pady=25)

        # Key Features label
        key_features_label = ctk.CTkLabel(
            features_content,
            text="Key Features",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#2D1B69",
            anchor="w"
        )
        key_features_label.pack(anchor="w", pady=(0, 10))

        # Features grid
        self.create_features_grid(features_content)


    def create_features_grid(self, parent):
        """Create features grid with 4 items"""
        grid_frame = ctk.CTkFrame(parent, fg_color="transparent")
        grid_frame.pack(fill="x")

        # Configure grid
        for i in range(4):
            grid_frame.grid_columnconfigure(i, weight=1, minsize=150)

        # Features data with specific image files
        features = [
            {
                "title": "Smart CV Analysis",
                "description": "Automated PDF text extraction and intelligent keyword matching",
                "image": "img4.png"
            },
            {
                "title": "Advanced Search",
                "description": "Boyer-Moore algorithms for precise search results",
                "image": "img5.png"
            },
            {
                "title": "Fuzzy Matching",
                "description": "Find relevant candidates even with typos using Levenshtein Distance",
                "image": "img6.png"
            },
            {
                "title": "Complete Profiles",
                "description": "Automatic extraction of skills, experience, and education details",
                "image": "img7.png"
            }
        ]

        # Create feature cards
        for i, feature in enumerate(features):
            self.create_feature_card(grid_frame, feature, i)


    def create_feature_card(self, parent, feature_data, index):
        """Create individual feature card"""
        card = ctk.CTkFrame(parent, fg_color="transparent")
        card.grid(row=0, column=index, padx=10, pady=5, sticky="nsew")

        # Feature image
        self.create_feature_image(card, feature_data["image"])

        # Feature title
        title_label = ctk.CTkLabel(
            card,
            text=feature_data["title"],
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#2D1B69",
            anchor="center"
        )
        title_label.pack(pady=(10, 5))

        # Feature description
        desc_label = ctk.CTkLabel(
            card,
            text=feature_data["description"],
            font=ctk.CTkFont(size=10),
            text_color="#6B7280",
            anchor="center",
            justify="center",
            wraplength=120
        )
        desc_label.pack(pady=(0, 10))


    def create_feature_image(self, parent, filename):
        """Create feature image based on provided filename"""
        try:
            image_path = self.find_image_path(filename)

            if image_path and os.path.exists(image_path):
                pil_image = Image.open(image_path)
                pil_image = pil_image.resize((60, 60), Image.Resampling.LANCZOS)

                feature_image = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=(60, 60)
                )

                image_label = ctk.CTkLabel(
                    parent,
                    image=feature_image,
                    text="",
                    width=60,
                    height=60
                )
                image_label.pack(pady=(10, 0))
            else:
                self.create_placeholder_image(parent, 60, 60)

        except Exception as e:
            print(f"Error loading feature image '{filename}': {e}")
            self.create_placeholder_image(parent, 60, 60)

    def create_team_section(self, parent):
        """Create Team section"""
        # Team container
        team_container = ctk.CTkFrame(parent, fg_color="#18206F", corner_radius=15)
        team_container.pack(fill="x")
        
        # Content with padding
        content_frame = ctk.CTkFrame(team_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Team title
        team_title = ctk.CTkLabel(
            content_frame,
            text="Team SigningOut",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        team_title.pack(pady=(0, 10))
        
        # Team description
        team_desc = ctk.CTkLabel(
            content_frame,
            text="Transform your hiring process with SignHire\n - whereintelligent algorithms meet intuitive design.",
            font=ctk.CTkFont(size=14, slant="italic"),
            text_color="#E5E7EB",
            justify="center"
        )
        team_desc.pack()
    
    def find_image_path(self, filename):
        """Find image path in various locations"""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "..", "..", "assets", filename),
            os.path.join(os.path.dirname(__file__), "..", "assets", filename),
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets", filename),
            os.path.join("assets", filename)
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None
    
    def create_placeholder_image(self, parent, width, height):
        """Create placeholder image when actual image is not found"""
        placeholder = ctk.CTkFrame(
            parent,
            width=width,
            height=height,
            fg_color="#D1D5DB",
            corner_radius=10
        )
        placeholder.pack(pady=10)
        placeholder.pack_propagate(False)
        
        # Add placeholder text
        placeholder_text = ctk.CTkLabel(
            placeholder,
            text="IMG",
            font=ctk.CTkFont(size=12),
            text_color="#6B7280"
        )
        placeholder_text.pack(expand=True)
    
    def get_page_data(self):
        """Get page data for navigation"""
        return {
            'title': 'About the App',
            'description': 'Learn more about SignHire ATS System'
        }