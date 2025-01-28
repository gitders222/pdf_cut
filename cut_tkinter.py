import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter

class PDFCutterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Cutting App")
        self.root.geometry("400x300")

        # Variables
        self.pdf_path = tk.StringVar()
        self.page_range = tk.StringVar()

        # GUI Elements
        tk.Label(root, text="PDF Cutting App", font=("Arial", 16)).pack(pady=10)

        # Select PDF
        tk.Button(root, text="Select PDF", command=self.select_pdf).pack(pady=5)
        tk.Entry(root, textvariable=self.pdf_path, width=50, state="readonly").pack(pady=5)

        # Page Range
        tk.Label(root, text="Page Range (e.g., 1-3,5):").pack(pady=5)
        tk.Entry(root, textvariable=self.page_range, width=30).pack(pady=5)

        # Save Button
        tk.Button(root, text="Save Cut PDF", command=self.save_cut_pdf).pack(pady=20)

    def select_pdf(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")]
        )
        if filepath:
            self.pdf_path.set(filepath)

    def save_cut_pdf(self):
        if not self.pdf_path.get():
            messagebox.showerror("Error", "Please select a PDF file.")
            return

        if not self.page_range.get():
            messagebox.showerror("Error", "Please enter a page range.")
            return

        try:
            # Parse the page range
            ranges = self.parse_page_range(self.page_range.get())

            # Read the PDF
            reader = PdfReader(self.pdf_path.get())
            writer = PdfWriter()

            for page in ranges:
                if 0 <= page < len(reader.pages):
                    writer.add_page(reader.pages[page])
                else:
                    raise ValueError(f"Page {page + 1} is out of range.")

            # Save the cut PDF
            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")]
            )
            if save_path:
                with open(save_path, "wb") as output:
                    writer.write(output)
                messagebox.showinfo("Success", "Cut PDF saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def parse_page_range(self, range_str):
        pages = set()
        for part in range_str.split(","):
            if "-" in part:
                start, end = map(int, part.split("-"))
                pages.update(range(start - 1, end))
            else:
                pages.add(int(part) - 1)
        return sorted(pages)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFCutterApp(root)
    root.mainloop()
