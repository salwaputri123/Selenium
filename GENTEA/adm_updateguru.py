import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

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
    time.sleep(2)

    # === UPDATE DATA GURU ===
    print("Memulai proses update data guru...")

    driver.get("https://appv3.stagingquamuslms.com/school/teacher")
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Tambah Data')]"))
    )
    print("Halaman Data Guru siap.")

    guru_dicari = "Ahmad Fauzan"
    print(f"Mencari guru '{guru_dicari}' untuk diupdate...")

    search_input = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.mantine-TextInput-input"))
    )
    search_input.clear()
    search_input.send_keys(guru_dicari)
    search_input.send_keys(Keys.RETURN)
    time.sleep(3)

    # Klik tombol edit
    print(f"Mengklik tombol edit untuk guru '{guru_dicari}'...")
    edit_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                f"//td[contains(., '{guru_dicari}')]/following-sibling::td//button[contains(@class, 'mantine-ActionIcon-root')]",
            )
        )
    )
    driver.execute_script("arguments[0].click();", edit_button)
    print("Tombol edit berhasil diklik.")

    # Tunggu form edit muncul
    print("Menunggu form edit muncul...")
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@data-path='birth_place']"))
    )
    print("Form edit sudah muncul.")

    # Edit data Tempat Lahir
    print("Mengubah data Tempat Lahir...")
    tempat_lahir_baru = "Jakarta"
    tempat_lahir_field = driver.find_element(By.XPATH, "//input[@data-path='birth_place']")
    tempat_lahir_field.clear()
    tempat_lahir_field.send_keys(tempat_lahir_baru)
    time.sleep(1)

    # Edit data Tanggal Lahir
    print("Mengubah data Tanggal Lahir...")
    tanggal_lahir_baru = "1990-01-15"
    tanggal_lahir_field = driver.find_element(By.XPATH, "//input[@data-dates-input='true']")
    tanggal_lahir_field.clear()
    tanggal_lahir_field.send_keys(tanggal_lahir_baru)
    time.sleep(1)

    # Klik tombol "Simpan" lalu konfirmasi "Ya, Ubah"
    print("Mengklik tombol 'Simpan' dan konfirmasi 'Ya, Ubah'...")

    simpan_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[contains(text(),'Simpan')]]")
        )
    )
    driver.execute_script("arguments[0].click();", simpan_button)
    time.sleep(2)

    # Klik tombol "Ya, Ubah" di popup konfirmasi
    ya_ubah_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(),'Ya, Ubah')]")
        )
    )
    driver.execute_script("arguments[0].click();", ya_ubah_button)
    print("Tombol 'Ya, Ubah' berhasil diklik.")

    # Tunggu popup konfirmasi sukses
    print("Menunggu popup konfirmasi sukses...")
    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(text(),'berhasil') or contains(text(),'success')]",
                )
            )
        )
        print("Update data guru berhasil disimpan!")
    except TimeoutException:
        print("Tidak menemukan popup konfirmasi sukses.")

    # Screenshot hasil
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    driver.save_screenshot(f"update_success_{timestamp}.png")

except Exception as e:
    print(f"Terjadi error: {e}")
    timestamp_error = datetime.now().strftime("%Y%m%d_%H%M%S")
    driver.save_screenshot(f"test_failed_{timestamp_error}.png")
finally:
    print("Menutup browser...")
    driver.quit()
