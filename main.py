import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog

# Function to switch pages
def show_frame(frame):
    frame.tkraise()

# Function to handle file upload in the new user page
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if file_path:
        label_file.config(text=f"File Uploaded: {file_path}")

# Create the main window
root = ttk.Window(themename="superhero")  # Using the dark superhero theme
root.title("MAXXIS Credit Score Manager")
root.geometry("700x600")  # Window size set to 700x600
root.config(padx=20, pady=20)

# Define the frame container
container = ttk.Frame(root)
container.pack(fill="both", expand=True)

# Configure row/column weights so all frames resize with window
for i in range(3):
    container.grid_rowconfigure(i, weight=1)
    container.grid_columnconfigure(i, weight=1)

# Custom fonts set to Segoe UI
custom_font_large = ("Segoe UI", 24, "bold")
custom_font_medium = ("Segoe UI", 14)
button_font = ("Segoe UI", 12)  # Font for buttons

# Define custom button styles for danger, success, and info
style = ttk.Style()

# Match predefined colors with exact ttkbootstrap styles
style.configure('custom-danger.TButton', background='#dc3545', foreground='white', font=('Segoe UI', 12), anchor='center')
style.map('custom-danger.TButton', foreground=[('pressed', 'white'), ('active', 'white')], background=[('pressed', '#bd2130'), ('active', '#dc3545')])

style.configure('custom-success.TButton', background='#28a745', foreground='white', font=('Segoe UI', 12), anchor='center')
style.map('custom-success.TButton', foreground=[('pressed', 'white'), ('active', 'white')], background=[('pressed', '#218838'), ('active', '#28a745')])

style.configure('custom-info.TButton', background='#17a2b8', foreground='white', font=('Segoe UI', 12), anchor='center')
style.map('custom-info.TButton', foreground=[('pressed', 'white'), ('active', 'white')], background=[('pressed', '#117a8b'), ('active', '#17a2b8')])

### LANDING PAGE ###
landing_page = ttk.Frame(container)
landing_page.grid(row=0, column=0, sticky="nsew")

# Center container for the landing page content
landing_page_content = ttk.Frame(landing_page)
landing_page_content.place(relx=0.5, rely=0.5, anchor="center")  # Center the content

# Title
title_label = ttk.Label(landing_page_content, text="MAXXIS Credit Score Manager", font=custom_font_large, bootstyle="primary")
title_label.pack(pady=40)

# Button Container for better organization
btn_frame = ttk.Frame(landing_page_content)
btn_frame.pack(pady=20)

# Custom buttons with new styles
btn_to_main = ttk.Button(btn_frame, text="Enter Application", command=lambda: show_frame(main_page),
                         style="custom-success.TButton", width=20)
btn_to_main.grid(row=0, column=0, padx=10, pady=10)

btn_register = ttk.Button(btn_frame, text="Register New User", command=lambda: show_frame(new_user_page),
                          style="custom-info.TButton", width=20)
btn_register.grid(row=0, column=1, padx=10, pady=10)

### NEW USER PAGE ###
new_user_page = ttk.Frame(container)
new_user_page.grid(row=0, column=0, sticky="nsew")

new_user_title = ttk.Label(new_user_page, text="New User Registration", font=custom_font_large, bootstyle="primary")
new_user_title.pack(pady=20)

# Input field for Customer Name
name_label = ttk.Label(new_user_page, text="Customer Name:", font=custom_font_medium)
name_label.pack(pady=5)
name_entry = ttk.Entry(new_user_page, font=custom_font_medium, width=40)
name_entry.pack(pady=5)

# Input field for Customer ID
id_label = ttk.Label(new_user_page, text="Customer ID:", font=custom_font_medium)
id_label.pack(pady=5)
id_entry = ttk.Entry(new_user_page, font=custom_font_medium, width=40)
id_entry.pack(pady=5)

# File Upload Label and Button
label_file = ttk.Label(new_user_page, text="Upload Financial Data (CSV)", font=custom_font_medium)
label_file.pack(pady=10)

btn_upload = ttk.Button(new_user_page, text="Upload File", command=upload_file, style="custom-info.TButton", width=20)
btn_upload.pack(pady=10)

# Back Button
btn_back_to_landing = ttk.Button(new_user_page, text="Back to Landing Page", command=lambda: show_frame(landing_page),
                                 style="custom-danger.TButton", width=20)
btn_back_to_landing.pack(pady=20)

### MAIN PAGE (Mockup for now) ###
main_page = ttk.Frame(container)
main_page.grid(row=0, column=0, sticky="nsew")

main_page_title = ttk.Label(main_page, text="Main Application Page (Mockup)", font=custom_font_large, bootstyle="primary")
main_page_title.pack(pady=50)

btn_back_to_landing_main = ttk.Button(main_page, text="Back to Landing Page", command=lambda: show_frame(landing_page),
                                      style="custom-danger.TButton", width=20)
btn_back_to_landing_main.pack(pady=20)

# Start with the landing page
show_frame(landing_page)

# Start the main loop
root.mainloop()