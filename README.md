# Sistem Rekomendasi Jurnal Bisnis Digital


Selamat datang di Sistem Rekomendasi Jurnal Bisnis Digital! Proyek ini bertujuan untuk mempermudah proses menemukan jurnal bisnis digital terindex scopus yang relevan untuk keperluan penelitian dan akademis.
Dengan memanfaatkan teknik analisis teks canggih dan dataset komprehensif dari Scopus, sistem ini menyediakan rekomendasi jurnal yang akurat dan relevan.

### Apa Itu Sistem Ini?

Sistem Rekomendasi Jurnal Bisnis Digital adalah sebuah aplikasi web yang dirancang untuk membantu peneliti, akademisi, dan mahasiswa dalam menemukan jurnal yang paling sesuai dengan topik penelitian mereka. Sistem ini menggunakan algoritma pemrosesan bahasa alami (NLP) untuk menganalisis teks dari judul dan abstrak jurnal, kemudian mencocokkannya dengan kata kunci yang dimasukkan oleh pengguna.

### Tujuan

Tujuan utama dari sistem ini adalah untuk menghemat waktu dan usaha pengguna dalam mencari literatur penelitian yang relevan. Dengan memberikan rekomendasi yang tepat, sistem ini memungkinkan pengguna untuk lebih fokus pada aspek penting dari pekerjaan penelitian mereka.

### Teknologi yang Digunakan

- **Flask**: Kerangka kerja web untuk membangun aplikasi.
- **SQLAlchemy**: ORM untuk interaksi basis data.
- **Pandas**: Manipulasi dan analisis data.
- **scikit-learn**: Pustaka pembelajaran mesin untuk pemrosesan teks.
- **spaCy**: Pustaka pemrosesan bahasa alami.
- **NLTK**: Toolkit bahasa alami untuk pemrosesan teks.
- **Flask-Mail**: Penanganan email untuk fungsi reset kata sandi.
- **SQLite**: Basis data untuk menyimpan informasi pengguna dan penanda.

### Content Based Filtering

Sistem ini menggunakan pendekatan Content Based Filtering untuk memberikan rekomendasi jurnal. Teknik yang digunakan meliputi:

- **TF-IDF (Term Frequency-Inverse Document Frequency)**: Teknik ini digunakan untuk mengubah teks menjadi vektor numerik yang mencerminkan pentingnya kata-kata dalam dokumen.
- **Cosine Similarity**: Metode ini digunakan untuk mengukur kesamaan antara dua vektor teks. Dengan menghitung cosine similarity antara vektor kata kunci yang dimasukkan pengguna dan vektor jurnal dalam database, sistem dapat menemukan jurnal yang paling relevan.

## Fitur

- **Autentikasi Pengguna**: Registrasi, login, dan manajemen profil pengguna.
- **Rekomendasi Jurnal**: Masukkan kata kunci untuk menerima daftar rekomendasi jurnal berdasarkan kesamaan teks.
- **Penandaan (Bookmarking)**: Simpan dan kelola penanda untuk akses mudah ke artikel penting.
- **Reset Kata Sandi**: Reset kata sandi dengan aman melalui email.
- **Saran**: Kirimkan saran atau masukan untuk meningkatkan sistem.

## Screenshots:

![Screenshot 2024-05-20 195957](https://github.com/user-attachments/assets/409a5846-652e-42d3-92ed-900010a22329)
![Screenshot 2024-05-20 192449](https://github.com/user-attachments/assets/34478757-4292-4140-ae24-79a9cb872cd8)
![Screenshot 2024-05-20 192509](https://github.com/user-attachments/assets/128e539a-e4bb-47b2-85b9-1731e78e8746)
![Screenshot 2024-05-20 192520](https://github.com/user-attachments/assets/b82aee51-9ec8-4e58-8a32-aa2b018739ac)
![Screenshot 2024-05-20 192529](https://github.com/user-attachments/assets/942141b9-71d7-463d-beca-bf402ec68a1e)
![Screenshot 2024-05-20 192557](https://github.com/user-attachments/assets/329324c8-9cc9-4f40-8bfe-4e63737a4d01)
![Screenshot 2024-05-20 192611](https://github.com/user-attachments/assets/7784a2ee-ea06-49de-8c3b-165f19bafa61)
![Screenshot 2024-05-20 192423](https://github.com/user-attachments/assets/7ee2a720-f0af-47a8-9d3c-4c6491f6eb82)



