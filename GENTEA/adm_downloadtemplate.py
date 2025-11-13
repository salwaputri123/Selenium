import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Jalankan tanpa tampilan browser (opsional)
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

    # ======== Download Template ========
    print("Memulai proses download template...")
    
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

    print("Menunggu menu dropdown muncul sempurna...")
    time.sleep(3) # Beri waktu 3 detik untuk animasi dan perhitungan layout

    # --- Klik menu "Download Template" ---
    print("Mengklik menu 'Download Template'...")
    # Menggunakan locator yang paling spesifik dan benar
    download_menu_item = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//div[contains(@class, 'Menu-itemLabel') and text()='Download Template']]"))
    )
    download_menu_item.click()
    print("Menu 'Download Template' berhasil diklik.")
    
    # Beri waktu sebentar untuk notifikasi download muncul
    time.sleep(3)

    # --- Screenshot bukti bahwa tombol telah diklik ---
    timestamp_download = datetime.now().strftime("%Y%m%d_%H%M%S")
    download_ss = f"template_download_success_{timestamp_download}.png"
    driver.save_screenshot(download_ss)
    print(f"Screenshot 'Download Berhasil' disimpan sebagai '{download_ss}'")
    print("Silakan periksa folder Downloads Anda untuk memastikan file template telah tersimpan.")


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