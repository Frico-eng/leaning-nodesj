import cv2
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from .video_feed import VideoFeed
from datetime import datetime

class CubeSolverInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Rubik's Cube Solver AI")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Set modern theme
        self.set_modern_theme()
        
        # Create images directory if it doesn't exist
        self.images_path = r"C:\Users\fredl\OneDrive\Área de Trabalho\projects\python\cubeSolver\images"
        os.makedirs(self.images_path, exist_ok=True)
        
        # Initialize video feed
        self.video_feed = VideoFeed()
        self.video_feed.set_callback(self.update_video_feed)
        
        # Setup GUI
        self.setup_gui()
        
        # Banner for notifications
        self.banner = None
        
        # Start video
        if not self.video_feed.start():
            messagebox.showerror("Error", "Could not initialize camera")
            
    def set_modern_theme(self):
        """Set a modern color theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background='#2c3e50')
        style.configure('TLabel', background='#2c3e50', foreground='white', font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=10)
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), foreground='#3498db')
        style.configure('Status.TLabel', font=('Segoe UI', 9), foreground='#bdc3c7')
        
        # Configure button colors
        style.map('TButton',
                 background=[('active', '#3498db'), ('pressed', '#2980b9')],
                 foreground=[('active', 'white'), ('pressed', 'white')])
        
    def setup_gui(self):
        # Main container
        main_container = ttk.Frame(self.root, padding="20")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=4)  # Video area
        main_container.columnconfigure(1, weight=1)  # Button area
        main_container.rowconfigure(0, weight=1)
        
        # Left side - Video feed
        video_frame = ttk.Frame(main_container, style='TFrame')
        video_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 20))
        
        # Title for video feed
        title_label = ttk.Label(video_frame, text="RUBIK'S CUBE SOLVER", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 15))
        
        # Video container with border
        video_container = ttk.Frame(video_frame, relief='solid', borderwidth=2)
        video_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        video_container.configure(style='TFrame')
        
        # Video feed label
        self.video_label = ttk.Label(video_container, text="Initializing camera...", 
                                   background='#1a1a1a', foreground='white')
        self.video_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status label
        self.status_label = ttk.Label(video_frame, text="Ready to capture", style='Status.TLabel')
        self.status_label.grid(row=2, column=0, pady=5)
        
        # Debug info label (hidden by default)
        self.debug_label = ttk.Label(video_frame, text="", style='Status.TLabel', foreground='#e74c3c')
        self.debug_label.grid(row=3, column=0, pady=2)
        
        # Right side - Buttons panel
        button_panel = ttk.Frame(main_container, style='TFrame', relief='solid', borderwidth=1)
        button_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Panel title
        panel_title = ttk.Label(button_panel, text="CONTROLS", style='Title.TLabel')
        panel_title.grid(row=0, column=0, pady=20)
        
        # Button container
        btn_container = ttk.Frame(button_panel, style='TFrame')
        btn_container.grid(row=1, column=0, padx=20, pady=20)
        
        # Capture button with icon style
        self.capture_btn = ttk.Button(btn_container, text="📷 CAPTURE IMAGE", 
                                    command=self.capture_image, style='TButton')
        self.capture_btn.grid(row=0, column=0, pady=15, sticky='ew')
        
        # Debug button to check permissions
        self.debug_btn = ttk.Button(btn_container, text="🔧 DEBUG INFO", 
                                  command=self.show_debug_info, style='TButton')
        self.debug_btn.grid(row=1, column=0, pady=15, sticky='ew')
        
        # View Images button
        self.view_btn = ttk.Button(btn_container, text="📁 VIEW IMAGES", 
                                 command=self.view_images, style='TButton')
        self.view_btn.grid(row=2, column=0, pady=15, sticky='ew')
        
        # Close button
        self.close_btn = ttk.Button(btn_container, text="❌ EXIT", 
                                  command=self.close_app, style='TButton')
        self.close_btn.grid(row=3, column=0, pady=15, sticky='ew')
        
        # Info text
        info_text = ttk.Label(btn_container, 
                            text="\nInstructions:\n1. Position cube in frame\n2. Click CAPTURE\n3. View saved images",
                            style='Status.TLabel', justify='center')
        info_text.grid(row=4, column=0, pady=20)
        
        # Configure weights for resizing
        video_frame.columnconfigure(0, weight=1)
        video_frame.rowconfigure(1, weight=1)
        video_container.columnconfigure(0, weight=1)
        video_container.rowconfigure(0, weight=1)
        button_panel.columnconfigure(0, weight=1)
        button_panel.rowconfigure(1, weight=1)
        btn_container.columnconfigure(0, weight=1)
        
    def show_banner(self, message, is_success=True):
        """Show a transparent banner message"""
        if self.banner:
            self.banner.destroy()
            
        # Create banner
        self.banner = tk.Toplevel(self.root)
        self.banner.overrideredirect(True)  # Remove window decorations
        self.banner.attributes('-alpha', 0.9)  # Semi-transparent
        
        # Set banner colors based on success/error
        bg_color = '#27ae60' if is_success else '#e74c3c'
        
        banner_label = tk.Label(self.banner, text=message, bg=bg_color, fg='white', 
                               font=('Segoe UI', 12, 'bold'), padx=20, pady=10,
                               relief='raised', bd=1)
        banner_label.pack()
        
        # Position banner at top center of main window
        self.root.update()
        x = self.root.winfo_x() + (self.root.winfo_width() - banner_label.winfo_reqwidth()) // 2
        y = self.root.winfo_y() + 50
        self.banner.geometry(f"+{x}+{y}")
        
        # Auto-hide after 3 seconds
        self.root.after(3000, self.hide_banner)
        
    def hide_banner(self):
        """Hide the banner"""
        if self.banner:
            self.banner.destroy()
            self.banner = None
            
    def show_debug_info(self):
        """Show debug information about the images directory"""
        try:
            debug_info = []
            
            # Check if directory exists
            debug_info.append(f"Directory exists: {os.path.exists(self.images_path)}")
            
            if os.path.exists(self.images_path):
                # Check if directory is writable
                test_file = os.path.join(self.images_path, "test_write.txt")
                try:
                    with open(test_file, 'w') as f:
                        f.write("test")
                    os.remove(test_file)
                    debug_info.append("Directory is writable: Yes")
                except Exception as e:
                    debug_info.append(f"Directory is writable: No - {e}")
                
                # Count existing images
                image_files = [f for f in os.listdir(self.images_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                debug_info.append(f"Existing images: {len(image_files)}")
            
            # Show debug info
            self.debug_label.config(text=" | ".join(debug_info))
            self.show_banner("🔧 Debug info updated", is_success=True)
            
        except Exception as e:
            self.show_banner(f"❌ Debug error: {e}", is_success=False)
        
    def update_video_feed(self, frame):
        # Convert frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Resize frame to fit in the interface
        height, width = frame.shape[:2]
        max_height = 600
        if height > max_height:
            scale = max_height / height
            new_width = int(width * scale)
            frame_rgb = cv2.resize(frame_rgb, (new_width, max_height))
        
        # Convert to ImageTk format
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        
        # Update label
        self.video_label.configure(image=imgtk, text="")
        self.video_label.image = imgtk
        
    def capture_image(self):
        frame = self.video_feed.get_frame()
        if frame is not None:
            try:
                # Generate filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                filename = os.path.join(self.images_path, f"cube_{timestamp}.jpg")
                
                # Debug: Check if frame is valid
                if frame.size == 0:
                    self.show_banner("❌ Empty frame captured", is_success=False)
                    self.status_label.config(text="Empty frame")
                    return
                
                # Try to save with different quality settings
                save_success = False
                for quality in [95, 90, 80]:  # Try different quality levels
                    save_success = cv2.imwrite(filename, frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
                    if save_success:
                        break
                
                if save_success:
                    # Verify the file was actually created
                    if os.path.exists(filename) and os.path.getsize(filename) > 0:
                        # Show success banner
                        short_filename = os.path.basename(filename)
                        self.show_banner(f"✓ Image saved: {short_filename}", is_success=True)
                        self.status_label.config(text=f"✓ Image saved: {short_filename}")
                        self.debug_label.config(text="")  # Clear debug info on success
                    else:
                        self.show_banner("❌ File created but is empty", is_success=False)
                        self.status_label.config(text="File created but is empty")
                else:
                    # Try alternative save method
                    try:
                        from PIL import Image
                        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                        pil_image.save(filename, 'JPEG', quality=90)
                        
                        if os.path.exists(filename) and os.path.getsize(filename) > 0:
                            short_filename = os.path.basename(filename)
                            self.show_banner(f"✓ Image saved (PIL): {short_filename}", is_success=True)
                            self.status_label.config(text=f"✓ Image saved: {short_filename}")
                        else:
                            self.show_banner("❌ PIL save also failed", is_success=False)
                            self.status_label.config(text="PIL save failed")
                    except Exception as pil_error:
                        self.show_banner(f"❌ All save methods failed: {pil_error}", is_success=False)
                        self.status_label.config(text=f"All saves failed: {pil_error}")
                    
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                self.show_banner(error_msg, is_success=False)
                self.status_label.config(text=error_msg)
                self.debug_label.config(text=f"Exception: {type(e).__name__}")
        else:
            self.show_banner("❌ No frame available", is_success=False)
            self.status_label.config(text="No frame available")
            
    def view_images(self):
        try:
            # Check if directory exists and has images
            if not os.path.exists(self.images_path):
                os.makedirs(self.images_path)
                self.show_banner("Created images directory", is_success=True)
                
            # Check if there are any images
            image_files = [f for f in os.listdir(self.images_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if not image_files:
                self.show_banner("No images found in directory", is_success=False)
                return
                
            # Open the images folder
            os.startfile(self.images_path)
            self.show_banner("📁 Opened images folder", is_success=True)
            self.status_label.config(text="Opened images folder")
        except Exception as e:
            self.show_banner(f"❌ Error opening folder: {e}", is_success=False)
            self.status_label.config(text=f"Error: {e}")
            
    def close_app(self):
        self.video_feed.stop()
        self.root.quit()
        self.root.destroy()
        
    def __del__(self):
        self.video_feed.stop()

def main():
    root = tk.Tk()
    app = CubeSolverInterface(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()

if __name__ == "__main__":
    main()