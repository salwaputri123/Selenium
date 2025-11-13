import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
# options.add_argument("--headless") # Uncomment jika ingin menjalankan tanpa tampilan browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("Membuka halaman login...")
    driver.get("https://appv3.stagingquamuslms.com/login?redirectUrl=%2F")
    driver.maximize_window()
    time.sleep(2)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@data-path='code']"))
    )

    # ======== LOGIN ========
    driver.find_element(By.XPATH, "//input[@data-path='code']").clear()
    driver.find_element(By.XPATH, "//input[@data-path='code']").send_keys("quamus")
    time.sleep(1)

    driver.find_element(By.XPATH, "//input[@data-path='username']").clear()
    driver.find_element(By.XPATH, "//input[@data-path='username']").send_keys("superadmin")
    time.sleep(1)

    driver.find_element(By.XPATH, "//input[@data-path='password']").clear()
    driver.find_element(By.XPATH, "//input[@data-path='password']").send_keys("bEz81Z1hzLdy2uJrwunBavzwKWIdKwRZS5Etij4yS0hJm")
    time.sleep(1)

    print("Klik tombol Submit...")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    print("Menunggu tampilan dashboard...")
    WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//*[contains(text(),'Selamat Datang') or contains(text(),'Superadmin') or contains(text(),'Aplikasi QuamusLMS')]"
        ))
    )
    print("Login berhasil!")

    time.sleep(2)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

   
    # ======== Tambah Data Guru ========
    print("Membuka halaman Data Pokok Guru...")
    driver.get("https://appv3.stagingquamuslms.com/school/teacher")
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Tambah Data')]"))
    )
    print("Halaman Data Pokok Guru berhasil terbuka!")
    time.sleep(1)

    # ======== Cari Data yang Baru Ditambahkan ========
    print("Mencari data 'Budi Santoso' di kolom pencarian...")
    search_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.mantine-TextInput-input"))
    )
    search_input.clear()
    search_input.send_keys("Budi Santoso")
    print("Pencarian dilakukan.")
    time.sleep(2)

    print("Melakukan validasi akhir: Memeriksa apakah data guru muncul di tabel hasil pencarian...")
    # Jika tidak ditemukan, akan memicu TimeoutException dan langsung loncat ke blok 'except' di paling bawah
    teacher_name_in_table = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//td[contains(., 'Budi Santoso')]"))
    )
    print("Validasi BERHASIL: Data 'Budi Santoso' ditemukan di tabel hasil pencarian!")

    # ======== Buat Akun untuk Guru ========
    print("Memulai proses pembuatan akun untuk 'Budi Santoso'...")
    
    # --- Tahap 1: Kembali ke daftar guru utama ---
    print("Mengosongkan kolom pencarian untuk melihat semua guru...")
    search_input.clear()
    driver.find_element(By.TAG_NAME, 'body').click()
    time.sleep(2)
    print("Kolom pencarian dikosongkan.")
    # --- Tahap 2 & 3: Temukan baris guru dan klik tombol "Aksi" ---
    print("Mencari baris 'Budi Santoso' dan mengklik tombol 'Aksi'...")
    aksi_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//tr[.//td[contains(., 'Budi Santoso')]]//button[contains(@class, 'mantine-ActionIcon-root')]"))
    )
    aksi_button.click()
    print("Tombol 'Aksi' untuk 'Budi Santoso' berhasil diklik.")

    # --- Tahap 4 & 5: Tunggu menu muncul dan klik "Buat Akun" ---
    print("Menunggu menu muncul dan mengklik 'Buat Akun'...")
    buat_akun_menu = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//div[text()='Buat Akun']]"))
    )
    buat_akun_menu.click()
    print("Menu 'Buat Akun' berhasil diklik.")

    # --- TAHAP BARU: Tunggu dan Klik Konfirmasi "Ya, Buat Akun" ---
    print("Menunggu dialog konfirmasi 'Ya, Buat Akun'...")
    confirm_button = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//button[.//span[text()='Ya, Buat Akun']]"))
    )
    confirm_button.click()
    print("Tombol 'Ya, Buat Akun' berhasil diklik.")

    # --- Tahap 6: Validasi Akhir Akun (Setelah Konfirmasi) ---
    print("Melakukan validasi akhir: Memeriksa apakah akun berhasil dibuat...")
    # Jika tidak ditemukan, akan memicu TimeoutException dan langsung loncat ke blok 'except' di paling bawah
    success_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'berhasil') and contains(text(), 'akun')]"))
    )
    print("Validasi BERHASIL: Pesan sukses pembuatan akun ditemukan!")
    account_saved_ss = f"account_created_success_{timestamp}.png"
    driver.save_screenshot(account_saved_ss)
    print(f"Screenshot 'Akun Berhasil Dibuat' disimpan sebagai '{account_saved_ss}'")

except Exception as e:
    print(f"Terjadi error: {e}")
    timestamp_error = datetime.now().strftime("%Y%m%d_%H%M%S")
    fail_ss = f"test_failed_{timestamp_error}.png"
    driver.save_screenshot(fail_ss)
    print(f"Screenshot error disimpan sebagai '{fail_ss}'")
finally:
    time.sleep(1)
    print("Menutup browser...")
    driver.quit()