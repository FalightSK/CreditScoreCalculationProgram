import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Function to calculate and display x^2 + y
def calculate():
    try:
        x = float(entry_x.get())
        y = float(entry_y.get())
        result = x**2 + y
        result_textbox.delete("1.0", END)
        result_textbox.insert(END, f"Result: {result}")
    except ValueError:
        result_textbox.delete("1.0", END)
        result_textbox.insert(END, "Please enter valid numbers")

# Create the main window
root = ttk.Window(themename="darkly")  # You can change the theme as needed
root.title("Calculate x^2 + y")
root.geometry("400x300")

# Set a custom font (Poppins or Gilroy or fallback)
custom_font = ("Poppins", 12)  # You can replace 'Poppins' with 'Gilroy' if available

# Create a frame to hold all the widgets in the center
main_frame = ttk.Frame(root)
main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Create labels and entry widgets aligned to the center
label_title = ttk.Label(main_frame, text="Calculate x^2 + y", font=("Poppins", 16), bootstyle=PRIMARY)
label_title.pack(pady=10)

label_x = ttk.Label(main_frame, text="Enter x:", font=custom_font)
label_x.pack(pady=5)

entry_x = ttk.Entry(main_frame, font=custom_font, width=20)
entry_x.pack(pady=5)

label_y = ttk.Label(main_frame, text="Enter y:", font=custom_font)
label_y.pack(pady=5)

entry_y = ttk.Entry(main_frame, font=custom_font, width=20)
entry_y.pack(pady=5)

# Create a button to trigger the calculation
calc_button = ttk.Button(main_frame, text="Calculate", command=calculate, bootstyle=SUCCESS)
calc_button.pack(pady=20)

# Create a text box to display the result
result_textbox = ttk.Text(main_frame, height=3, width=30, font=custom_font)
result_textbox.pack(pady=10)

# Start the main event loop
root.mainloop()