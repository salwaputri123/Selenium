import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

# === KONFIGURASI BROWSER ===
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

    # === DELETE DATA GURU ===
    print("Memulai proses delete data guru...")

    driver.get("https://appv3.stagingquamuslms.com/school/teacher")
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Tambah Data')]"))
    )
    print("Halaman Data Guru siap.")

    guru_dicari = "Ahmad Fauzan"
    print(f"Mencari guru '{guru_dicari}' untuk dihapus...")

    # Cari input pencarian guru
    search_input = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.mantine-TextInput-input"))
    )
    search_input.clear()
    search_input.send_keys(guru_dicari)
    search_input.send_keys(Keys.RETURN)
    time.sleep(3)

    # === PERBAIKAN BAGIAN DELETE ===
    print(f"Mengklik tombol delete untuk guru '{guru_dicari}'...")

    # Cari baris guru
    row_xpath = f"//tr[.//p[contains(normalize-space(.), '{guru_dicari}')]]"
    row_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, row_xpath))
    )

    # Ambil semua tombol aksi di baris tersebut
    action_buttons = row_element.find_elements(By.XPATH, ".//button[contains(@class,'mantine-ActionIcon-root')]")
    if not action_buttons:
        raise Exception("Tombol aksi tidak ditemukan pada baris guru tersebut.")

    # Ambil tombol terakhir (biasanya delete)
    delete_button = action_buttons[-1]

    # Scroll dan klik dengan JavaScript agar pasti berhasil
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", delete_button)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", delete_button)
    print("Tombol delete berhasil diklik.")

    # Tambahkan jeda agar modal konfirmasi tampil sempurna
    time.sleep(3)

    # === KONFIRMASI DELETE ===
    print("Menunggu tombol konfirmasi 'Ya, Hapus'...")
    ya_hapus_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space(text())='Ya, Hapus']]"))
    )

    # Tambah delay sebelum klik konfirmasi
    time.sleep(2)
    driver.execute_script("arguments[0].click();", ya_hapus_button)
    print("Tombol 'Ya, Hapus' berhasil diklik.")

    # Tunggu popup konfirmasi sukses
    print("Menunggu popup konfirmasi 'berhasil' muncul...")
    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'berhasil') or contains(text(),'Berhasil') or contains(text(),'success')]"))
        )
        print("Data guru berhasil dihapus!")
    except TimeoutException:
        print("Tidak menemukan popup konfirmasi sukses setelah delete. Cek manual di halaman.")

    # Screenshot hasil
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    driver.save_screenshot(f"delete_success_{timestamp}.png")

except Exception as e:
    print(f"Terjadi error: {e}")
    timestamp_error = datetime.now().strftime("%Y%m%d_%H%M%S")
    driver.save_screenshot(f"delete_failed_{timestamp_error}.png")

finally:
    print("Menutup browser...")
    driver.quit()
