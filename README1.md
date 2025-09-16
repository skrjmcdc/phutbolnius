# Tugas 2

**Nama:** Muhammad Ibaadi Ilmi  
**NPM:** 2406357684  
**Kelas:** PBP A

**Link aplikasi:** <https://muhammad-ibaadi-phutbolnius.pbp.cs.ui.ac.id/>

## Step-by-step checklist

- Pertama, saya membuat direktori bernama `tugas` yang bersebelahan dengan direktori `football-news` yang berisi proyek tutorial.
- Di dalam direktori `tugas`, saya membuat dan menyalakan *virtual environment* Python:
    python3 -m venv env
    . env/bin/activate
- Selanjutnya saya menyalin file `requirements.txt` pada proyek tutorial ke proyek tugas:
    cp ../football-news/requirements.txt requirements.txt
- File `requirements.txt` berisi daftar modul Python yang akan saya perlukan untuk membuat proyek Django:
    django
    gunicorn
    whitenoise
    psycopg2-binary
    requests
    urllib3
    python-dotenv
- Saya meng-install semua modul Python tersebut dalam *virtual environment* saya:
    pip install -r requirements.txt
- Setelah meng-install semua modul yang diperlukan, saya memulai proyek Django dengan nama `phutbolnius`:
    python3 -m django startproject phutbolnius
- Selanjutnya saya membuat aplikasi bernama `main`:
    python3 manage.py startapp main
- Agar memastikan tidak ada error, saya menjalankan server pada laptop saya:
    python3 manage.py runserver 8123
- Kemudian saya mengaksesnya dengan mengetik `localhost:8123` pada *web browser* saya. Untungnya tidak ada error yang ditampilkan.
- Namun, ternyata di terminal muncul peringatan serta anjuran agar saya melakukan migrasi database terlebih dahulu, jadi saya menjalankan perintah yang disebutkan di terminal:
    python3 manage.py migrate
- Setelah itu, saya mulai mengerjakan halaman utama. Saya membuat direktori `templates` di folder aplikasi `main`, lalu di dalamnya saya membuat file `index.html` dengan isi sebagai berikut:

    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>
        <h1>Halo Dunia</h1>
    </body>
    </html>

- Kemudian saya mulai mengerjakan mekanisme routing agar pengguna dapat mengakses halaman utama.
- Saya kembali melakukan `runserver`, namun ternyata muncul error: ![](https://drive.google.com/file/d/1V7ombRweWjwVZoDyhrz4ryPhePNqlSwe/view)
- Setelah saya telusuri, ternyata masalahnya adalah saya belum menambahkan `main` ke dalam list `INSTALLED_APPS` di file proyek `settings.py`. Setelah saya tambahkan `main` ke dalam list `INSTALLED_APPS`, akhirnya halaman utama dapat ditampilkan.
- Setelah itu, saya menambahkan model `Product` di file `models.py`, lalu saya melakukan migrasi database agar model tersebut terekam oleh Django.
- Setelah sedikit mengubah halaman utama agar sesuai dengan requirement tugas, saya melakukan deployment ke PWS.
- Terakhir, saya menonaktifkan *virtual environment* Python:
    deactivate

## Bagan alur *request* *client*

![](https://drive.google.com/file/d/1AkQjLgdl9LWFaNF0YXXtmxelDPh8jlZY/view?usp=drive_link)

## Peran `settings.py`

Dalam proyek Django, `settings.py` sesuai namanya berfungsi untuk meng-konfigurasi proyek secara keseluruhan. Pengaturan yang tersedia antara lain:

## Cara kerja migrasi database di Django

Saat kita ingin melakukan migrasi database di Django, pertama kita perlu membuat daftar tindakan migrasi yang perlu dilakukan. Kita melakukannya dengan perintah berikut:
    python3 manage.py makemigrations
Setelah daftar tersebut dibuat, kita dapat melaksanakannya dengan perintah berikut:
    python3 manage.py migrate

## Alasan Django dijadikan permulaan pembelajaran pengembangan perangkat lunak

Menurut saya, alasan Django dijadikan permulaan pembelajaran pengembangan perangkat lunak adalah karena bahasa yang digunakan hanya satu, yaitu Python (selain bahasa-bahasa web), yang mana bahasa Python sangat mudah untuk dipelajari dan memang sudah dipelajari pada mata kuliah sebelumnya.
