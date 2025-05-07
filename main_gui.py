import tkinter as tk
from tkinter import filedialog
from lsb_handler import encode_lsb, decode_lsb
from jpeg_handler import encode_jpeg_dct, decode_jpeg_dct
from bpcs_handler import encode_bpcs, decode_bpcs
from masking_filtering_handler import encode_masking_filtering, decode_masking_filtering
from heuristic_handler import encode_heuristic, decode_heuristic

def embed_message():
    file_path = filedialog.askopenfilename(title="Dosya Seçin", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    message = message_entry.get()
    method = method_var.get()
    
    if method == "LSB":
        output_path = "output/lsb_encoded.png"
        success = encode_lsb(file_path, message, output_path)
    elif method == "JPEG":
        output_path = "output/jpeg_encoded.jpg"
        success = encode_jpeg_dct(file_path, message, output_path)
    elif method == "BPCS":
        output_path = "output/bpcs_encoded.png"
        success = encode_bpcs(file_path, message, output_path)
    elif method == "Masking and Filtering":
        output_path = "output/masking_filtering_encoded.png"
        success = encode_masking_filtering(file_path, message, output_path)
    elif method == "Heuristic":
        output_path = "output/heuristic_encoded.png"
        success = encode_heuristic(file_path, message, output_path)
    
    if success:
        result_label.config(text=f"Mesaj başarıyla gömüldü! Dosya kaydedildi: {output_path}")
    else:
        result_label.config(text="Mesaj gömme işlemi başarısız oldu.")

def extract_message():
    file_path = filedialog.askopenfilename(title="Şifreli Resmi Seçin", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    method = method_var.get()

    if method == "LSB":
        message = decode_lsb(file_path)
    elif method == "JPEG":
        message = decode_jpeg_dct(file_path)
    elif method == "BPCS":
        message = decode_bpcs(file_path)
    elif method == "Masking and Filtering":
        message = decode_masking_filtering(file_path)
    elif method == "Heuristic":
        message = decode_heuristic(file_path)

    message_label.config(text=f"Gizli Mesaj: {message}")

# Tkinter arayüzü
root = tk.Tk()
root.title("Steganografi Uygulaması")

method_var = tk.StringVar()
method_var.set("LSB")  # Default olarak LSB

method_menu = tk.OptionMenu(root, method_var, "LSB", "JPEG", "BPCS", "Masking and Filtering", "Heuristic")
method_menu.pack()

message_label = tk.Label(root, text="Gizlenecek mesajı girin:")
message_label.pack()

message_entry = tk.Entry(root, width=50)
message_entry.pack()

embed_button = tk.Button(root, text="Mesaj Göm", command=embed_message)
embed_button.pack()

extract_button = tk.Button(root, text="Mesajı Çöz", command=extract_message)
extract_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()