import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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
    time.sleep(3)

    # ======== Export Update XLSX ========
    print("Memulai proses Export Update XLSX...")
    driver.get("https://appv3.stagingquamuslms.com/school/teacher")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Tambah Data')]"))
    )
    print("Halaman Data Guru siap.")

    # --- Klik tombol "Pilihan" ---
    print("Mengklik tombol 'Pilihan'...")
    pilihan_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Pilihan']]"))
    )
    pilihan_button.click()
    print("Tombol 'Pilihan' berhasil diklik.")

    # Tambahkan jeda agar menu dropdown muncul dengan sempurna
    print("Menunggu menu dropdown terbuka dengan sempurna (5 detik)...")
    time.sleep(5)

    # --- Tunggu menu dropdown muncul ---
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'mantine-Menu-dropdown')]"))
    )
    print("Menu dropdown sudah muncul dan siap.")

    # --- Klik menu "Export Update XLSX" ---
    print("Mengklik menu 'Export Update XLSX'...")
    export_update_menu_item = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[.//div[contains(@class, 'mantine-Menu-itemLabel') and text()='Export Update XLSX']]"
        ))
    )
    export_update_menu_item.click()
    print("Menu 'Export Update XLSX' berhasil diklik.")

    # Tambahkan jeda agar proses export benar-benar selesai
    print("Menunggu proses export selesai (5 detik)...")
    time.sleep(10)

    # --- Screenshot bukti ---
    timestamp_export = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_ss = f"export_update_xlsx_clicked_success_{timestamp_export}.png"
    driver.save_screenshot(export_ss)
    print(f"Screenshot disimpan sebagai '{export_ss}'")
    print("Silakan periksa folder Downloads Anda untuk memastikan file XLSX telah tersimpan.")

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
