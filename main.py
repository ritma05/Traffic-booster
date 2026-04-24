import time
import random
from playwright.sync_api import sync_playwright

USER_AGENTS = [
    # ✅ Chrome Desktop (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",

    # ✅ Chrome Mobile (Samsung Galaxy S21)
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",

    # ✅ Chrome Mobile (Pixel 6 Pro)
    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",

    # ✅ Firefox Desktop (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",

    # ✅ Safari Desktop (macOS Ventura)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",

    # ✅ Safari Mobile (iPhone 14 Pro)
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",

    # ✅ Edge Desktop (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",

    # ✅ Chrome Mobile (Xiaomi Android 13)
    "Mozilla/5.0 (Linux; Android 13; Mi 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",

    # ✅ Firefox Android
    "Mozilla/5.0 (Android 11; Mobile; rv:124.0) Gecko/124.0 Firefox/124.0",

    # ✅ Brave Browser Desktop (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Brave/1.48.120",

    # ✅ Firefox Desktop (macOS)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.0; rv:124.0) Gecko/20100101 Firefox/124.0",

    # ✅ Edge Mobile (Android)
    "Mozilla/5.0 (Linux; Android 12; SAMSUNG SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36 EdgA/124.0.0.0",

    # ✅ Samsung Internet Browser (Android)
    "Mozilla/5.0 (Linux; Android 12; SAMSUNG SM-G996B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/21.0 Chrome/124.0.0.0 Mobile Safari/537.36",

    # ✅ Chrome Mobile (Google Nexus 5X)
    "Mozilla/5.0 (Linux; Android 8.1.0; Nexus 5X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",

    # ✅ Firefox Mobile (iOS)
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/124.0 Mobile/15E148 Safari/605.1.15",

    # ✅ Edge Desktop (macOS)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
]


def klik_tombol_pertama(page):
    try:
        iframe1 = page.frame_locator("iframe").first
        iframe1.locator("button.gpxLoader-button").click()
        return True
    except:
        return False


def cari_dan_klik_learn_more(page):
    found = False
    teks_tombol_list = [
        "mehr", "mehr info", "weitere infos", "jetzt buchen",
        "sign up", "website", "anmelden", "zum shop",
        "abonnieren", "geschaft besuchen", "learn more", "try today"
    ]

    for percobaan in range(5):
        for frame in page.frames:
            if "gamepix.com" in frame.url:
                continue

            for teks in teks_tombol_list:
                try:
                    tombol = frame.locator(f"text=/{teks}/i")
                    count = tombol.count()
                    if count == 0:
                        continue

                    tombol_pertama = tombol.first
                    try:
                        tombol_pertama.scroll_into_view_if_needed(timeout=1000)
                    except:
                        pass

                    try:
                        box = tombol_pertama.bounding_box()
                    except:
                        box = None

                    if box:
                        try:
                            tombol_pertama.click(timeout=1500)
                            found = True
                            break
                        except:
                            try:
                                x = box["x"] + box["width"] / 2
                                y = box["y"] + box["height"] / 2
                                page.mouse.click(x, y)
                                found = True
                                break
                            except:
                                pass
                except:
                    continue
            if found:
                break
        if found:
            break
        time.sleep(2)

    return found


def run_simulasi(sesi_ke):
    print(f"\n🌐 Memulai sesi ke-{sesi_ke}...")
    user_agent = random.choice(USER_AGENTS)

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)

        context = browser.new_context(
            viewport={"width": 400, "height": 650},
            user_agent=user_agent,
            timezone_id="Europe/Berlin",
            locale="de-DE",
        )

        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
        """)

        context.clear_cookies()
        context.clear_permissions()
        context.add_init_script("localStorage.clear(); sessionStorage.clear();")

        url = "https://zonagamearca.blogspot.com/2026/04/merge-royal.html?m=1"

        page = context.new_page()
        print(f"🌐 Membuka halaman {url}")

        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)

        page.goto(url)
        tunggu = random.randint(2, 3)
        time.sleep(tunggu)

        if not klik_tombol_pertama(page):
            context.close()
            browser.close()
            print(f"⚠️ Sesi ke-{sesi_ke} gagal klik tombol pertama.")
            return

        tunggu_iklan = random.randint(20, 25)
        print(f"⏳ Menunggu sebelum deteksi iklan ({tunggu_iklan} detik)...")
        time.sleep(tunggu_iklan)

        learn_more_diklik = cari_dan_klik_learn_more(page)

        if learn_more_diklik:
            waktu_tunggu = random.randint(15, 20)
            print(f"🕒 Tombol iklan berhasil diklik. Menunggu {waktu_tunggu} detik...")
        else:
            waktu_tunggu = random.randint(0, 0)
            print(f"⚠️ Tidak ada tombol iklan. Menunggu {waktu_tunggu} detik...")

        time.sleep(waktu_tunggu)

        context.close()
        browser.close()
        print(f"✅ Sesi ke-{sesi_ke} selesai.\n")


if __name__ == "__main__":
    sesi_ke = 1
    while True:
        try:
            run_simulasi(sesi_ke)
            sesi_ke += 1
        except KeyboardInterrupt:
            print("🛑 Dihentikan oleh pengguna.")
            break
        except Exception as e:
            print(f"❌ Terjadi kesalahan pada sesi ke-{sesi_ke}: {e}")
            sesi_ke += 1
            time.sleep(2)
