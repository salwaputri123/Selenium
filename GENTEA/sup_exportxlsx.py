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
    # Tunggu hingga tombol submit benar-benar bisa diklik
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    submit_button.click()

    print("Menunggu 3 detik untuk memastikan proses login selesai...")
    time.sleep(3) 

    # Lanjutkan dengan logika menunggu dashboard
    print("Menunggu tampilan dashboard...")
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//*[contains(text(),'Selamat Datang') or contains(text(),'Superadmin') or contains(text(),'Aplikasi QuamusLMS')]"
        ))
    )
    print("Login berhasil!")

    # ======== Export XLSX ========
    print("Memulai proses export XLSX...")
    
    # Pastikan kita berada di halaman guru
    driver.get("https://appv3.stagingquamuslms.com/school/teacher")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Tambah Data')]")))
    print("Halaman Data Guru siap.")

    # --- Klik tombol "Pilihan" ---
    print("Mengklik tombol 'Pilihan'...")
    pilihan_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Pilihan']]"))
    )
    pilihan_button.click()
    print("Tombol 'Pilihan' berhasil diklik.")

    # --- Tunggu menu dropdown muncul ---
    print("Menunggu menu dropdown muncul sempurna...")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'mantine-Menu-dropdown')]"))
    )
    print("Menu dropdown sudah muncul dan siap.")

    # --- Klik menu "Export XLSX" ---
    print("Mengklik menu 'Export XLSX'...")
    export_menu_item = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//div[contains(@class, 'Menu-itemLabel') and text()='Export XLSX']]"))
    )
    export_menu_item.click()
    print("Menu 'Export XLSX' berhasil diklik.")
    
    # Beri waktu sebentar untuk proses export muncul
    time.sleep(3)

    # --- Screenshot bukti bahwa tombol telah diklik ---
    timestamp_export = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_ss = f"export_xlsx_clicked_success_{timestamp_export}.png"
    driver.save_screenshot(export_ss)
    print(f"Screenshot 'Export Klik Berhasil' disimpan sebagai '{export_ss}'")
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