import time
import random
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        # Menggunakan chromium karena sudah diinstal di main.yml
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1"
        )
        
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        try:
            print("--- Membuka situs ---")
            page.goto("https://zonagamearca.blogspot.com/2026/04/merge-royal.html?m=1", timeout=90000)
            
            time.sleep(random.uniform(20, 25))
            
            clicked = False
            for frame in page.frames:
                # Selector yang mencakup iklan adsense dan lainnya
                target = frame.locator("button, [aria-label*='Ad'], .adsbygoogle, [id*='ad']")
                
                if target.count() > 0:
                    try:
                        target.first.click(timeout=3000)
                        print("✅ Iklan diklik! Menunggu 15 detik...")
                        time.sleep(15) 
                        clicked = True
                        break 
                    except:
                        continue
            
            if not clicked:
                print("⚠️ Tidak ada iklan yang terdeteksi.")
            else:
                print("--- Sesi selesai setelah stay 15 detik ---")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
