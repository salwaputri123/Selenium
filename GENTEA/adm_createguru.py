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
# options.add_argument("--headless")  # aktifkan jika ingin tanpa GUI
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("🔹 Membersihkan session lama...")
    driver.delete_all_cookies()
    driver.get("about:blank")
    time.sleep(1)

    print("🔹 Membuka halaman login...")
    driver.get("https://appv3.stagingquamuslms.com/login?redirectUrl=%2F")
    driver.maximize_window()

    # Tunggu field login muncul
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@data-path='code']"))
    )

    print("🔹 Mengisi form login...")
    code = driver.find_element(By.XPATH, "//input[@data-path='code']")
    user = driver.find_element(By.XPATH, "//input[@data-path='username']")
    pw = driver.find_element(By.XPATH, "//input[@data-path='password']")

    code.clear()
    user.clear()
    pw.clear()
    time.sleep(0.5)

    code.send_keys("sdattaqwa")
    time.sleep(0.5)
    user.send_keys("admin")
    time.sleep(0.5)
    pw.send_keys("83630")

    print("🔹 Klik tombol Submit...")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    print("Menunggu dashboard terbuka...")
    WebDriverWait(driver, 40).until(
        EC.any_of(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Dashboard')]")),
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Data Pokok')]")),
        )
    )
    print("✅ Login berhasil!\n")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    time.sleep(3)

    # === Buka halaman Data Guru lewat navigasi ===
    print("🔹 Membuka menu Data Pokok...")
    menu_data_pokok = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Data Pokok')]"))
    )
    driver.execute_script("arguments[0].click();", menu_data_pokok)
    time.sleep(2)

    print("🔹 Membuka submenu Guru...")
    submenu_guru = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Guru')]"))
    )
    driver.execute_script("arguments[0].click();", submenu_guru)

    # Tunggu tombol Tambah Data muncul
    print("Menunggu halaman Data Guru terbuka...")
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Tambah Data')]"))
    )
    print("✅ Halaman Data Guru berhasil terbuka!\n")

    # === Klik tombol Tambah Data ===
    print("Klik tombol Tambah Data...")
    tambah_button = driver.find_element(By.XPATH, "//span[contains(text(),'Tambah Data')]")
    driver.execute_script("arguments[0].click();", tambah_button)

    # Tunggu form muncul
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@data-path='name']"))
    )
    print("Form tambah guru siap diisi.\n")

    # === Isi form (diperlambat sedikit agar lebih stabil) ===
    print("Mengisi form data guru (diperlambat agar stabil)...")
    nama_guru = "Budi Santoso"
    driver.find_element(By.XPATH, "//input[@data-path='name']").send_keys(nama_guru)
    time.sleep(1.5)
    driver.find_element(By.XPATH, "//input[@data-path='staff_no']").send_keys("1987654321")
    time.sleep(1.5)
    driver.find_element(By.XPATH, "//input[@data-path='resident_no']").send_keys("3210987654321098")
    time.sleep(1.5)
    driver.find_element(By.XPATH, "//input[@data-path='birth_place']").send_keys("Bandung")
    time.sleep(1.5)

    date_input = driver.find_element(By.XPATH, "//input[@data-dates-input='true']")
    date_input.clear()
    date_input.send_keys("11/11/1987")
    time.sleep(1)

    # === Klik tombol Simpan ===
    print("Klik tombol Simpan...")
    driver.find_element(By.XPATH, "//button[.//span[text()='Simpan']]").click()

    # Tunggu dialog konfirmasi muncul — dipercepat responnya
    print("Menunggu dialog konfirmasi 'Ya, Simpan' (lebih cepat)...")
    try:
        ya_button = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Ya, Simpan']"))
        )
    except TimeoutException:
        ya_button = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Ya, Ubah']"))
        )

    # Klik cepat tanpa delay
    driver.execute_script("arguments[0].click();", ya_button)
    print("Menunggu proses penyimpanan selesai...")

    WebDriverWait(driver, 25).until_not(
        EC.visibility_of_element_located((By.XPATH, "//button[.//span[text()='Simpan']]"))
    )

    print("✅ Data guru berhasil disimpan!")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    driver.save_screenshot(f"guru_disimpan_{timestamp}.png")

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