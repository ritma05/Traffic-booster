import time
import random
from playwright.sync_api import sync_playwright

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Mi 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
]

def human_behavior(page):
    # Scroll dikit biar dikira manusia asli
    try:
        page.mouse.wheel(0, random.randint(200, 500))
        time.sleep(random.randint(1, 3))
    except:
        pass

def run_simulasi(sesi_ke):
    print(f"🚀 Memulai sesi ke-{sesi_ke}...")
    ua = random.choice(USER_AGENTS)

    with sync_playwright() as p:
        # Pake Chromium (standar ads)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=ua,
            viewport={"width": 400, "height": 750},
            locale="de-DE",
            timezone_id="Europe/Berlin"
        )

        page = context.new_page()
        
        try:
            url = "https://gamesfreeonlinehub.blogspot.com/2026/02/robot-band-find-differences-free-puzzle.html?m=1"
            page.goto(url, timeout=60000)
            print(f"✅ Halaman terbuka.")
            
            # Tunggu pancingan game
            time.sleep(5)
            iframe_game = page.frame_locator("iframe").first
            if iframe_game.locator("button.gpxLoader-button").is_visible():
                iframe_game.locator("button.gpxLoader-button").click()
                print("🔘 Game button diklik.")

            # Tunggu iklan muncul
            print("⏳ Menunggu iklan muncul...")
            time.sleep(random.randint(15, 20))
            human_behavior(page)

            # --- LOGIKA CARI IKLAN ---
            teks_tombol_list = [
                "mehr", "mehr info", "weitere infos", "jetzt buchen",
                "sign up", "website", "anmelden", "zum shop",
                "abonnieren", "learn more", "try today", "visit site", "open"
            ]

            found = False
            for frame in page.frames:
                if "gamepix.com" in frame.url: continue 

                for teks in teks_tombol_list:
                    try:
                        tombol = frame.locator(f"text=/{teks}/i").first
                        if tombol.is_visible():
                            box = tombol.bounding_box()
                            if box:
                                # Klik tengah tombol
                                page.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
                                found = True
                                print(f"💰 KLIK BERHASIL: [{teks}]")
                                break
                    except:
                        continue
                if found: break

            # --- DURASI STAY (30 DETIK) ---
            if found:
                # Durasi sesuai permintaan (30-35 detik biar gak kaku)
                stay = random.randint(30, 35)
                print(f"🕒 Stay di iklan selama {stay} detik...")
                time.sleep(stay)
            else:
                print("⚠️ Iklan tidak ditemukan di sesi ini.")

        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            browser.close()
            print(f"✅ Sesi {sesi_ke} selesai.\n")

if __name__ == "__main__":
    # Sekali jalan di GitHub, dia akan running 4 sesi bergantian
    for i in range(1, 5):
        run_simulasi(i)
        time.sleep(random.randint(5, 10))
          
