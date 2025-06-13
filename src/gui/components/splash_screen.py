import customtkinter as ctk
import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, '..', 'assets', 'img1.png')

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent, on_start_callback):
        super().__init__(parent)
        self.on_start_callback = on_start_callback
        
        self.title("SignHire")
        self.geometry("800x600")
        self.configure(fg_color="#18206F") 
        self.resizable(False, False)
        self.center_window()
        
        self.transient(parent) # atas jendela utama
        self.grab_set()
        
        self.setup_ui()
    
    def center_window(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        self.geometry(f"800x600+{x}+{y}")
    
    def setup_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)
        
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=2) 
        main_frame.grid_columnconfigure(1, weight=1)  
        
        left_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(60, 20), pady=40)
        
        center_container = ctk.CTkFrame(left_frame, fg_color="transparent")
        center_container.pack(expand=True, fill="both")
        
        text_frame = ctk.CTkFrame(center_container, fg_color="transparent")
        text_frame.pack(expand=True)
        
        tagline = ctk.CTkLabel(
            text_frame,
            text="Where CVs Turn into Careers.",
            font=("Inter", 24),
            text_color="white"
        )
        tagline.pack(pady=(0, 20), anchor="center")
        
        app_name = ctk.CTkLabel(
            text_frame,
            text="SignHire",
            font=("Inter", 48, "bold"),
            text_color="white"
        )
        app_name.pack(pady=(0, 10), anchor="center")
        
        powered_by = ctk.CTkLabel(
            text_frame,
            text="Powered by SigningOut",
            font=("Inter", 14),
            text_color="#E5E7EB"
        )
        powered_by.pack(pady=(0, 30), anchor="center")
        
        start_button = ctk.CTkButton(
            text_frame,
            text="Start",
            font=("Inter", 18, "bold"),
            fg_color="#F5E2c8",
            text_color="#7C2D12",
            hover_color="#FDE68A",
            height=50,
            width=200,
            corner_radius=25,
            command=self.on_start_click
        )
        start_button.pack(anchor="center")
        
        right_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 40), pady=40)
        
        image_container = ctk.CTkFrame(right_frame, fg_color="transparent")
        image_container.pack(expand=True, fill="both")
        
        self.load_image(image_container)
    
    def load_image(self, parent):
        try:
            img = Image.open(ASSETS_PATH)
            
            max_width, max_height = 250, 250
            img.thumbnail((max_width, max_height), Image.LANCZOS)
            
            ctk_img = ctk.CTkImage(
                light_image=img, 
                dark_image=img, 
                size=img.size  
            )
            label = ctk.CTkLabel(
                parent, 
                image=ctk_img, 
                text=""
            )
            label.pack(expand=True, anchor="center")
            
            label.image = ctk_img
        except Exception as e:
            print(f"Failed to load image: {e}")
            fallback = ctk.CTkLabel(
                parent, 
                text="(Image not found)", 
                text_color="white",
                font=("Inter", 16),
                justify="center"
            )
            fallback.pack(expand=True, anchor="center")
    
    def on_start_click(self):
        self.destroy()
        self.on_start_callback()