import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from lsb_handler import encode_lsb, decode_lsb
import os


class StegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganografi Uygulaması")
        self.root.geometry("500x400")

        # Dosya seçimi
        self.file_label = tk.Label(root, text="Dosya Seç:")
        self.file_label.pack(pady=5)

        self.select_button = tk.Button(root, text="Dosya Seç", command=self.select_file)
        self.select_button.pack()

        self.filename_var = tk.StringVar()
        self.filename_entry = tk.Entry(root, textvariable=self.filename_var, width=50, state='readonly')
        self.filename_entry.pack(pady=5)

        # Mesaj girme
        self.message_label = tk.Label(root, text="Gizlenecek / Çözülecek Mesaj:")
        self.message_label.pack(pady=5)

        self.message_text = tk.Text(root, height=5, width=50)
        self.message_text.pack()

        # Algoritma seçimi
        self.algorithm_label = tk.Label(root, text="Algoritma Seç:")
        self.algorithm_label.pack(pady=5)

        self.algorithm_var = tk.StringVar()
        self.algorithm_menu = ttk.Combobox(root, textvariable=self.algorithm_var)
        self.algorithm_menu['values'] = ["LSB", "JPEG (DCT)", "BPCS", "Maskeleme", "Sezgisel"]
        self.algorithm_menu.pack()

        # İşlem butonları
        self.embed_button = tk.Button(root, text="Mesajı Gizle", command=self.embed_message)
        self.embed_button.pack(pady=10)

        self.extract_button = tk.Button(root, text="Mesajı Çöz", command=self.extract_message)
        self.extract_button.pack(pady=5)

        # Durum mesajı
        self.status_label = tk.Label(root, text="", fg="green")
        self.status_label.pack(pady=10)

    def select_file(self):
        filepath = filedialog.askopenfilename()
        self.filename_var.set(filepath)

    def embed_message(self):
        file_path = self.filename_var.get()
        message = self.message_text.get("1.0", tk.END).strip()
        algorithm = self.algorithm_var.get()

        if not file_path or not message or not algorithm:
            messagebox.showerror("Hata", "Lütfen dosya, mesaj ve algoritma seçiniz.")
            return

        if algorithm == "LSB":
            output_path = os.path.join("output", "lsb_encoded.png")
            success = encode_lsb(file_path, message, output_path)
            if success:
                self.status_label.config(text="Mesaj başarıyla gizlendi: " + output_path)
            else:
                self.status_label.config(text="Gizleme başarısız.", fg="red")

    def extract_message(self):
        file_path = self.filename_var.get()
        algorithm = self.algorithm_var.get()

        if not file_path or not algorithm:
            messagebox.showerror("Hata", "Lütfen dosya ve algoritma seçiniz.")
            return

        if algorithm == "LSB":
            message = decode_lsb(file_path)
            self.message_text.delete("1.0", tk.END)
            self.message_text.insert(tk.END, message)
            self.status_label.config(text="Mesaj başarıyla çözüldü.")

root = tk.Tk()
app = StegoApp(root)
root.mainloop()
