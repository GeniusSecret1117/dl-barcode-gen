import os
import logging

# --- Setup logging ---
logging.basicConfig(
    filename="app_debug.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Force Python to see Tcl/Tk libraries (adjust paths if Tcl/Tk installed elsewhere)
os.environ["TCL_LIBRARY"] = r"C:\Program Files\Python313\tcl\tcl8.6"
os.environ["TK_LIBRARY"] = r"C:\Program Files\Python313\tcl\tk8.6"

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import requests
from bs4 import BeautifulSoup
import pdf417gen
from PIL import Image, ImageTk
import io


# --- ZXing Upload & Decode ---
def decode_image():
    logging.info("decode_image() called")

    # Ask user to select a file
    filepath = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
    if not filepath:
        logging.warning("No file selected for decoding.")
        return

    logging.info(f"Selected file for decoding: {filepath}")

    try:
        with open(filepath, "rb") as f:
            files = {"file": (filepath, f, "image/png")}
            logging.debug("Sending file to ZXing...")
            response = requests.post("https://zxing.org/w/decode", files=files)

        logging.debug("Received response from ZXing")
        soup = BeautifulSoup(response.text, "html.parser")
        pre_tags = soup.find_all("pre")

        raw_text = pre_tags[0].get_text(strip=False) if pre_tags else "Decode failed"
        logging.info(f"Decoded text: {raw_text[:100]}...")  # log only first 100 chars

        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, raw_text)
        messagebox.showinfo("Success", "Decoded text inserted into text box")

    except Exception as e:
        logging.error("Error during decoding", exc_info=True)
        messagebox.showerror("Error", str(e))


# --- Generate PDF417 ---
def generate_barcode():
    logging.info("generate_barcode() called")

    raw_text = text_box.get("1.0", tk.END).strip()
    if not raw_text:
        logging.warning("Attempted to generate barcode with no text.")
        messagebox.showwarning("Warning", "No text to encode!")
        return

    logging.debug(f"Encoding text into PDF417: {raw_text[:100]}...")  # show first 100 chars
    try:
        codes = pdf417gen.encode(raw_text, columns=6, security_level=5)
        image = pdf417gen.render_image(codes, scale=3, ratio=3, padding=5)

        bio = io.BytesIO()
        image.save(bio, format="PNG")
        bio.seek(0)

        pil_image = Image.open(bio)
        tk_image = ImageTk.PhotoImage(pil_image)

        barcode_label.config(image=tk_image)
        barcode_label.image = tk_image

        pil_image.save("output/output_pdf417.png")
        logging.info("PDF417 barcode saved as output_pdf417.png")

        messagebox.showinfo("Saved", "PDF417 barcode saved as output_pdf417.png")

    except Exception as e:
        logging.error("Error during barcode generation", exc_info=True)
        messagebox.showerror("Error", str(e))


# --- GUI Setup ---
logging.info("Starting GUI...")

root = tk.Tk()
root.title("Barcode Decoder & Generator")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

btn_upload = tk.Button(frame, text="Upload & Decode Image", command=decode_image)
btn_upload.grid(row=0, column=0, padx=5, pady=5)

btn_generate = tk.Button(frame, text="Generate PDF417", command=generate_barcode)
btn_generate.grid(row=0, column=1, padx=5, pady=5)

text_box = ScrolledText(root, width=80, height=15)
text_box.pack(padx=10, pady=10)

barcode_label = tk.Label(root)
barcode_label.pack(pady=10)

logging.info("GUI loaded successfully. Entering mainloop...")
root.mainloop()
