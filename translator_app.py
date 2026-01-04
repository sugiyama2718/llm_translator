import customtkinter as ctk
import threading
import sys
import os

# Ensure the current directory is in python path to import simple_translator
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from simple_translator import translate_ja_to_en
except ImportError:
    # Fallback for testing if file not found locally in typical run
    print("Warning: simple_translator module not found. Mocking for UI test.")
    def translate_ja_to_en(text):
        import time
        for word in text.split():
            time.sleep(0.1)
            yield word + " "

class TranslatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("AI Translator (JP -> EN)")
        self.geometry("600x500")
        
        # Grid Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Input
        self.grid_rowconfigure(1, weight=1) # Output
        self.grid_rowconfigure(2, weight=0) # Controls

        # --- Input Section ---
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew")
        self.input_label = ctk.CTkLabel(self.input_frame, text="Japanese Input:")
        self.input_label.pack(anchor="w", padx=5, pady=2)
        self.input_textbox = ctk.CTkTextbox(self.input_frame, height=150)
        self.input_textbox.pack(expand=True, fill="both", padx=5, pady=5)

        # --- Output Section ---
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")
        self.output_label = ctk.CTkLabel(self.output_frame, text="English Output:")
        self.output_label.pack(anchor="w", padx=5, pady=2)
        self.output_textbox = ctk.CTkTextbox(self.output_frame, height=150)
        self.output_textbox.pack(expand=True, fill="both", padx=5, pady=5)
        self.output_textbox.configure(state="disabled") # Read-only initially

        # --- Controls Section ---
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        self.translate_button = ctk.CTkButton(self.controls_frame, text="Translate", command=self.start_translation)
        self.translate_button.pack(side="left", padx=5, expand=True, fill="x")

        self.copy_button = ctk.CTkButton(self.controls_frame, text="Copy to Clipboard", command=self.copy_output, fg_color="gray", hover_color="darkgray")
        self.copy_button.pack(side="right", padx=5)

    def start_translation(self):
        input_text = self.input_textbox.get("1.0", "end-1c").strip()
        if not input_text:
            return

        # Disable button during translation to prevent spam
        self.translate_button.configure(state="disabled", text="Translating...")
        
        # Clear previous output
        self.output_textbox.configure(state="normal")
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.configure(state="disabled")

        # Start background thread
        threading.Thread(target=self.run_translation, args=(input_text,), daemon=True).start()

    def run_translation(self, text):
        try:
            for chunk in translate_ja_to_en(text):
                # Schedule UI update on main thread
                self.after(0, self.update_output, chunk)
        except Exception as e:
            self.after(0, self.update_output, f"[Error] {str(e)}")
        finally:
            self.after(0, self.reset_button)

    def update_output(self, text):
        self.output_textbox.configure(state="normal")
        self.output_textbox.insert("end", text)
        self.output_textbox.see("end") # Auto-scroll
        self.output_textbox.configure(state="disabled")

    def reset_button(self):
        self.translate_button.configure(state="normal", text="Translate")

    def copy_output(self):
        output_text = self.output_textbox.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(output_text)
        # Visual feedback
        original_text = self.copy_button.cget("text")
        self.copy_button.configure(text="Copied!")
        self.after(2000, lambda: self.copy_button.configure(text=original_text))

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    app = TranslatorApp()
    app.mainloop()
