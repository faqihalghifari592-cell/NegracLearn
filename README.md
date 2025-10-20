# Web Pembelajaran Rancabungur

Platform pembelajaran berbasis Flask untuk menampilkan dan mengelola media edukatif secara otomatis. Mendukung login berbasis file Excel dari Google Drive, preview file, dan dashboard interaktif.

## Fitur
- Login admin dari file Excel (via gdown)
- Upload dan preview file PDF, PPT, gambar
- Filter berdasarkan kategori
- Tampilan responsif untuk guru dan siswa

## Struktur Folder
web-pembelajaran/ 
├── app/ # File utama Flask (app.py) 
│ └── app.py 
├── templates/ # HTML untuk login dan dashboard │ 
├── login.html │
 └── index.html 
 ├── static/ # File CSS, JS, dan gambar pendukung 
 ├── data/ # Tempat file Excel login (diunduh otomatis) │
  └── admin_list.xlsx 
├── instance/ # Folder instance Flask (opsional) 
├── venv/ # Virtual environment (tidak diupload) 
├── .gitignore # Abaikan file lokal dan environment 
├── requirements.txt # Modul Python yang dibutuhkan 
├── Procfile # Untuk deploy via Gunicorn di Render 
├── render.yaml # Konfigurasi Render (opsional) 
├── README.md # Dokumentasi proyek 
├── run.py # Alternatif entry point Flask 
├── data.py # Modul data tambahan 
├── test_drive.py # Script pengujian akses Google Drive 
├── client_secrets.json # Konfigurasi OAuth (jika digunakan)


## Cara Menjalankan Secara Lokal
```bash
pip install -r requirements.txt
python app/app.py
