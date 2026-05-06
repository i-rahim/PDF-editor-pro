import sys
import os
import ctypes
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QWidget, QFileDialog, QMessageBox, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from pypdf import PdfWriter, PdfReader
from PIL import Image

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class PDFEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Editor 1.0")
        self.setFixedSize(500, 650) # Boyutu biraz artırdık yeni buton için
        self.setWindowIcon(QIcon(resource_path("icon.png")))
        
        # --- STYLE SHEET ---
        self.setStyleSheet("""
            QMainWindow, QWidget { 
                background-color: #F2EEEB; 
            }
            QLabel { 
                font-family: 'Segoe UI Semibold'; 
                font-size: 24px; 
                color: #737272; 
                margin-bottom: 30px;
                background-color: transparent;
            }
            
            #title_label {
                font-family: 'Lucida Handwriting', 'Segoe Script', cursive;
                font-size: 42px;
                font-weight: bold;
                color: #0D0D0D;
                margin-top: 5px;
                margin-bottom: 50px;
                background-color: transparent;
                border-bottom: 2px solid #0D0D0D;
                padding-bottom: 5px;
            }

            QPushButton { 
                border-radius: 12px; 
                padding: 18px; 
                font-family: 'Segoe UI'; 
                font-size: 14px; 
                font-weight: bold;
                min-width: 280px; 
                margin-bottom: 15px;
                color: #ffffff;
                text-align: center;
                background: #403F3E;
            }
            
            QPushButton:hover { 
                background: #0D0D0D; 
                color: #A6A5A4; 
            }

            #footer { 
                font-size: 11px; 
                color: #0D0D0D; 
                margin-top: 25px; 
                background: transparent; 
            }

            QMessageBox {
                background-color: #FFAE00;
            }
            QMessageBox QLabel {
                color: #f8fafc;
                font-size: 14px;
                font-family: 'Segoe UI';
                background-color: transparent;
            }
            QMessageBox QPushButton {
                background-color: #334155;
                color: white;
                min-width: 80px;
                padding: 8px;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- UI Elements ---
        self.label = QLabel("PDF Editor")
        self.label.setObjectName("title_label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        # Merge Button
        self.btn_merge = QPushButton("📂  MERGE PDF FILES")
        self.btn_merge.clicked.connect(self.pdf_merge)
        layout.addWidget(self.btn_merge)

        # Split Button
        self.btn_split = QPushButton("✂️  SPLIT PDF PAGES (ALL)")
        self.btn_split.clicked.connect(self.pdf_ayir)
        layout.addWidget(self.btn_split)

        # Photo to PDF Button
        self.btn_photo = QPushButton("📸   CREATE A PDF FROM AN IMAGE")
        self.btn_photo.clicked.connect(self.photo_to_pdf)
        layout.addWidget(self.btn_photo)

        # COMPRESS Button (New)
        self.btn_compress = QPushButton("📉   COMPRESS PDF")
        self.btn_compress.clicked.connect(self.pdf_compress)
        layout.addWidget(self.btn_compress)

        footer = QLabel("2026 Copyright - RI")
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.apply_dark_title_bar()

    def apply_dark_title_bar(self):
        try:
            hwnd = int(self.winId())
            value = ctypes.c_int(1) # Dark mode title bar
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(value), ctypes.sizeof(value))
        except: pass

    def pdf_merge(self):
        dosyalar, _ = QFileDialog.getOpenFileNames(self, "Select PDF", "", "PDF (*.pdf)")
        if dosyalar:
            try:
                merger = PdfWriter()
                for pdf in dosyalar: merger.append(pdf)
                kayit, _ = QFileDialog.getSaveFileName(self, "Save", "merged_doc.pdf", "PDF (*.pdf)")
                if kayit:
                    with open(kayit, "wb") as f: merger.write(f)
                    self.show_msg("Successful", "The files have been successfully merged!")
            except Exception as e: self.show_msg("Error", f"Error: {str(e)}", True)

    def pdf_ayir(self):
        dosya, _ = QFileDialog.getOpenFileName(self, "Select the PDF to Split", "", "PDF (*.pdf)")
        if dosya:
            klasor = QFileDialog.getExistingDirectory(self, "Select Folder")
            if klasor:
                try:
                    reader = PdfReader(dosya)
                    for i, sayfa in enumerate(reader.pages):
                        writer = PdfWriter()
                        writer.add_page(sayfa)
                        with open(os.path.join(klasor, f"page_{i+1}.pdf"), "wb") as f:
                            writer.write(f)
                    self.show_msg("Successful", f"{len(reader.pages)} pages have been saved!")
                except Exception as e: self.show_msg("Error", f"Error: {str(e)}", True)

    def photo_to_pdf(self):
        photoler, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Images (*.jpg *.png *.jpeg)")
        if photoler:
            try:
                A4_W, A4_H = (595, 842)
                pdf_sayfalari = []
                for r in photoler:
                    img = Image.open(r)
                    if img.mode in ("RGBA", "P"):
                        canvas = Image.new("RGB", img.size, (255, 255, 255))
                        canvas.paste(img.convert("RGBA"), mask=img.convert("RGBA").split()[3])
                        img = canvas
                    else:
                        img = img.convert('RGB')
                    
                    img.thumbnail((A4_W, A4_H), Image.Resampling.LANCZOS)
                    sayfa = Image.new('RGB', (A4_W, A4_H), (255, 255, 255))
                    sayfa.paste(img, ((A4_W - img.width) // 2, (A4_H - img.height) // 2))
                    pdf_sayfalari.append(sayfa)

                if pdf_sayfalari:
                    kayit, _ = QFileDialog.getSaveFileName(self, "Save", "image_pdf.pdf", "PDF (*.pdf)")
                    if kayit:
                        pdf_sayfalari[0].save(kayit, save_all=True, append_images=pdf_sayfalari[1:], quality=100)
                        self.show_msg("Successful", "Image to PDF created!")
            except Exception as e: self.show_msg("Error", f"Error: {str(e)}", True)

    def pdf_compress(self):
        dosya, _ = QFileDialog.getOpenFileName(self, "Select PDF to Compress", "", "PDF (*.pdf)")
        if dosya:
            try:
                old_size = os.path.getsize(dosya) / (1024 * 1024)
                reader = PdfReader(dosya)
                writer = PdfWriter()

                for page in reader.pages:
                    writer.add_page(page)

                # Tarama dosyaları için görsel sıkıştırma (quality=60)
                for page in writer.pages:
                    for img in page.images:
                        img.replace(img.image, quality=60)

                kayit, _ = QFileDialog.getSaveFileName(self, "Save Compressed PDF", "compressed_doc.pdf", "PDF (*.pdf)")
                if kayit:
                    with open(kayit, "wb") as f:
                        writer.write(f)
                    
                    new_size = os.path.getsize(kayit) / (1024 * 1024)
                    reduction = ((old_size - new_size) / old_size) * 100
                    
                    self.show_msg("Successful", 
                                 f"Compression Finished!\n\n"
                                 f"Original: {old_size:.2f} MB\n"
                                 f"Compressed: {new_size:.2f} MB\n"
                                 f"Reduction: %{reduction:.1f}")
            except Exception as e: self.show_msg("Error", f"Error: {str(e)}", True)

    def show_msg(self, baslik, mesaj, is_error=False):
        msg = QMessageBox(self)
        msg.setWindowTitle(baslik)
        msg.setText(mesaj)
        msg.setIcon(QMessageBox.Icon.Critical if is_error else QMessageBox.Icon.Information)
        msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if os.name == 'nt':
        myappid = 'mycompany.pdfeditor.v1'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app.setStyle("Fusion")
    window = PDFEditor()
    window.show()
    sys.exit(app.exec())
