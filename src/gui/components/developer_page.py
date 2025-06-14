# developer_page.py
import customtkinter as ctk
import os
from PIL import Image, ImageDraw, ImageOps

class DeveloperPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill="both", expand=True)
        self.setup_ui()
        
    def setup_ui(self):
        self.configure(fg_color="transparent")
        
        main_container = ctk.CTkFrame(self, fg_color="#18206F", corner_radius=0)
        main_container.pack(fill="both", expand=True)
        
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=40, pady=40)
        self.create_page_title(content_frame)
        
        self.create_team_cards(content_frame)
    
    def create_page_title(self, parent):
        title_label = ctk.CTkLabel(
            parent,
            text="The Team Behind SignHire",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=(0, 15))
        
        subtitle_label = ctk.CTkLabel(
            parent,
            text="Meet the developers who brought intelligent recruitment to life",
            font=ctk.CTkFont(size=16, slant="italic"),
            text_color="#E5E7EB"
        )
        subtitle_label.pack(pady=(0, 40))
    
    def create_team_cards(self, parent):
        cards_container = ctk.CTkFrame(parent, fg_color="transparent")
        cards_container.pack(fill="both", expand=True, padx=15)
        
        for i in range(3):
            cards_container.grid_columnconfigure(i, weight=1, minsize=300)
        
        team_members = [
            {
                "name": "Newa",
                "nim": "13523043",
                "quote": "I maybe not yours and you're not mine.\nBut I'll be there for you when you need me \n - It's Only Me, Kaleb J",
                "description": "Terima kasih kepada stima yang sudah mewarnai\nsemester paling chaos so far dengan 3 tucil dan 3 tubes.\nSangat berkesan.\n\nTerima kasih juga kepada tim SigningOut yang sudah\nmenjadi tim penutup stima yang sangat fun.\n\nps: Heleni jangan lupa bayar denda wkwk",
                "profile_image": "newa.jpg" 
            },
            {
                "name": "Nayla",
                "nim": "13523079",
                "quote": "Pasti kau temukan aku di garis terdepan \nBertepuk dengan sebelah tangan \n - Garis Terdepan, Fiersa Bestari",
                "description": "Terimakasi stima atas segala experiencenya. \nApresiasi besar juga buat temen temen signingOut, \nlovyu ol",
                "profile_image": "nayla.jpg"  
            },
            {
                "name": "Heleni",
                "nim": "13523107",
                "quote": "Siapa yang tau \nSiapa yang mau\nKau di sana\nAku diseberangmu\n - Mangu, Fourtwnty",
                "description": "Makasih buat semuanya, segala hal yang telah dibolehkan terjadi dalam hidupku dan memberi makna mendalam, yaitu stima dan teman-teman SigningOut.\n\nSelamat menyelesaikan semester 4!",
                "profile_image": "heleni.jpeg" 
            }
        ]
        
        for i, member in enumerate(team_members):
            self.create_team_card(cards_container, member, i)
    
    def create_team_card(self, parent, member_data, index):
        card = ctk.CTkFrame(
            parent,
            fg_color="#E8D5B7", 
            corner_radius=20,
            width=300, 
            height=350  
        )
        card.grid(row=0, column=index, padx=12, pady=10, sticky="nsew")
        card.grid_propagate(False)
        
        card_content = ctk.CTkFrame(card, fg_color="transparent")
        card_content.pack(fill="both", expand=True, padx=18, pady=18)
        
        quote_textbox = ctk.CTkTextbox(
            card_content,
            height=100, 
            font=ctk.CTkFont(size=12, slant="italic"),  
            fg_color="transparent",
            text_color="#2D1B69",
            wrap="word",
            border_width=0,
            corner_radius=0
        )
        quote_textbox.pack(anchor="w", fill="x", pady=(0, 12))  
        quote_textbox.insert("1.0", f'"{member_data["quote"]}"')
        quote_textbox.configure(state="disabled")  
        
        description_textbox = ctk.CTkTextbox(
            card_content,
            height=150,  
            font=ctk.CTkFont(size=10), 
            fg_color="transparent",
            text_color="#2D1B69",
            wrap="word",
            border_width=0,
            corner_radius=0
        )
        description_textbox.pack(anchor="w", fill="x", pady=(0, 15)) 
        description_textbox.insert("1.0", member_data["description"])
        description_textbox.configure(state="disabled")  
        
        bottom_section = ctk.CTkFrame(card_content, fg_color="transparent")
        bottom_section.pack(side="bottom", fill="x", pady=(10, 0))  
        
        profile_section = ctk.CTkFrame(bottom_section, fg_color="transparent")
        profile_section.pack(fill="x")
        
        self.create_profile_picture(profile_section, member_data)
        
        info_section = ctk.CTkFrame(profile_section, fg_color="transparent")
        info_section.pack(side="left", fill="both", expand=True, padx=(12, 0))  
        
        name_label = ctk.CTkLabel(
            info_section,
            text=member_data["name"],
            font=ctk.CTkFont(size=15, weight="bold"),  
            text_color="#2D1B69",
            anchor="w"
        )
        name_label.pack(anchor="w", fill="x")
        
        nim_label = ctk.CTkLabel(
            info_section,
            text=member_data["nim"],
            font=ctk.CTkFont(size=11),  
            text_color="#6B7280",
            anchor="w"
        )
        nim_label.pack(anchor="w", fill="x")
    
    def create_profile_picture(self, parent, member_data):
        try:
            image_path = self.find_image_path(member_data["profile_image"])
            
            if image_path and os.path.exists(image_path):
                pil_image = Image.open(image_path)
                pil_image = pil_image.resize((120, 120), Image.Resampling.LANCZOS)
                
                profile_image = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=(50, 50) 
                )
                
                profile_label = ctk.CTkLabel(
                    parent,
                    image=profile_image,
                    text="",
                    width=50,  
                    height=50  
                )
                profile_label.pack(side="left")
                
                print(f"Profile image loaded for {member_data['name']}: {member_data['profile_image']}")
            else:
                self.try_fallback_images(parent, member_data)
                
        except Exception as e:
            print(f"Error loading profile image for {member_data['name']}: {e}")
            self.try_fallback_images(parent, member_data)
    
    def try_fallback_images(self, parent, member_data):
        fallback_images = ["img2.png", "img3.png"] 
        
        for fallback in fallback_images:
            try:
                image_path = self.find_image_path(fallback)
                
                if image_path and os.path.exists(image_path):
                    pil_image = Image.open(image_path)
                    pil_image = pil_image.resize((50, 50), Image.Resampling.LANCZOS)
                    
                    profile_image = ctk.CTkImage(
                        light_image=pil_image,
                        dark_image=pil_image,
                        size=(50, 50)
                    )
                    
                    profile_label = ctk.CTkLabel(
                        parent,
                        image=profile_image,
                        text="",
                        width=50,  
                        height=50  
                    )
                    profile_label.pack(side="left")
                    
                    print(f"Fallback image {fallback} used for {member_data['name']}")
                    return  
                    
            except Exception as e:
                print(f"Fallback image {fallback} failed for {member_data['name']}: {e}")
                continue
        
        self.create_profile_placeholder(parent, member_data["name"])
    
    def create_profile_placeholder(self, parent, member_name):
        profile_frame = ctk.CTkFrame(
            parent,
            width=50,  
            height=50,  
            fg_color="#2D1B69",  
            corner_radius=25
        )
        profile_frame.pack(side="left")
        profile_frame.pack_propagate(False)
        
        initials = member_name[:2].upper() if len(member_name) >= 2 else member_name[0].upper()
        
        profile_text = ctk.CTkLabel(
            profile_frame,
            text=initials,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        )
        profile_text.pack(expand=True)
    
    def find_image_path(self, filename):
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
        return {
            'title': 'Developer',
            'description': 'Meet the team behind SignHire'
        }