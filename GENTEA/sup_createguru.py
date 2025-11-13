import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

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

    # Klik tombol Tambah Data
    print("Klik tombol Tambah Data...")
    driver.find_element(By.XPATH, "//*[contains(text(),'Tambah Data')]").click()
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@data-path='name']"))
    )
    time.sleep(1)

    # Isi form data guru
    print("Mengisi data guru...")
    driver.find_element(By.XPATH, "//input[@data-path='name']").send_keys("Budi Santoso")
    time.sleep(0.5)
    driver.find_element(By.XPATH, "//input[@data-path='staff_no']").send_keys("1987654321")
    time.sleep(0.5)
    driver.find_element(By.XPATH, "//input[@data-path='resident_no']").send_keys("3210987654321098")
    time.sleep(0.5)
    driver.find_element(By.XPATH, "//input[@data-path='birth_place']").send_keys("Bandung")
    time.sleep(0.5)
    date_input = driver.find_element(By.XPATH, "//input[@data-dates-input='true']")
    date_input.clear()
    date_input.send_keys("11/11/1987")
    time.sleep(0.5)

    # Klik tombol Simpan pertama kali
    print("Klik tombol Simpan...")
    driver.find_element(By.XPATH, "//button[.//span[text()='Simpan']]").click()

    # Tunggu dialog konfirmasi muncul
    print("Menunggu dialog konfirmasi...")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[.//span[text()='Ya, Simpan']]"))
    )
    print("Klik tombol 'Ya, Simpan' pada dialog konfirmasi...")
    driver.find_element(By.XPATH, "//button[.//span[text()='Ya, Simpan']]").click()
    
    print("Menunggu proses penyimpanan selesai...")
    WebDriverWait(driver, 30).until_not(
        EC.visibility_of_element_located((By.XPATH, "//button[.//span[text()='Simpan']]"))
    )
    print("Data guru berhasil disimpan!")
    success_ss = f"guru_saved_{timestamp}.png"
    driver.save_screenshot(success_ss)
    print(f"Screenshot setelah Simpan disimpan sebagai '{success_ss}'")

    # ======== Cari Data yang Baru Ditambahkan ========
    print("Mencari data 'Budi Santoso' di kolom pencarian...")
    try:
        search_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.mantine-TextInput-input"))
        )
        search_input.clear()
        search_input.send_keys("Budi Santoso")
        print("Pencarian dilakukan.")
        time.sleep(2)
    except TimeoutException:
        print("Kolom pencarian tidak ditemukan atau tidak bisa diklik dalam 10 detik.")
        raise Exception("Gagal menemukan kolom pencarian.")

    print("Melakukan validasi akhir: Memeriksa apakah data guru muncul di tabel hasil pencarian...")
    try:
        teacher_name_in_table = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//td[contains(., 'Budi Santoso')]"))
        )
        if teacher_name_in_table:
            print("Validasi BERHASIL: Data 'Budi Santoso' ditemukan di tabel hasil pencarian!")
            validation_ss = f"validation_success_{timestamp}.png"
            driver.save_screenshot(validation_ss)
            print(f"Screenshot bukti validasi disimpan sebagai '{validation_ss}'")

    except TimeoutException:
        print("Validasi GAGAL: Data 'Budi Santoso' tidak ditemukan di tabel setelah pencarian.")
        fail_validation_ss = f"validation_failed_{timestamp}.png"
        driver.save_screenshot(fail_validation_ss)
        print(f"Screenshot kegagalan validasi disimpan sebagai '{fail_validation_ss}'")
        raise Exception("Validasi penambahan data guru gagal.")

except Exception as e:
    print(f"Terjadi error: {e}")
    timestamp_error = datetime.now().strftime("%Y%m%d_%H%M%S")
    fail_ss = f"test_failed_{timestamp_error}.png"
    driver.save_screenshot(fail_ss)
    print(f"Screenshot error disimpan sebagai '{fail_ss}'")
finally:
    time.sleep(2)
    print("Menutup browser...")
    driver.quit()