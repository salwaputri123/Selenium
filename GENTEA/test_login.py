import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("Membuka halaman login...")
    driver.get("https://appv3.stagingquamuslms.com/login?redirectUrl=%2F")
    driver.maximize_window()
    time.sleep(2) 

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@data-path='code']"))
    )

    # Isi field login
    field_code = driver.find_element(By.XPATH, "//input[@data-path='code']")
    field_code.clear()
    field_code.send_keys("quamus")
    time.sleep(1)

    field_user = driver.find_element(By.XPATH, "//input[@data-path='username']")
    field_user.clear()
    field_user.send_keys("superadmin")
    time.sleep(1)

    field_pass = driver.find_element(By.XPATH, "//input[@data-path='password']")
    field_pass.clear()
    field_pass.send_keys("bEz81Z1hzLdy2uJrwunBavzwKWIdKwRZS5Etij4yS0hJm")
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
    time.sleep(2)  # kasih waktu sebelum screenshot

    print("Login berhasil! Dashboard terdeteksi.")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"login_success_{timestamp}.png"
    driver.save_screenshot(filename)
    print(f"Screenshot login berhasil disimpan sebagai '{filename}'")

except Exception as e:
    print(f"Terjadi error: {e}")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"login_failed_{timestamp}.png"
    driver.save_screenshot(filename)
    print(f"Screenshot disimpan sebagai '{filename}'")
finally:
    time.sleep(2)
    print("Menutup browser...")
    driver.quit()
