import os
import tkinter as tk
from tkinter import filedialog
import re
import json
import logging
import fitz  # PyMuPDF

# Set up logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to convert PDF to text and append to vault.txt using PyMuPDF
def convert_pdf_to_text():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        try:
            logging.info(f"Attempting to extract text from {file_path}")
            # Extract text using PyMuPDF
            document = fitz.open(file_path)
            text = ""
            for page_num in range(len(document)):
                page = document.load_page(page_num)
                text += page.get_text()

            if not text:
                logging.warning(f"No text extracted from {file_path}.")
                return

            # Normalize whitespace and clean up text
            text = re.sub(r'\s+', ' ', text).strip()

            # Split text into chunks by sentences, respecting a maximum chunk size
            sentences = re.split(r'(?<=[.!?]) +', text)
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 1 < 1000:  # +1 for the space
                    current_chunk += (sentence + " ").strip()
                else:
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            if current_chunk:  # Don't forget the last chunk!
                chunks.append(current_chunk)
            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    vault_file.write(chunk.strip() + "\n")
            logging.info(f"PDF content appended to vault.txt with each chunk on a separate line.")
        except Exception as e:
            logging.error(f"Error extracting text from PDF: {e}")

# Function to upload a text file and append to vault.txt
def upload_txtfile():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r', encoding="utf-8") as txt_file:
                text = txt_file.read()

                # Normalize whitespace and clean up text
                text = re.sub(r'\s+', ' ', text).strip()

                # Split text into chunks by sentences, respecting a maximum chunk size
                sentences = re.split(r'(?<=[.!?]) +', text)
                chunks = []
                current_chunk = ""
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) + 1 < 1000:  # +1 for the space
                        current_chunk += (sentence + " ").strip()
                    else:
                        chunks.append(current_chunk)
                        current_chunk = sentence + " "
                if current_chunk:  # Don't forget the last chunk!
                    chunks.append(current_chunk)
                with open("vault.txt", "a", encoding="utf-8") as vault_file:
                    for chunk in chunks:
                        vault_file.write(chunk.strip() + "\n")
                print(f"Text file content appended to vault.txt with each chunk on a separate line.")
        except Exception as e:
            print(f"Error reading text file: {e}")

# Function to upload a JSON file and append to vault.txt
def upload_jsonfile():
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        try:
            with open(file_path, 'r', encoding="utf-8") as json_file:
                data = json.load(json_file)

                # Flatten the JSON data into a single string
                text = json.dumps(data, ensure_ascii=False)

                # Normalize whitespace and clean up text
                text = re.sub(r'\s+', ' ', text).strip()

                # Split text into chunks by sentences, respecting a maximum chunk size
                sentences = re.split(r'(?<=[.!?]) +', text)
                chunks = []
                current_chunk = ""
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) + 1 < 1000:  # +1 for the space
                        current_chunk += (sentence + " ").strip()
                    else:
                        chunks.append(current_chunk)
                        current_chunk = sentence + " "
                if current_chunk:  # Don't forget the last chunk!
                    chunks.append(current_chunk)
                with open("vault.txt", "a", encoding="utf-8") as vault_file:
                    for chunk in chunks:
                        vault_file.write(chunk.strip() + "\n")
                print(f"JSON file content appended to vault.txt with each chunk on a separate line.")
        except Exception as e:
            print(f"Error reading JSON file: {e}")

# Create the main window
root = tk.Tk()
root.title("Upload .pdf, .txt, or .json")

# Create a button to open the file dialog for PDF
pdf_button = tk.Button(root, text="Upload PDF", command=convert_pdf_to_text)
pdf_button.pack(pady=10)

# Create a button to open the file dialog for text file
txt_button = tk.Button(root, text="Upload Text File", command=upload_txtfile)
txt_button.pack(pady=10)

# Create a button to open the file dialog for JSON file
json_button = tk.Button(root, text="Upload JSON File", command=upload_jsonfile)
json_button.pack(pady=10)

# Run the main event loop
root.mainloop()