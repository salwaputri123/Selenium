import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("=== MEMBUKA HALAMAN LOGIN ===")
    driver.get("https://appv3.stagingquamuslms.com/login?redirectUrl=%2F")
    driver.maximize_window()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@data-path='code']")))

    # ======== LOGIN AKUN SEKOLAH ========
    print("Mengisi form login sekolah...")
    code = driver.find_element(By.XPATH, "//input[@data-path='code']")
    user = driver.find_element(By.XPATH, "//input[@data-path='username']")
    pw = driver.find_element(By.XPATH, "//input[@data-path='password']")

    code.clear(); code.send_keys("sdattaqwa")
    time.sleep(0.5)
    user.clear(); user.send_keys("admin")
    time.sleep(0.5)
    pw.clear(); pw.send_keys("83630")
    time.sleep(0.5)

    print("Klik tombol Login...")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    print("Menunggu tampilan dashboard...")
    WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Selamat Datang') or contains(text(),'Dashboard')]"))
    )
    print("Login berhasil!")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    time.sleep(2)


    # === IMPORT XLSX ===
    print("Memulai proses import XLSX...")
    file_path = "C:\\Users\\acer\\Downloads\\data_guru.xlsx"

    if not os.path.exists(file_path):
        raise Exception(f"File tidak ditemukan di path: {file_path}")

    # Buka halaman guru
    driver.get("https://appv3.stagingquamuslms.com/school/teacher")
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Tambah Data')]"))
    )
    print("Halaman Data Guru siap.")

    # Klik tombol 'Pilihan'
    print("Mengklik tombol 'Pilihan'...")
    pilihan_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Pilihan']]"))
    )
    pilihan_button.click()
    print("Tombol 'Pilihan' berhasil diklik.")

    # Tunggu menu dropdown muncul
    print("Menunggu menu dropdown muncul...")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'mantine-Menu-dropdown')]"))
    )
    print("Menu dropdown sudah muncul.")
    # Klik menu Import XLSX
    print("Mencari dan mengklik menu 'Import XLSX'...")
    import_menu_item = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'Menu-itemLabel') and contains(text(),'Import XLSX')]"))
    )
    import_menu_item.click()
    print("Menu 'Import XLSX' berhasil diklik.")

    # Pilih file
    print("Mengklik tombol pilih file...")
    file_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )
    file_input.send_keys(file_path)
    print("File berhasil dimasukkan ke input.")

    # Tunggu sejenak agar file diproses
    time.sleep(3)

    # Klik tombol Simpan
    print("Mengklik tombol 'Simpan'...")
    simpan_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    simpan_button.click()
    print("Tombol 'Simpan' berhasil diklik.")

       # Konfirmasi 'Ya, Simpan'
    print("Menunggu dialog konfirmasi 'Ya, Simpan'...")
    confirm_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Ya, Simpan']]"))
    )
    confirm_button.click()
    print("Tombol 'Ya, Simpan' berhasil diklik.")

    # Tunggu popup konfirmasi sukses
    print("Menunggu popup konfirmasi 'Create success' muncul...")
    try:
        popup_success = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//*[contains(text(),'Create success') or contains(text(),'berhasil') or contains(text(),'Data berhasil dibuat')]"
            ))
        )
        print("Popup konfirmasi sukses terdeteksi!")

        # Screenshot ketika popup muncul
        timestamp_import = datetime.now().strftime("%Y%m%d_%H%M%S")
        import_ss = f"import_xlsx_success_{timestamp_import}.png"
        driver.save_screenshot(import_ss)
        print(f"Screenshot popup 'Create Success' disimpan sebagai '{import_ss}'")

    except TimeoutException:
        print("Tidak menemukan popup 'Create success' dalam waktu 30 detik.")
        raise Exception("Popup sukses tidak muncul setelah menyimpan data.")

    # Tambahkan sedikit delay untuk memastikan halaman siap sebelum validasi
    time.sleep(3)


    # === CEK NAMA GURU DI TABEL ===
    guru_dicari = "Ahmad Fauzan"
    print(f"Melakukan validasi akhir: mencari nama guru '{guru_dicari}' di tabel...")

    try:
        # Tunggu kolom pencarian muncul
        search_input = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.mantine-TextInput-input"))
        )
        search_input.clear()
        search_input.send_keys(guru_dicari)
        search_input.send_keys(Keys.RETURN)
        time.sleep(2)

        # Cek apakah nama muncul di tabel
        guru_ditemukan = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, f"//td[contains(., '{guru_dicari}')]"))
        )
        if guru_ditemukan:
            print(f"Validasi BERHASIL: Data '{guru_dicari}' ditemukan di tabel.")
            validation_ss = f"validation_success_{timestamp_import}.png"
            driver.save_screenshot(validation_ss)
            print(f"Screenshot validasi disimpan sebagai '{validation_ss}'")

    except TimeoutException:
        print(f"Validasi GAGAL: Data '{guru_dicari}' tidak ditemukan di tabel.")
        validation_fail_ss = f"validation_failed_{timestamp_import}.png"
        driver.save_screenshot(validation_fail_ss)
        print(f"Screenshot kegagalan validasi disimpan sebagai '{validation_fail_ss}'")
        raise Exception(f"Validasi gagal: '{guru_dicari}' tidak muncul di tabel hasil pencarian.")

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
