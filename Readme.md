# U.S. Driver's License PDF417 Barcode Generator & Decoder

This project allows you to:

- Decode PDF417 barcodes from images (e.g., driver's licenses) using ZXing online decoder.
- Generate PDF417 barcodes from text following the U.S. driver’s license (AAMVA) format.
- Preview generated barcodes and save them locally.

---

## Setup

1. **Clone the repository** (or copy the files to your local machine).

2. **Create a Python virtual environment**:

```bash
python -m venv venv
```

3. **Activate the virtual environment**:

- **Windows (PowerShell)**:
```powershell
venv\Scripts\Activate.ps1
```

- **Windows (CMD)**:
```cmd
venv\Scripts\activate.bat
```

- **Linux/macOS**:
```bash
source venv/bin/activate
```

4. **Install dependencies**:

```bash
pip install -r requirements.txt
```

> `requirements.txt` should include at least:
> ```
> requests
> beautifulsoup4
> pillow
> pdf417gen
> ```

---

## Running the Application

1. **Run the GUI script**:

```bash
python DL_BarCode_Gen.py
```

2. **Using the GUI**:

- **Upload & Decode Image**:  
Click the **"Upload & Decode Image"** button to select an image containing a PDF417 barcode. The decoded text will appear in the text box.

- **Generate PDF417 Barcode**:  
Enter the text (e.g., U.S. driver’s license AAMVA-formatted text) into the text box, then click **"Generate PDF417"**. A preview will appear in the GUI and the barcode will be saved as `output_pdf417.png` in the current folder.

---

## Notes

- The `DCA`, `DCB`, `DCD` fields in the AAMVA format are optional, jurisdiction-specific fields. You can leave them blank for simulations.
- All other fields (DBA, DCS, DCT, DBB, DAG, DAJ, DAQ, etc.) are required for a valid simulated barcode.
- The script requires **Tcl/Tk** for Tkinter. Make sure your Python installation includes Tcl/Tk libraries, or adjust the paths in `DL_BarCode_Gen.py`:

```python
os.environ["TCL_LIBRARY"] = r"C:\Program Files\Python313\tcl\tcl8.6"
os.environ["TK_LIBRARY"] = r"C:\Program Files\Python313\tcl\tk8.6"
```

- All generated barcodes are for **simulation/testing purposes only**. Do **not** use real personal information.

---

## License

This project is for educational and testing purposes only.

