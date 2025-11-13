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
    print("✅ Login berhasil!")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    time.sleep(3)

    # ======== TAMBAH DATA GURU ========
    print("Membuka halaman Data Pokok Guru...")
    driver.get("https://appv3.stagingquamuslms.com/school/teacher")
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Tambah Data')]")))
    print("✅ Halaman Data Pokok Guru terbuka.")

    # ======== VALIDASI DENGAN SEARCH ========
    print("Melakukan pencarian data guru yang baru ditambahkan...")
    search_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[contains(@class,'mantine-TextInput-input')]"))
    )
    search_input.clear()
    search_input.send_keys("Budi Santoso")
    time.sleep(2)

    print("Menunggu hasil pencarian muncul...")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//td[contains(., 'Budi Santoso')]"))
    )
    print("✅ Data 'Budi Santoso' ditemukan di hasil pencarian!")

    # ======== BUAT AKUN GURU ========
    print("Membuka menu Aksi → Buat Akun...")
    aksi_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//tr[.//td[contains(., 'Budi Santoso')]]//button[contains(@class,'mantine-ActionIcon-root')]"))
    )
    aksi_button.click()
    time.sleep(1)

    buat_akun_menu = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//div[text()='Buat Akun']]"))
    )
    buat_akun_menu.click()
    print("Klik menu 'Buat Akun' berhasil.")

    print("Menunggu konfirmasi 'Ya, Buat Akun'...")
    confirm_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Ya, Buat Akun']"))
    )
    confirm_button.click()
    print("✅ Klik 'Ya, Buat Akun' berhasil.")

    # ======== VALIDASI AKHIR ========
    print("Memeriksa pesan sukses...")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'berhasil') and contains(text(), 'akun')]"))
    )
    print("✅ Akun guru berhasil dibuat!")

    ss_name = f"success_buat_akun_{timestamp}.png"
    driver.save_screenshot(ss_name)
    print(f"📸 Screenshot disimpan: {ss_name}")

except Exception as e:
    print(f"❌ Terjadi error: {e}")
    fail_name = f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    driver.save_screenshot(fail_name)
    print(f"📸 Screenshot error: {fail_name}")

finally:
    print("Menutup browser...")
    driver.quit()
