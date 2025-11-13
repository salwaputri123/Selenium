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
# options.add_argument("--headless")  # Uncomment jika ingin tanpa GUI
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("Membuka halaman login...")
    driver.get("https://appv3.stagingquamuslms.com/login?redirectUrl=%2F")
    driver.maximize_window()
    time.sleep(2)

    # Tunggu field login muncul
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@data-path='code']"))
    )

    # === LOGIN ===
    driver.find_element(By.XPATH, "//input[@data-path='code']").clear()
    driver.find_element(By.XPATH, "//input[@data-path='code']").send_keys("quamus")
    time.sleep(1)

    driver.find_element(By.XPATH, "//input[@data-path='username']").clear()
    driver.find_element(By.XPATH, "//input[@data-path='username']").send_keys("superadmin")
    time.sleep(1)

    driver.find_element(By.XPATH, "//input[@data-path='password']").clear()
    driver.find_element(By.XPATH, "//input[@data-path='password']").send_keys(
        "bEz81Z1hzLdy2uJrwunBavzwKWIdKwRZS5Etij4yS0hJm"
    )
    time.sleep(1)

    print("Klik tombol Submit...")
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    submit_button.click()

    print("Menunggu proses login selesai...")
    time.sleep(3)

    WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Superadmin') or contains(text(),'Selamat Datang') or contains(text(),'Aplikasi QuamusLMS')]"))
    )
    print("Login berhasil!")

    # === DELETE DATA GURU ===
    print("Memulai proses delete data guru...")

    driver.get("https://appv3.stagingquamuslms.com/school/teacher")
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Tambah Data')]"))
    )
    print("Halaman Data Guru siap.")

    guru_dicari = "Galih Putra"
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
