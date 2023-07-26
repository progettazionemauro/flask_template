import tkinter as tk
from tkinter import ttk, filedialog
import sys
import os

def on_directory_change(*args):
    # Clear the current dropdown menu options
    for dropdown in file_dropdowns:
        dropdown['values'] = []

    # Get the selected directory
    directory = directory_var.get().strip()

    # Check if the directory exists
    if not os.path.exists(directory):
        return

    # Get the list of first-level directories in the selected directory
    dirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

    # Update the dropdown menu options for the directory combobox
    directory_combobox['values'] = dirs

    # Update the dropdown menu options for each file dropdown
    for dropdown in file_dropdowns:
        dropdown['values'] = files_in_directory(directory, dropdown.get().strip())

def files_in_directory(directory, filename_prefix=""):
    # Get the list of files in the directory
    files = os.listdir(directory)
    # Filter files only, excluding directories
    files = [f for f in files if os.path.isfile(os.path.join(directory, f))]
    # Filter files by filename prefix
    if filename_prefix:
        files = [f for f in files if f.startswith(filename_prefix)]
    return files

def add_file_dropdown():
    # Create a new file dropdown and add it to the list of dropdowns
    new_dropdown = ttk.Combobox(root, state="readonly")
    new_dropdown.pack()
    if file_dropdowns:
        new_dropdown['values'] = file_dropdowns[0]['values']  # Set initial values to match the first dropdown
    else:
        # Set default values when the list is empty
        new_dropdown['values'] = []

    # Bind the on_file_change function to the file dropdown widget
    new_dropdown.bind('<<ComboboxSelected>>', on_file_change)

    file_dropdowns.append(new_dropdown)

def on_file_change(*args):
    # Update the displayed filenames in the text widget
    filenames_text.delete(1.0, tk.END)
    filenames = [dropdown.get().strip() for dropdown in file_dropdowns if dropdown.get().strip()]
    filenames_text.insert(tk.END, "\n".join(filenames))

def concatenate_files():
    directory = directory_var.get().strip()
    filenames = filenames_text.get("1.0", tk.END).strip().split("\n")
    filenames = [filename.strip() for filename in filenames if filename.strip()]

    # Check if the directory exists
    if not os.path.exists(directory):
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Error: Directory '{directory}' does not exist.")
        return

    # Get the current directory where the Python script is located
    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

    # Construct the full path for the storage.txt file in the current directory
    output_file_path = os.path.join(current_directory, "storage.txt")

    # Open the file in write mode ('w') to overwrite any existing content
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        for filename in filenames:
            filepath = os.path.join(directory, filename)
            if os.path.exists(filepath) and os.path.isfile(filepath):
                with open(filepath, "r", encoding="latin-1") as input_file:
                    output_file.write(input_file.read())
                output_file.write("\n")
            else:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Error: File '{filename}' does not exist in the specified directory.")
                return

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Files concatenated successfully! Output file: {output_file_path}")


def close_app():
    root.destroy()

root = tk.Tk()
root.title("File Concatenator")

directory_var = tk.StringVar()  # Variable to store the selected directory

directory_label = tk.Label(root, text="Select a directory:")
directory_label.pack()

directory_combobox = ttk.Combobox(root, textvariable=directory_var, state="readonly")
directory_combobox.pack()

def browse_directory():
    selected_directory = filedialog.askdirectory(initialdir="/home/")
    if selected_directory:
        directory_var.set(selected_directory)
        on_directory_change()  # Update the file dropdowns when the directory is selected

browse_button = tk.Button(root, text="Browse", command=browse_directory)
browse_button.pack()

add_button = tk.Button(root, text="Add File Dropdown", command=add_file_dropdown)
add_button.pack()

file_dropdowns = []  # List to store all the file dropdowns

add_file_dropdown()  # Add the initial file dropdown

filenames_label = tk.Label(root, text="Selected filenames:")
filenames_label.pack()

filenames_text = tk.Text(root, height=5)
filenames_text.pack()

concatenate_button = tk.Button(root, text="Concatenate Files", command=concatenate_files)
concatenate_button.pack()

result_label = tk.Label(root, text="Result:")
result_label.pack()

result_text = tk.Text(root, height=5)
result_text.pack()

close_button = tk.Button(root, text="Close", command=close_app)
close_button.pack()

# Bind the on_directory_change function to the directory combobox widget
directory_combobox.bind('<<ComboboxSelected>>', on_directory_change)

root.mainloop()
