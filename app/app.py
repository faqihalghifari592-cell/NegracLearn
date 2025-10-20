from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
import os
import pandas as pd
import gdown
from werkzeug.utils import secure_filename
from flask import Flask
app = Flask(__name__)


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_key')
file_id = os.environ.get('EXCEL_FILE_ID')

# 📁 Konfigurasi folder upload
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.join('static', 'uploads'))

# ✅ Batas ukuran file
MAX_SIZE_DEFAULT = 30 * 1024 * 1024      # 30 MB untuk file biasa
MAX_SIZE_MEDIA   = 1024 * 1024 * 1024    # 1 GB untuk video/audio

# ✅ Ekstensi file yang diizinkan
ALLOWED_EXTENSIONS = {'pdf', 'ppt', 'pptx', 'jpg', 'jpeg', 'png', 'mp4', 'mp3', 'wav'}

# 🔍 Fungsi validasi ekstensi
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ✅ Fungsi validasi ukuran file
def check_file_size(file):
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)  # reset posisi baca

    ext = file.filename.rsplit('.', 1)[1].lower()

    if ext in {'mp4', 'mp3', 'wav'}:
        return size <= MAX_SIZE_MEDIA
    else:
        return size <= MAX_SIZE_DEFAULT

# 📄 Baca data login dari Excel
excel_path = os.path.join('data', 'admin_list.xlsx')
if not os.path.exists(excel_path):
    raise FileNotFoundError(f"❌ File Excel tidak ditemukan: {excel_path}")

df = pd.read_excel(excel_path)
df.columns = df.columns.str.strip().str.lower()  # Normalisasi header

if 'username' not in df.columns or 'password' not in df.columns:
    raise ValueError("❌ Kolom 'username' dan 'password' wajib ada di file Excel.")

users = dict(zip(df['username'].astype(str), df['password'].astype(str)))

# 🏠 Halaman utama: tampilkan semua file
@app.route('/')
def index():

    folder = app.config['UPLOAD_FOLDER']

    # 🔧 Pastikan folder upload ada
    if not os.path.exists(folder):
        os.makedirs(folder)

    files = os.listdir(folder)

    query = request.args.get('q', '').lower()
    kategori = request.args.get('kategori', '').lower()

    if query:
        files = [f for f in files if query in f.lower()]

    return render_template('index.html', files=files)



# 🔐 Login guru
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 🔽 Unduh file Excel dari Google Drive
        file_id = "1DeB0-8q9D7EFkamjKHMCEp0VBGpzDnby"  # Ganti dengan ID file Excel kamu
        url = f"https://drive.google.com/uc?id={file_id}"
        local_path = os.path.join('data', 'admin_list.xlsx')

        # Pastikan folder data ada
        if not os.path.exists('data'):
            os.makedirs('data')

        gdown.download(url, local_path, quiet=False)

        # 📄 Baca file Excel lokal
        df = pd.read_excel(local_path)
        df.columns = df.columns.str.strip().str.lower()

        user_match = df[
            (df['username'] == username) &
            (df['password'] == password)
        ]

        if not user_match.empty:
            session['username'] = username
            return redirect('/')
        else:
            flash('Username atau password salah')
            return redirect('/login')

    return render_template('login.html')

# 🚪 Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# 📤 Upload file (hanya untuk guru login)
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files.get('file')

        if not file:
            error = "Tidak ada file yang diunggah."
            return render_template('upload.html', error=error)

        if not allowed_file(file.filename):
            error = "Jenis file tidak diizinkan."
            return render_template('upload.html', error=error)

        if not check_file_size(file):
            error = "Ukuran file melebihi batas yang diizinkan."
            return render_template('upload.html', error=error)

        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        return redirect(url_for('index'))  # ✅ INI HARUS DIINDEKTASIKAN

    return render_template('upload.html')  # ✅ Ini untuk GET method

@app.route('/hapus/<filename>', methods=['POST'])
def hapus(filename):
    if 'username' not in session:
        return redirect(url_for('login'))

    folder = app.config['UPLOAD_FOLDER']
    path = os.path.join(folder, filename)

    if os.path.exists(path):
        os.remove(path)
        print(f"✅ File dihapus: {filename}")
    else:
        print(f"❌ File tidak ditemukan: {filename}")

    return redirect(url_for('index'))



# 📄 Akses file langsung
@app.route('/media/<filename>')
def media(filename):
    folder = app.config['UPLOAD_FOLDER']
    path = os.path.join(folder, filename)

    if not os.path.exists(path):
        print("❌ File tidak ditemukan:", path)
        return "File tidak ditemukan", 404

    print("✅ Menyajikan file:", path)
    return send_from_directory(folder, filename)


if __name__ == '__main__':
    app.run(debug=True)

