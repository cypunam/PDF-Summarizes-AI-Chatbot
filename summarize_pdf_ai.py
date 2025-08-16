import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, font
import pdfplumber
import google.generativeai as genai
import os

# Configure Gemini API
genai.configure(api_key="AIzaSyBr4itiIoPsDvuA3qjSy0onoqq5urmz044")  # Replace with your API key
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to extract text from PDF
def extract_text(pdf_path): 
    text = ""
    with pdfplumber.open(pdf_path) as pdf: 
        for page in pdf.pages: 
            page_text = page.extract_text() 
            if page_text: 
                text += page_text 
    return text

# Function to summarize PDF
def summarize_pdf(text):
    response = model.generate_content([
        f"You are a PDF summarizer. Summarize the following content:\n\n{text}"
    ])
    return response.text

# Function to answer question
def question_answer(text, question):
    response = model.generate_content([
        f"Please answer the following question based on the text: {text}\n\nQuestion: {question}"
    ])
    return response.text

# Browse PDF file
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    pdf_path_var.set(file_path)

# Process PDF and question
def process_pdf():
    pdf_path = pdf_path_var.get()
    question = question_entry.get()

    if not pdf_path:
        messagebox.showerror("Error", "Please select a PDF file first!")
        return

    if not os.path.exists(pdf_path):
        messagebox.showerror("Error", "PDF file not found!")
        return

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Processing...\n")
    root.update()

    try:
        text = extract_text(pdf_path)
        if not text.strip():
            messagebox.showerror("Error", "No text found in PDF.")
            return

        if question.strip():
            result = question_answer(text, question)
        else:
            result = summarize_pdf(text)

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- UI DESIGN ---------------- #
root = tk.Tk()
root.title("AI PDF Summarizer & QnA")
root.geometry("650x580")
root.config(bg="#2C3E50")  # Dark blue background
root.resizable(False, False)
root.attributes('-fullscreen', True)

# Fonts
title_font = font.Font(family="Helvetica", size=18, weight="bold")
label_font = font.Font(family="Helvetica", size=12)
btn_font = font.Font(family="Helvetica", size=10, weight="bold")

# Variables
pdf_path_var = tk.StringVar()

# Title
title_label = tk.Label(root, text="📄 AI PDF Summarizer & QnA", bg="#2C3E50", fg="white", font=title_font)
title_label.pack(pady=15)

# PDF File input
tk.Label(root, text="Select PDF File:", bg="#2C3E50", fg="white", font=label_font).pack(pady=5)
file_frame = tk.Frame(root, bg="#2C3E50")
file_frame.pack()
tk.Entry(file_frame, textvariable=pdf_path_var, width=40, font=label_font).pack(side=tk.LEFT, padx=5)
tk.Button(file_frame, text="Browse", command=browse_file, bg="#1ABC9C", fg="white", font=btn_font).pack(side=tk.LEFT, padx=5)

# Question input
tk.Label(root, text="Question (Leave empty for summary):", bg="#2C3E50", fg="white", font=label_font).pack(pady=10)
question_entry = tk.Entry(root, width=50, font=label_font)
question_entry.pack(pady=5)

# Submit button
submit_btn = tk.Button(root, text="Submit", command=process_pdf, bg="#E67E22", fg="white", font=btn_font, width=15)
submit_btn.pack(pady=10)

# Result section
tk.Label(root, text="Result:", bg="#2C3E50", fg="white", font=label_font).pack(pady=5)
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15, font=("Courier New", 10))
result_text.pack(pady=5)

# Footer
footer = tk.Label(root, text="© 2025 Copyright by PUNAM KUMAR", 
                  bg="#2C3E50", fg="lightgray", font=("Helvetica", 9))
footer.pack(side=tk.BOTTOM, pady=10)

# Run
root.mainloop()
