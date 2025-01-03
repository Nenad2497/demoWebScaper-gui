import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
from bs4 import BeautifulSoup
import json
import os


root = tk.Tk()
root.title("DataScraper")
root.geometry("850x850")


style = ttk.Style()
style.theme_use("clam")
style.configure(
    "TFrame",
    background="#242424"
)
style.configure(
    "TLabel",
    background="#242424",
    foreground="#fff",
    font=("Helvetica", 12)
)
style.configure(
    "TButton",
    background="green",
    foreground="#fff",
    font=("Helvetica", 10, "bold"),
    borderwidth=1
)
style.map(
    "TButton",
    background=[("active", "#6c757d")],
    relief=[("pressed", "sunken")]
)
style.configure(
    "TEntry",
    padding=6,
    font=("Helvetica", 10)
)


def open_scanner_window():
    scanner_window = tk.Toplevel(root)
    scanner_window.title("Scanner")
    scanner_window.geometry("750x950")
    scanner_label = ttk.Label(scanner_window, text="Scanner Window", font=("Helvetica", 16))
    scanner_label.pack(pady=20)


navbar = tk.Frame(root, bg="white", height=50)
navbar.pack(side="top", fill="x")

scanner_image_path = "scanner.png"  # Replace with your scanner image path

scanner_img = Image.open(scanner_image_path).resize((20, 20))
scanner_icon = ImageTk.PhotoImage(scanner_img)

scanner_button = tk.Button(navbar, image=scanner_icon, bg="white", relief="flat", command=open_scanner_window)
scanner_button.image = scanner_icon
scanner_button.pack(side="left", padx=10, pady=5)

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

label_title = ttk.Label(frame, text="Scrape any website", font=("Helvetica", 16, "bold"))
label_title.pack(pady=10)

label_url = ttk.Label(frame, text="Target URL")
label_url.pack(pady=5)
entry_url = ttk.Entry(frame, width=650)
entry_url.pack(pady=5)

label_name = ttk.Label(frame, text="Target element")
label_name.pack(pady=5)
entry_name = ttk.Entry(frame, width=650)
entry_name.pack(pady=5)

label_email = ttk.Label(frame, text="Target class_")
label_email.pack(pady=5)
entry_email = ttk.Entry(frame, width=650)
entry_email.pack(pady=5)

# Create a Treeview widget to display the data
treeview = ttk.Treeview(frame, columns=("Element",))
treeview.column("Element", width=450)
treeview.pack(pady=10)

def on_button_click():
    url = entry_url.get()
    element = entry_name.get()
    class_ = entry_email.get()
    search_data(url, element, class_)

def search_data(url, element, class_):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    matches = soup.find_all(element, class_=class_)

    for row in treeview.get_children():
        treeview.delete(row)

    result_count = 0

    if matches:
        for match in matches:
            match_text = match.get_text(strip=True)
            treeview.insert("", "end", values=(match_text,))
            result_count += 1
    else:
        treeview.insert("", "end", values=("No elements found",))

    label_result_count.config(text=f"Results Found: {result_count}")
    update_data_count()

def clear_treeview():
    for row in treeview.get_children():
        treeview.delete(row)
    label_result_count.config(text="Results Found: 0")

def save_to_file():
    filename = entry_txt_filename.get()
    file_extension = file_extension_choice.get()

    if not filename.endswith(f".{file_extension}"):
        filename += f".{file_extension}"

    data_to_save = [treeview.item(row)["values"][0] for row in treeview.get_children()]

    if file_extension == "txt":
        with open(filename, "w") as file:
            for data in data_to_save:
                file.write(data + "\n")
    elif file_extension == "json":
        with open(filename, "w") as json_file:
            json.dump(data_to_save, json_file, indent=4)

    messagebox.showinfo("Data Saved", f"Data has been successfully saved to {filename}.")
    update_data_count()

def update_data_count():
    saved_files = [f for f in os.listdir() if f.endswith(('.txt', '.json'))]
    data_count = len(saved_files)
    label_data_count.config(text=f"Data Entries Saved: {data_count}")

def open_saved_data_folder():
    folder_path = os.getcwd()
    filedialog.askdirectory(initialdir=folder_path, title="Open Saved Data Folder")

label_result_count = ttk.Label(frame, text="Results Found: 0", font=("Helvetica", 12, "bold"))
label_result_count.pack(pady=1)

button_clear_results = ttk.Button(frame, text="Clear Results", command=clear_treeview)
button_clear_results.pack(pady=1)

button_submit = ttk.Button(frame, width=30, text="Start The Scraper", command=on_button_click)
button_submit.pack(pady=30)

bottom_frame = ttk.Frame(frame)
bottom_frame.pack(pady=1, fill="x")

label_txt_filename = ttk.Label(bottom_frame, text="Name the file")
label_txt_filename.pack(side="left", padx=5)
entry_txt_filename = ttk.Entry(bottom_frame, width=50)
entry_txt_filename.pack(side="left", padx=5)

file_extension_choice = ttk.Combobox(bottom_frame, values=["txt", "json"], width=20)
file_extension_choice.set("txt")
file_extension_choice.pack(side="left", padx=5)

button_save = ttk.Button(bottom_frame, text="Save Data", command=save_to_file)
button_save.pack(side="left", padx=5)

button_count = ttk.Button(bottom_frame, text="Show Data Count", command=update_data_count)
button_count.pack(side="left", padx=5)

label_data_count = ttk.Label(frame, text="Data Entries Saved: 0", font=("Helvetica", 12, "bold"))
label_data_count.pack(pady=10)

button_open_folder = ttk.Button(frame, text="Open Saved Data Folder", command=open_saved_data_folder)
button_open_folder.pack(pady=10)

root.mainloop()
