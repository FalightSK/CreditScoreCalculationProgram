import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog

import newCustomer

# Function to switch pages
def show_frame(frame):
    frame.tkraise()

# Function to handle financial position file upload
def upload_financial_position():
    global financial_position_path
    financial_position_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv"), ("All files", "*.*")])
    if financial_position_path:
        file_name = os.path.basename(financial_position_path)
        label_financial_position.config(text=f"{file_name}")

# Function to handle income statement file upload
def upload_income_statement():
    global income_statement_path
    income_statement_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv"), ("All files", "*.*")])
    if income_statement_path:
        file_name = os.path.basename(income_statement_path)
        label_income_statement.config(text=f"{file_name}")

# Function to determine rating and color symbol based on credit score
def get_rating_and_color(credit_score):
    if credit_score >= 740:
        return "Very Good", "success",  "Very Good ✅"
    elif credit_score >= 670:
        return "Good", "warning", "Good 👍"
    elif credit_score >= 580:
        return "Fair", "warning", "Fair ⚠️"
    else:
        return "Poor", "danger", "Poor ❌"

# Placeholder function for submitting files and moving to the credit score page
def submit_files():
    customer_name = name_entry.get()
    customer_id = id_entry.get()
    
    if financial_position_path and income_statement_path:
        position = newCustomer.read_financial_file(financial_position_path)
        income = newCustomer.read_financial_file(income_statement_path)
        credit_score = int(newCustomer.FICO_cal(newCustomer.extract_fin_info(position, income)))
        
        # Update the meter and labels on the credit score page
        credit_meter.configure(amountused=credit_score)
        
        # Update the meter color and description based on the score
        credit_meter.configure(bootstyle=get_rating_and_color(credit_score)[1])
        label_credit_confidence.config(text=get_rating_and_color(credit_score)[0], bootstyle=get_rating_and_color(credit_score)[1])
        
        # Update the customer name and type labels
        label_credit_score_name.config(text=f"Customer ID: {customer_name}")
        label_credit_score_id.config(text=f"Customer Type: {customer_id}")
        
        # Switch to the credit score page
        show_frame(credit_score_page)
    else:
        print("Please upload both files.")

# Create the main window
root = ttk.Window(themename="superhero")  # Using the dark superhero theme
root.title("MAXXIS Credit Score Manager")
root.geometry("1250x700")
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
style.configure('custom-success.TButton', background='#28a745', foreground='white', font=('Segoe UI', 12), anchor='center')
style.configure('custom-info.TButton', background='#17a2b8', foreground='white', font=('Segoe UI', 12), anchor='center')

# Placeholder variables for file paths
financial_position_path = ""
income_statement_path = ""

################# LANDING PAGE #################
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
################# ################# #################

################# NEW USER PAGE #################
new_user_page = ttk.Frame(container)
new_user_page.grid(row=0, column=0, sticky="nsew")
new_user_title = ttk.Label(new_user_page, text="New User Registration", font=custom_font_large, bootstyle="primary")
new_user_title.pack(pady=20)
# Input field for Customer ID
name_label = ttk.Label(new_user_page, text="Customer ID:", font=custom_font_medium)
name_label.pack(pady=5)
name_entry = ttk.Entry(new_user_page, font=custom_font_medium, width=40)
name_entry.pack(pady=5)
# Input field for Customer Type
id_label = ttk.Label(new_user_page, text="Customer Type:", font=custom_font_medium)
id_label.pack(pady=5)
id_entry = ttk.Entry(new_user_page, font=custom_font_medium, width=40)
id_entry.pack(pady=5)

# File upload forms placed in the same row
file_frame = ttk.Frame(new_user_page)
file_frame.pack(pady=10)
# File upload for Financial Position (left side)
label_financial_position = ttk.Label(file_frame, text="No file uploaded", font=custom_font_medium)
label_financial_position.grid(row=0, column=0, padx=10, pady=5)
btn_financial_position = ttk.Button(file_frame, text="Upload Financial Position", command=upload_financial_position, style="custom-info.TButton", width=20)
btn_financial_position.grid(row=1, column=0, padx=10, pady=5)
# File upload for Income Statement (right side)
label_income_statement = ttk.Label(file_frame, text="No file uploaded", font=custom_font_medium)
label_income_statement.grid(row=0, column=1, padx=10, pady=5)
btn_income_statement = ttk.Button(file_frame, text="Upload Income Statement", command=upload_income_statement, style="custom-info.TButton", width=20)
btn_income_statement.grid(row=1, column=1, padx=10, pady=5)

# Submit Files Button
btn_submit_files = ttk.Button(new_user_page, text="Submit Files", command=submit_files, style="custom-success.TButton", width=20)
btn_submit_files.pack(pady=20)
# Back Button
btn_back_to_landing = ttk.Button(new_user_page, text="Back to Landing Page", command=lambda: show_frame(landing_page), style="custom-danger.TButton", width=20)
btn_back_to_landing.pack(pady=20)
################# ################# #################

################# MAIN PAGE (Mockup for now) #################
import Script.databaseClient as db

main_page = ttk.Frame(container)
main_page.grid(row=0, column=0, sticky="nsew")

# Title for the main page
main_page_title = ttk.Label(main_page, text="Customer Overview", font=("Segoe UI", 24, "bold"), bootstyle="primary")
main_page_title.pack(pady=20)

# Search and Filter section
search_filter_frame = ttk.Frame(main_page)
search_filter_frame.pack(pady=10, fill="x")

# Search bar
search_label = ttk.Label(search_filter_frame, text="Search:", font=("Segoe UI", 12))
search_label.pack(side="left", padx=5)
search_entry = ttk.Entry(search_filter_frame, font=("Segoe UI", 12), width=30)
search_entry.pack(side="left", padx=5)

# Filter dropdown
filter_label = ttk.Label(search_filter_frame, text="Filter by Type:", font=("Segoe UI", 12))
filter_label.pack(side="left", padx=20)
filter_combobox = ttk.Combobox(search_filter_frame, values=["All", "Tyre Shop"], font=("Segoe UI", 12), width=15)
filter_combobox.current(0)  # Set default to "All"
filter_combobox.pack(side="left", padx=5)

# Table (Treeview) to display customer data
columns = ("customer_id", "type", "credit_budget", "credit_terms", "credit_score", "rating")

customer_table = ttk.Treeview(main_page, columns=columns, show="headings", height=10)
customer_table.pack(pady=20, fill="both", expand=True)

# Define the headings
customer_table.heading("customer_id", text="Customer ID")
customer_table.heading("type", text="Type")
customer_table.heading("credit_budget", text="Credit Budget")
customer_table.heading("credit_terms", text="Credit Terms")
customer_table.heading("credit_score", text="Credit Score")
customer_table.heading("rating", text="Rating")

# Define tags for row colors based on credit score
customer_table.tag_configure("success", foreground="green")
customer_table.tag_configure("warning", foreground="orange")
customer_table.tag_configure("danger", foreground="red")

# Define alternating row background colors
customer_table.tag_configure("evenrow", background="#1E1E2F")
customer_table.tag_configure("oddrow", background="#2A2A40")

# Add data to the table with color-coded emoticons and alternating row colors
row_num = 0
for customer in db.read()["history"].values():
    color, tag, emoticon = get_rating_and_color(customer["credit_score"])
    row_tag = "evenrow" if row_num % 2 == 0 else "oddrow"
    
    customer_table.insert("", "end", values=(
        customer["customer_id"],
        customer["type"],
        customer["credit_budget"],
        customer["credit_terms"],
        customer["credit_score"],
        emoticon  # Insert emoticon in place of plain text rating
    ), tags=(tag, row_tag))
    
    row_num += 1

# Back Button to go to the landing page
btn_back_to_landing_main = ttk.Button(main_page, text="Back to Landing Page", command=lambda: show_frame(landing_page),
                                      style="custom-danger.TButton", width=20)
btn_back_to_landing_main.pack(pady=20)

################# CREDIT SCORE PAGE #################
credit_score_page = ttk.Frame(container)
credit_score_page.grid(row=0, column=0, sticky="nsew")

# Title for Credit Score Page
credit_score_title = ttk.Label(credit_score_page, text="Credit Score", font=custom_font_large, bootstyle="primary")
credit_score_title.pack(pady=20)

# Customer Type and ID Labels
label_credit_score_name = ttk.Label(credit_score_page, text="Customer ID:", font=custom_font_medium)
label_credit_score_name.pack(pady=5)
label_credit_score_id = ttk.Label(credit_score_page, text="Customer Type:", font=custom_font_medium)
label_credit_score_id.pack(pady=5)

# Horizontal container for "Rating" and Confidence Level on the same row
rating_frame = ttk.Frame(credit_score_page)
rating_frame.pack(pady=5)

# Add the white "Rating" label on the left
label_rating_title = ttk.Label(rating_frame, text="Rating:", font=("Segoe UI", 14, "bold"), bootstyle="light")
label_rating_title.pack(side="left", padx=5)

# Confidence level label next to "Rating"
label_credit_confidence = ttk.Label(rating_frame, text="", font=("Segoe UI", 16, "bold"))
label_credit_confidence.pack(side="left", padx=5)

# Credit Score Meter (now placed after the Rating/Confidence row)
credit_meter = ttk.Meter(credit_score_page, bootstyle="success", subtext="Credit Score", interactive=False, amounttotal=850,
                         meterthickness=20, textright='/ 850', arcrange=200, arcoffset=-190)
credit_meter.pack(pady=5)

# Add Return Button to go back to Landing Page
btn_return_to_landing = ttk.Button(credit_score_page, text="Return to Landing Page", command=lambda: show_frame(landing_page),
                                   style="custom-danger.TButton", width=20)
btn_return_to_landing.pack(pady=10)
################# ################# #################

# Start with the landing page
show_frame(landing_page)

# Start the main loop
root.mainloop()