import customtkinter as ctk
import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, '..', 'assets', 'img1.png')

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent, on_start_callback):
        super().__init__(parent)
        self.on_start_callback = on_start_callback
        
        # Configure window
        self.title("SignHire")
        self.geometry("800x600")
        self.configure(fg_color="#18206F")  # Purple background
        self.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Make it modal
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
    
    def center_window(self):
        """Center window on screen"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.winfo_screenheight() // 2) - (600 // 2)
        self.geometry(f"800x600+{x}+{y}")
    
    def setup_ui(self):
        """Setup splash screen UI components"""
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)
        
        # Configure grid weights untuk layout yang seimbang
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=2)  # Left section lebih besar
        main_frame.grid_columnconfigure(1, weight=1)  # Right section lebih kecil
        
        # Left section - Text content (center-aligned)
        left_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(60, 20), pady=40)
        
        # Center container untuk text
        center_container = ctk.CTkFrame(left_frame, fg_color="transparent")
        center_container.pack(expand=True, fill="both")
        
        # Text content frame yang akan di-center
        text_frame = ctk.CTkFrame(center_container, fg_color="transparent")
        text_frame.pack(expand=True)
        
        # Tagline
        tagline = ctk.CTkLabel(
            text_frame,
            text="Where CVs Turn into Careers.",
            font=("Inter", 24),
            text_color="white"
        )
        tagline.pack(pady=(0, 20), anchor="center")
        
        # App name
        app_name = ctk.CTkLabel(
            text_frame,
            text="SignHire",
            font=("Inter", 48, "bold"),
            text_color="white"
        )
        app_name.pack(pady=(0, 10), anchor="center")
        
        # Powered by
        powered_by = ctk.CTkLabel(
            text_frame,
            text="Powered by SigningOut",
            font=("Inter", 14),
            text_color="#E5E7EB"
        )
        powered_by.pack(pady=(0, 30), anchor="center")
        
        # Start button
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
        
        # Right section - Image (fixed position)
        right_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 40), pady=40)
        
        # Image container yang di-center di right frame
        image_container = ctk.CTkFrame(right_frame, fg_color="transparent")
        image_container.pack(expand=True, fill="both")
        
        self.load_image(image_container)
    
    def load_image(self, parent):
        """Load and display image in fixed position"""
        try:
            # Load image
            img = Image.open(ASSETS_PATH)
            
            # Resize dengan mempertahankan aspect ratio
            # Tentukan ukuran maksimal
            max_width, max_height = 250, 250
            img.thumbnail((max_width, max_height), Image.LANCZOS)
            
            # Create CTkImage
            ctk_img = ctk.CTkImage(
                light_image=img, 
                dark_image=img, 
                size=img.size  # Gunakan ukuran asli setelah resize
            )
            
            # Create label and center it
            label = ctk.CTkLabel(
                parent, 
                image=ctk_img, 
                text=""
            )
            label.pack(expand=True, anchor="center")
            
            # Keep reference to prevent garbage collection
            label.image = ctk_img
            
        except Exception as e:
            print(f"Failed to load image: {e}")
            # Fallback jika gambar tidak bisa dimuat
            fallback = ctk.CTkLabel(
                parent, 
                text="🖼️\n(Image not found)", 
                text_color="white",
                font=("Inter", 16),
                justify="center"
            )
            fallback.pack(expand=True, anchor="center")
    
    def on_start_click(self):
        """Handle start button click"""
        self.destroy()
        self.on_start_callback()