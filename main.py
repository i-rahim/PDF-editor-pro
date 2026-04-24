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
        self.setFixedSize(500, 600)
        self.setWindowIcon(QIcon(resource_path("icon.png")))
        
        # --- MESAJ BOX STYLE ---
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
                border-bottom: 2px solid #0D0D0D; /* Line color and thickness */
                padding-bottom: 5px; /* Distance between text and the line */
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
            }
            
            #footer { 
                font-size: 11px;
                color: #4ade80; 
                margin-top: 100px; /* Reduced because the spacer will do the work */
                margin-bottom: 5px; 
                background: transparent; 
            }
            
            
            #btn_merge {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #403F3E, stop:1 #403F3E);
                
            }
            #btn_merge:hover { background: #0D0D0D; color: #A6A5A4 }

            #btn_split {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #403F3E, stop:1 #403F3E);
                
            }
            #btn_split:hover { background: #0D0D0D; color: #A6A5A4 }

            #btn_photo {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #403F3E, stop:1 #403F3E);
                
            }
            #btn_photo:hover { background: #0D0D0D; color: #A6A5A4 }

            #footer { font-size: 11px; color: #0D0D0D; margin-top: 25px; background: transparent; }

            /* MESAJ Box (QMessageBox) clear */
            QMessageBox {
                background-color: #FFAE00;
                border: 1px solid #38bdf8;
            }
            /* icon and text background clear */
            QMessageBox QLabel {
                color: #f8fafc;
                font-size: 14px;
                font-family: 'Segoe UI';
                background-color: transparent; /* background color clear */
                padding: 5px;
            }
            QMessageBox QPushButton {
                background-color: #334155;
                color: white;
                min-width: 80px;
                padding: 8px;
                border: 1px solid #38bdf8;
                margin-bottom: 5px;
            }
            QMessageBox QPushButton:hover {
                background-color: #38bdf8;
                color: #0f172a;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Title Label ---
        self.label = QLabel("PDF Editor")
        self.label.setObjectName("title_label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.btn_merge = QPushButton("📂  MERGE PDF FILES")
        self.btn_merge.setObjectName("btn_merge")
        self.btn_merge.clicked.connect(self.pdf_merge)
        layout.addWidget(self.btn_merge)

        self.btn_split = QPushButton("✂️  SPLIT PDF PAGES (ALL)")
        self.btn_split.setObjectName("btn_split")
        self.btn_split.clicked.connect(self.pdf_ayir)
        layout.addWidget(self.btn_split)

        self.btn_photo = QPushButton("📸   CREATE A PDF FROM AN IMAGE")
        self.btn_photo.setObjectName("btn_photo")
        self.btn_photo.clicked.connect(self.photo_to_pdf)
        layout.addWidget(self.btn_photo)

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
            value = ctypes.c_int(0)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(value), ctypes.sizeof(value))
        except: pass

    def pdf_merge(self):
        dosyalar, _ = QFileDialog.getOpenFileNames(self, "Select PDF", "", "PDF (*.pdf)")
        if dosyalar:
            try:
                merger = PdfWriter()
                for pdf in dosyalar: merger.append(pdf)
                kayit, _ = QFileDialog.getSaveFileName(self, "Save", "newpdf_doc.pdf", "PDF (*.pdf)")
                if kayit:
                    with open(kayit, "wb") as f: merger.write(f)
                    self.show_msg("Successful", "The files have been successfully merged!")
            except Exception as e: self.show_msg("Error", f"Hata: {str(e)}", True)

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
                        with open(os.path.join(klasor, f"sayfa_{i+1}.pdf"), "wb") as f:
                            writer.write(f)
                    self.show_msg("Successful", f"{len(reader.pages)} pages have been saved to the folder!")
                except Exception as e: self.show_msg("Error", f"İşlem başarısız: {str(e)}", True)

    def photo_to_pdf(self):
        photoler, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Images (*.jpg *.png *.jpeg)")
        if photoler:
            try:
                A4_W, A4_H = (595, 842)
                pdf_sayfalari = []
                for r in photoler:
                    img = Image.open(r)
                    
                    # High-quality conversion
                    if img.mode in ("RGBA", "P"):
                        canvas = Image.new("RGB", img.size, (255, 255, 255))
                        canvas.paste(img.convert("RGBA"), mask=img.convert("RGBA").split()[3])
                        img = canvas
                    else:
                        img = img.convert('RGB')
                    
                    # Resize while keeping maximum quality
                    img.thumbnail((A4_W, A4_H), Image.Resampling.LANCZOS)
                    sayfa = Image.new('RGB', (A4_W, A4_H), (255, 255, 255))
                    sayfa.paste(img, ((A4_W - img.width) // 2, (A4_H - img.height) // 2))
                    pdf_sayfalari.append(sayfa)

                if pdf_sayfalari:
                    kayit, _ = QFileDialog.getSaveFileName(self, "Save", "image_pdf.pdf", "PDF (*.pdf)")
                    if kayit:
                        # quality=100 and subsampling=0 ensures maximum detail retention
                        pdf_sayfalari[0].save(
                            kayit, 
                            save_all=True, 
                            append_images=pdf_sayfalari[1:], 
                            quality=100, 
                            subsampling=0
                        )
                        self.show_msg("Successful", "Image to PDF has been created!")
            except Exception as e: self.show_msg("Error", f"Error: {str(e)}", True)

    def show_msg(self, baslik, mesaj, is_error=False):
        msg = QMessageBox(self)
        msg.setWindowTitle(baslik)
        msg.setText(mesaj)
        msg.setIcon(QMessageBox.Icon.Critical if is_error else QMessageBox.Icon.Information)
        msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if os.name == 'nt': # Sadece Windows ise
        myappid = 'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app.setStyle("Fusion")
    window = PDFEditor()
    window.show()
    sys.exit(app.exec())