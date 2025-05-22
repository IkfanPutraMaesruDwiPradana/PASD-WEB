#  Aplikasi Rekomendasi Karier Berdasarkan MBTI

Aplikasi ini dibuat untuk membantu pengguna mengetahui tipe kepribadian MBTI mereka melalui kuesioner sederhana, dan memberikan rekomendasi karier yang sesuai dengan tipe tersebut. Aplikasi ini dibangun menggunakan Python dan Streamlit.

---

##  Alur Pengembangan Aplikasi

### 1. Mencari dan Menyusun Data MBTI

Langkah pertama adalah mengumpulkan data yang relevan mengenai:

- **Struktur MBTI**: 4 dimensi utama (E/I, S/N, T/F, J/P).
- **16 tipe kepribadian MBTI** seperti INTP, ENFP, ISTJ, dsb.
- **Rekomendasi karier** untuk masing-masing tipe, berdasarkan sumber psikologi dan konseling karier.

### 2. Pre-processing Pertanyaan

Pada tahap ini, dilakukan penyesuaian dan pra-pemrosesan terhadap data pertanyaan:

- **Normalisasi Pertanyaan**: Membersihkan teks, memastikan tidak ada duplikasi.
- **Labelisasi Dimensi**: Setiap pertanyaan dikaitkan dengan salah satu dimensi MBTI.
- **Konversi Format**: Pertanyaan disimpan dalam format CSV atau JSON agar mudah dibaca oleh aplikasi web.

### 3. Melatih / Menyusun Logika Evaluasi MBTI

Berbeda dengan model machine learning, aplikasi ini menggunakan pendekatan berbasis aturan (rule-based):

- **Jawaban user di setiap pertanyaan (Setuju / Netral / Tidak Setuju) akan dikonversi ke skor numerik.**
- **Skor dikumpulkan berdasarkan dimensi.**
- **Hasil tertinggi dari tiap pasangan dimensi akan membentuk 4 huruf MBTI.**

### 4. Membangun Aplikasi Web
Tahap terakhir adalah menyusun tampilan dan logika interaktif dalam aplikasi web menggunakan Streamlit:

- **Tampilan Kuesioner**: Form pertanyaan dengan pilihan radio button.

- **Logika Evaluasi**: Menghitung hasil berdasarkan jawaban user.

- **Output**: Menampilkan tipe MBTI dan daftar karier yang cocok.

- **Opsional**: Visualisasi grafik, simpan hasil, export PDF, dan integrasi database.

file model randomforest
https://drive.google.com/file/d/1DDzP7owxInGaTqx-9077zXuNAsIg7qKC/view?usp=sharing

struktur model web
├── app.py
├── career.png
├── success_animation.json
├── random_forest_model.pkl
├── gender_encoder.pkl
├── interest_encoder.pkl
├── target_encoder.pkl
├── README.md

Keanggotaan 
- Ikfan Putra Maesru Dwi Pradana = 
- Khosyi Kafi Kirdiat = 
- Madina Nilasari = 
- Sabrina Salva Kalimatin Sava = 
- Novanditya Rhakahadi =
