import asyncio
from playwright.async_api import async_playwright
import random

async def gamepix_single_target():
    # URL TARGET UTAMA LU
    target_link = "https://gamesfreeonlinehub.blogspot.com/2026/01/merge-mine-idle-clicker-play-free-online.html?m=1"
    
    async with async_playwright() as p:
        # Launch browser satu kali untuk efisiensi
        browser = await p.chromium.launch(headless=True)
        
        counter = 1
        while True:
            # Ganti User Agent tiap sesi biar trafik gak dianggap bot satu device
            ua_list = [
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.105 Mobile Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            ]
            
            # Setup context sesuai identitas acak
            user = random.choice(ua_list)
            context = await browser.new_context(
                user_agent=user,
                viewport={'width': 390, 'height': 844} if "iPhone" in user or "Android" in user else {'width': 1280, 'height': 720}
            )
            page = await context.new_page()
            
            try:
                print(f"🎯 Sesi {counter} | Menyerang: {target_link[:40]}...")
                
                # 1. Buka Blogspot (Tunggu sampai konten utama muncul)
                await page.goto(target_link, wait_until="domcontentloaded", timeout=30000)
                
                # 2. Tunggu sebentar biar iframe GamePix & Iklan ke-load (7 detik)
                await asyncio.sleep(7)
                
                # 3. KLIK TENGAH (Memicu Iklan & Tombol Play GamePix)
                # Di mobile (390x844), tengahnya sekitar 195, 422
                await page.mouse.click(195, 422) 
                print("🖱️ KLIK TARGET BERHASIL!")
                
                # 4. NGETEM VALIDASI (12 - 15 detik)
                # PENTING: Jangan terlalu cepat biar Revenue masuk ke dashboard
                tunggu = random.randint(12, 15)
                await asyncio.sleep(tunggu)
                
                print(f"✅ Sesi {counter} Selesai | Ngetem {tunggu}s")
                
            except Exception as e:
                print(f"⚠️ Sesi {counter} Gagal/Timeout, skip...")
            
            # Tutup tab & sesi biar hemat RAM GitHub
            await page.close()
            await context.close()
            
            counter += 1
            # Hajar 500 sesi per satu kali jalan workflow
            if counter > 500: break 

        await browser.close()

if __name__ == "__main__":
    asyncio.run(gamepix_single_target())
                                                       
