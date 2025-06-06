# developer_page.py
import customtkinter as ctk
import os
from PIL import Image

class DeveloperPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill="both", expand=True)
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup developer page UI components"""
        self.configure(fg_color="transparent")
        
        # Main container - full width purple background
        main_container = ctk.CTkFrame(self, fg_color="#18206F", corner_radius=0)
        main_container.pack(fill="both", expand=True)
        
        # Content with padding
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Page title
        self.create_page_title(content_frame)
        
        # Team cards section
        self.create_team_cards(content_frame)
    
    def create_page_title(self, parent):
        """Create page title section"""
        # Main title
        title_label = ctk.CTkLabel(
            parent,
            text="The Team Behind SignHire",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=(0, 15))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            parent,
            text="Meet the developers who brought intelligent recruitment to life",
            font=ctk.CTkFont(size=16, slant="italic"),
            text_color="#E5E7EB"
        )
        subtitle_label.pack(pady=(0, 40))
    
    def create_team_cards(self, parent):
        """Create team member cards section"""
        # Cards container
        cards_container = ctk.CTkFrame(parent, fg_color="transparent")
        cards_container.pack(fill="x", expand=True)
        
        # Configure grid for 3 columns
        for i in range(3):
            cards_container.grid_columnconfigure(i, weight=1, minsize=200)
        
        # Team members data
        team_members = [
            {
                "name": "Newa",
                "nim": "13522001",
                "quote": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                "profile_image": "img3.png"  # Specific image for each member
            },
            {
                "name": "Newa",
                "nim": "13522002",
                "quote": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                "profile_image": "img4.png"  # Different image
            },
            {
                "name": "Newa",
                "nim": "13522003",
                "quote": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                "profile_image": "img5.png"  # Different image
            }
        ]
        
        # Create team member cards
        for i, member in enumerate(team_members):
            self.create_team_card(cards_container, member, i)
    
    def create_team_card(self, parent, member_data, index):
        """Create individual team member card"""
        # Team card with cream background
        card = ctk.CTkFrame(
            parent,
            fg_color="#E8D5B7",  # Cream color
            corner_radius=20,
            width=220,
            height=320
        )
        card.grid(row=0, column=index, padx=15, pady=10, sticky="nsew")
        card.grid_propagate(False)
        
        # Card content container
        card_content = ctk.CTkFrame(card, fg_color="transparent")
        card_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Quote section (italic text at top)
        quote_label = ctk.CTkLabel(
            card_content,
            text=f'"{member_data["quote"]}"',
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color="#2D1B69",
            anchor="w",
            justify="left",
            wraplength=180
        )
        quote_label.pack(anchor="w", fill="x", pady=(0, 15))
        
        # Description section
        description_label = ctk.CTkLabel(
            card_content,
            text=member_data["description"],
            font=ctk.CTkFont(size=11),
            text_color="#2D1B69",
            anchor="w",
            justify="left",
            wraplength=180
        )
        description_label.pack(anchor="w", fill="x", pady=(0, 20))
        
        # Bottom section with profile and name
        bottom_section = ctk.CTkFrame(card_content, fg_color="transparent")
        bottom_section.pack(side="bottom", fill="x", pady=(10, 0))
        
        # Profile picture and info
        profile_section = ctk.CTkFrame(bottom_section, fg_color="transparent")
        profile_section.pack(fill="x")
        
        # Profile picture with specific image
        self.create_profile_picture(profile_section, member_data)
        
        # Name and NIM info
        info_section = ctk.CTkFrame(profile_section, fg_color="transparent")
        info_section.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        # Name
        name_label = ctk.CTkLabel(
            info_section,
            text=member_data["name"],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#2D1B69",
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        # NIM
        nim_label = ctk.CTkLabel(
            info_section,
            text=member_data["nim"],
            font=ctk.CTkFont(size=11),
            text_color="#6B7280",
            anchor="w"
        )
        nim_label.pack(anchor="w", fill="x")
    
    def create_profile_picture(self, parent, member_data):
        """Create profile picture for team member"""
        try:
            # Try to load specific profile image for this member
            image_path = self.find_image_path(member_data["profile_image"])
            
            if image_path and os.path.exists(image_path):
                # Load and resize the specific image
                pil_image = Image.open(image_path)
                pil_image = pil_image.resize((45, 45), Image.Resampling.LANCZOS)
                
                # Convert to CTkImage
                profile_image = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=(45, 45)
                )
                
                # Create profile picture label
                profile_label = ctk.CTkLabel(
                    parent,
                    image=profile_image,
                    text="",
                    width=45,
                    height=45
                )
                profile_label.pack(side="left")
                
                print(f"Profile image loaded for {member_data['name']}: {member_data['profile_image']}")
            else:
                # Try fallback images if specific image not found
                self.try_fallback_images(parent, member_data)
                
        except Exception as e:
            print(f"Error loading profile image for {member_data['name']}: {e}")
            self.try_fallback_images(parent, member_data)
    
    def try_fallback_images(self, parent, member_data):
        """Try fallback images before using placeholder"""
        fallback_images = ["img2.png", "img3.png"]  # Fallback options
        
        for fallback in fallback_images:
            try:
                image_path = self.find_image_path(fallback)
                
                if image_path and os.path.exists(image_path):
                    # Load fallback image
                    pil_image = Image.open(image_path)
                    pil_image = pil_image.resize((45, 45), Image.Resampling.LANCZOS)
                    
                    # Convert to CTkImage
                    profile_image = ctk.CTkImage(
                        light_image=pil_image,
                        dark_image=pil_image,
                        size=(45, 45)
                    )
                    
                    # Create profile picture label
                    profile_label = ctk.CTkLabel(
                        parent,
                        image=profile_image,
                        text="",
                        width=45,
                        height=45
                    )
                    profile_label.pack(side="left")
                    
                    print(f"Fallback image {fallback} used for {member_data['name']}")
                    return  # Exit if fallback successful
                    
            except Exception as e:
                print(f"Fallback image {fallback} failed for {member_data['name']}: {e}")
                continue
        
        # If all fallbacks fail, use placeholder
        self.create_profile_placeholder(parent, member_data["name"])
    
    def create_profile_placeholder(self, parent, member_name):
        """Create profile picture placeholder"""
        # Create circular placeholder
        profile_frame = ctk.CTkFrame(
            parent,
            width=45,
            height=45,
            fg_color="#2D1B69",  # Dark blue color
            corner_radius=22.5  # Half of width/height for circle
        )
        profile_frame.pack(side="left")
        profile_frame.pack_propagate(False)
        
        # Add initials or icon
        initials = member_name[:2].upper() if len(member_name) >= 2 else member_name[0].upper()
        
        profile_text = ctk.CTkLabel(
            profile_frame,
            text=initials,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        )
        profile_text.pack(expand=True)
    
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
    
    def get_page_data(self):
        """Get page data for navigation"""
        return {
            'title': 'Developer',
            'description': 'Meet the team behind SignHire'
        }