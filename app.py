# The UI elements were mostly generated using chatGPT. The program logic integrations were all done by me though

import customtkinter
import os

from tkinter import filedialog
from PIL import Image
from image_translator import translate_image

app = customtkinter.CTk()
app.title("Not Google Lens")
app.geometry("960x540")  # Room for a bigger image

# Label to display the image
my_label = customtkinter.CTkLabel(app, text="")
my_label.grid(row=1, column=0, padx=20, pady=10)

# Store image, path, and filename
image_reference = {"img": None}
selected_file = {"path": None, "name": None}

# Maximum size for displayed image (you can tweak this)
MAX_WIDTH = 1920
MAX_HEIGHT = 800

def open_file():
    filename = filedialog.askopenfilename(
        initialdir="/",
        title="Select a File",
        filetypes=(("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*"))
    )
    if filename:
        print("Selected file:", filename)
        selected_file["path"] = filename
        selected_file["name"] = os.path.basename(filename)

        try:
            # Open and resize image
            img = Image.open(filename)
            img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.LANCZOS)

            # Create CTkImage
            ctk_img = customtkinter.CTkImage(light_image=img, dark_image=img, size=img.size)

            # Prevent garbage collection
            image_reference["img"] = ctk_img

            # Display the image
            my_label.configure(image=ctk_img)

        except Exception as e:
            print("Error loading image:", e)

def translate_selected_image():
    if selected_file["path"]:
        print("Translating image...")
        translated_image_path = translate_image(selected_file["path"], selected_file["name"])

        if translated_image_path:
            try:
                img = Image.open(translated_image_path)
                img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.LANCZOS)

                ctk_img = customtkinter.CTkImage(light_image=img, dark_image=img, size=img.size)
                image_reference["img"] = ctk_img  # Prevent garbage collection
                my_label.configure(image=ctk_img)
                print("Displayed translated image:", translated_image_path)

            except Exception as e:
                print("Failed to load translated image:", e)
        else:
            print("No translated image returned.")
    else:
        print("No file selected!")

# File selection button
button = customtkinter.CTkButton(app, text="Open File", command=open_file)
button.grid(row=0, column=0, padx=20, pady=20)

button_process = customtkinter.CTkButton(app, text="Translate Image", command=translate_selected_image)
button_process.grid(row=0, column=1, padx=20, pady=20)

app.mainloop()
