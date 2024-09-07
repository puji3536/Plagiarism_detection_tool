import tkinter as tk
from tkinter import filedialog
from difflib import SequenceMatcher
import PyPDF2
import docx

def load_file_or_display_contents(entry, text_widget, file_type):
    file_path = entry.get()
    if not file_path:
        if file_type == 'txt':
            file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        elif file_type == 'pdf':
            file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        elif file_type == 'docx':
            file_path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(tk.END, file_path)
        if file_type == 'txt':
            with open(file_path, 'r') as file:
                text = file.read()
                text_widget.delete(1.0, tk.END)
                text_widget.insert(tk.END, text)
        elif file_type == 'pdf':
            pdfFile = open(file_path, 'rb')
            pdfReader = PyPDF2.PdfReader(pdfFile)
            numPages = len(pdfReader.pages)
            text = ''
            for pageNum in range(numPages):
                pageObj = pdfReader.pages[pageNum]
                text += pageObj.extract_text()
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, text)
            pdfFile.close()
        elif file_type == 'docx':
            doc = docx.Document(file_path)
            text = ''
            for para in doc.paragraphs:
                text += para.text
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, text)

def compare_text(text1, text2):
    d = SequenceMatcher(None, text1, text2)
    similarity_ratio = d.ratio()
    similarity_percentage = int(similarity_ratio * 100)
    diff = list(d.get_opcodes())
    return similarity_percentage, diff

def show_similarity():
    text1 = text_textbox1.get(1.0, tk.END)
    text2 = text_textbox2.get(1.0, tk.END)
    
    if not text1.strip() and not text2.strip():
        text_textbox_diff.delete(1.0, tk.END)
        text_textbox_diff.insert(tk.END, "Warning: Please upload both files to compare.")
    elif not text1.strip():
        text_textbox_diff.delete(1.0, tk.END)
        text_textbox_diff.insert(tk.END, "Warning: Please upload the first file.")
    elif not text2.strip():
        text_textbox_diff.delete(1.0, tk.END)
        text_textbox_diff.insert(tk.END, "Warning: Please upload the second file.")
    else:
        result = compare_text(text1, text2)
        similarity_percentage, diff = result
        text_textbox_diff.delete(1.0, tk.END)
        text_textbox_diff.insert(tk.END, f"Similarity: {similarity_percentage}%")
        text_textbox1.tag_remove("same", "1.0", tk.END)
        text_textbox2.tag_remove("same", "1.0", tk.END)
        for tag in diff:
            if tag[0] == 'equal':
                start1 = f"1.{tag[1]}"
                end1 = f"1.{tag[2]}"
                start2 = f"1.{tag[3]}"
                end2 = f"1.{tag[4]}"
                text_textbox1.tag_add("same", start1, end1)
                text_textbox2.tag_add("same", start2, end2)
        text_textbox1.tag_configure("same", foreground="red", background="lightyellow")
        text_textbox2.tag_configure("same", foreground="red", background="lightyellow")

def clear_text():
    text_textbox1.delete(1.0, tk.END)
    text_textbox2.delete(1.0, tk.END)
    text_textbox_diff.delete(1.0, tk.END)
    file_entry1.delete(0, tk.END)
    file_entry2.delete(0, tk.END)

root = tk.Tk()
root.title("Text Comparison Tool")

frame = tk.Frame(root,bg='Blue')
frame.pack(padx=10, pady=10)

text_label1 = tk.Label(frame, text="Text 1:")
text_label1.grid(row=0, column=0, padx=5, pady=5)

text_textbox1 = tk.Text(frame, wrap=tk.WORD, width=80, height=30)
text_textbox1.grid(row=0, column=1, padx=5, pady=5)

text_label2 = tk.Label(frame, text="Text 2:")
text_label2.grid(row=0, column=2, padx=5, pady=5)

text_textbox2 = tk.Text(frame, wrap=tk.WORD, width=80, height=30)
text_textbox2.grid(row=0, column=3, padx=5, pady=5)

file_path1 = tk.Label(frame, text="Path 1:")
file_path1.grid(row=1, column=2, padx=(0, 5), pady=5, sticky='e')

file_entry1 = tk.Entry(frame, width=50)
file_entry1.grid(row=1, column=3, columnspan=2, padx=5, pady=5, sticky='w')

load_frame1 = tk.Frame(frame)
load_frame1.grid(row=1, column=0, columnspan=3, pady=2)

load_button1 = tk.Button(load_frame1, text="Load File 1", command=lambda: load_file_or_display_contents(file_entry1, text_textbox1, 'txt'))
load_button1.pack(side=tk.LEFT, padx=2)

load_button1_pdf = tk.Button(load_frame1, text="Load PDF File 1", command=lambda: load_file_or_display_contents(file_entry1, text_textbox1, 'pdf'))
load_button1_pdf.pack(side=tk.LEFT, padx=2)

load_button1_docx = tk.Button(load_frame1, text="Load Word File 1", command=lambda: load_file_or_display_contents(file_entry1, text_textbox1, 'docx'))
load_button1_docx.pack(side=tk.LEFT, padx=2)

file_path2 = tk.Label(frame, text="Path 2:")
file_path2.grid(row=2, column=2, padx=(0, 5), pady=5, sticky='e')

file_entry2 = tk.Entry(frame, width=50)
file_entry2.grid(row=2, column=3, columnspan=2, padx=5, pady=5, sticky='w')

load_frame2 = tk.Frame(frame)
load_frame2.grid(row=3, column=0, columnspan=3, pady=2)

load_button2 = tk.Button(load_frame2, text="Load File 2", command=lambda: load_file_or_display_contents(file_entry2, text_textbox2, 'txt'))
load_button2.pack(side=tk.LEFT, padx=2)

load_button2_pdf = tk.Button(load_frame2, text="Load PDF File 2", command=lambda: load_file_or_display_contents(file_entry2, text_textbox2, 'pdf'))
load_button2_pdf.pack(side=tk.LEFT, padx=2)

load_button2_docx = tk.Button(load_frame2, text="Load Word File 2", command=lambda: load_file_or_display_contents(file_entry2, text_textbox2, 'docx'))
load_button2_docx.pack(side=tk.LEFT, padx=2)

compare_button = tk.Button(frame, text="Compare", command=show_similarity)
compare_button.grid(row=6, column=1, padx=5, pady=2)

text_textbox_diff = tk.Text(frame, wrap=tk.WORD, width=80, height=4)
text_textbox_diff.grid(row=6, column=1, columnspan=3, padx=5, pady=2)

clear_button = tk.Button(frame, text="Clear", command=clear_text)
clear_button.grid(row=5, column=1, padx=5, pady=5)

root.mainloop()