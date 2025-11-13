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

    # === IMPORT UPDATE XLSX ===
    print("Memulai proses import update XLSX...")
    file_path = "C:\\Users\\acer\\Downloads\\dataguru_update.xlsx"

    if not os.path.exists(file_path):
        raise Exception(f"File tidak ditemukan di path: {file_path}")

    # Buka halaman Data Guru
    driver.get("https://appv3.stagingquamuslms.com/school/teacher")
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Tambah Data')]"))
    )
    print("Halaman Data Guru siap.")
    time.sleep(2)

    # Klik tombol 'Pilihan'
    print("Mengklik tombol 'Pilihan'...")
    pilihan_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Pilihan']]"))
    )
    pilihan_button.click()
    time.sleep(2)
    print("Tombol 'Pilihan' berhasil diklik.")

    # Tunggu dropdown muncul
    print("Menunggu menu dropdown muncul...")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'mantine-Menu-dropdown')]"))
    )
    print("Menu dropdown sudah muncul.")
    time.sleep(1)

    # Klik menu "Import Update XLSX"
    print("Mengklik menu 'Import Update XLSX'...")
    import_update_menu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//div[contains(@class,'mantine-Menu-itemLabel') and normalize-space(text())='Import Update XLSX']"
        ))
    )
    try:
        import_update_menu.click()
    except Exception:
        driver.execute_script("arguments[0].click();", import_update_menu)
    print("Menu 'Import Update XLSX' berhasil diklik.")
    time.sleep(3)

    # Pilih file
    print("Mengklik tombol pilih file...")
    file_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )
    file_input.send_keys(file_path)
    print("File 'dataguru_update.xlsx' berhasil dimasukkan.")
    time.sleep(3)

    # Klik tombol Simpan
    print("Mengklik tombol 'Simpan'...")
    simpan_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    simpan_button.click()
    time.sleep(2)
    print("Tombol 'Simpan' berhasil diklik.")

    # Klik tombol konfirmasi "Ya, Simpan"
    print("Menunggu dan mengklik tombol 'Ya, Simpan'...")
    confirm_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space(text())='Ya, Simpan']]"))
    )
    time.sleep(1.5)
    confirm_button.click()
    print("Tombol 'Ya, Simpan' berhasil diklik.")
    time.sleep(3)

    # Tunggu popup sukses (cari teks Update success atau 'berhasil')
    print("Menunggu popup konfirmasi sukses...")
    try:
        popup_success = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH,
                "//*[contains(text(),'Update success') or contains(text(),'berhasil') or contains(text(),'Data berhasil dibuat')]"))
        )
        print("Popup konfirmasi sukses terdeteksi!")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ss_popup = f"import_update_success_{timestamp}.png"
        driver.save_screenshot(ss_popup)
        print(f"Screenshot popup sukses disimpan sebagai '{ss_popup}'")

    except TimeoutException:
        print("Tidak menemukan popup 'Update success' dalam waktu 30 detik.")
        raise Exception("Popup sukses tidak muncul setelah update data.")

    # Validasi hasil tanpa screenshot
    time.sleep(2)
    guru_dicari = "Ahmad Fauzan"
    print(f"Melakukan validasi: mencari '{guru_dicari}' di tabel...")

    try:
        search_input = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.mantine-TextInput-input"))
        )
        search_input.clear()
        search_input.send_keys(guru_dicari)
        search_input.send_keys(Keys.RETURN)
        time.sleep(3)

        guru_ditemukan = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, f"//td[contains(., '{guru_dicari}')]"))
        )
        if guru_ditemukan:
            print(f"Validasi BERHASIL: '{guru_dicari}' ditemukan di tabel.")

    except TimeoutException:
        print(f"Validasi GAGAL: '{guru_dicari}' tidak ditemukan di tabel.")
        raise Exception(f"Validasi gagal: '{guru_dicari}' tidak muncul di tabel.")

except Exception as e:
    print(f"Terjadi error: {e}")
    timestamp_error = datetime.now().strftime("%Y%m%d_%H%M%S")
    fail_ss = f"import_update_failed_{timestamp_error}.png"
    driver.save_screenshot(fail_ss)
    print(f"Screenshot error disimpan sebagai '{fail_ss}'")
finally:
    time.sleep(2)
    print("Menutup browser...")
    driver.quit()
