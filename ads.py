import time
import random
from playwright.sync_api import sync_playwright

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Mi 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Android 11; Mobile; rv:124.0) Gecko/124.0 Firefox/124.0"
]

def klik_tombol_pertama(page):
    try:
        iframe1 = page.frame_locator("iframe").first
        iframe1.locator("button.gpxLoader-button").click(timeout=5000)
        return True
    except:
        return False

def cari_dan_klik_learn_more(page):
    found = False
    teks_tombol_list = [
        "learn more", "open", "visit", "install", "try today",
        "sign up", "website", "selengkapnya", "daftar", "shop now"
    ]
    for percobaan in range(5):
        for frame in page.frames:
            if "gamepix.com" in frame.url: continue
            for teks in teks_tombol_list:
                try:
                    tombol = frame.locator(f"text=/{teks}/i").first
                    if tombol.is_visible():
                        tombol.click(timeout=2000)
                        found = True
                        break
                except: continue
            if found: break
        if found: break
        time.sleep(2)
    return found

def run_simulasi(sesi_ke):
    print(f"\n🌐 Memulai sesi ke-{sesi_ke}...")
    user_agent = random.choice(USER_AGENTS)
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(viewport={"width": 400, "height": 700}, user_agent=user_agent)
        
        # Anti-bot
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        url = "https://gamesfreeonlinehub.blogspot.com/2026/01/body-drop-3d-play-free-online.html?m=1"
        page = context.new_page()
        
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(3)
            
            if not klik_tombol_pertama(page):
                print("⚠️ Gagal klik tombol play, lanjut scan iklan.")

            time.sleep(random.randint(12, 16)) # Tunggu iklan muncul
            
            if cari_dan_klik_learn_more(page):
                # KUNCI REVENUE: Ngetem lama biar Dollar valid
                waktu_tunggu = random.randint(35, 50) 
                print(f"💰 Iklan diklik! Ngetem {waktu_tunggu} detik...")
            else:
                waktu_tunggu = random.randint(5, 10)
                print(f"⚠️ Iklan gak ketemu, ngetem bentar ({waktu_tunggu}s)")

            time.sleep(waktu_tunggu)
        except Exception as e:
            print(f"❌ Error: {e}")
        
        context.close()
        browser.close()
        print(f"✅ Sesi ke-{sesi_ke} selesai.")

if __name__ == "__main__":
    sesi_ke = 1
    while True:
        try:
            run_simulasi(sesi_ke)
            sesi_ke += 1
            time.sleep(random.randint(2, 5))
        except:
            time.sleep(10)
      
