import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import requests

# Lista de proxies gratuitos de prueba (obtén más frescos de free-proxy-list.net)
PROXIES = [
    'http://proxy1:port',  # Reemplaza con proxies reales HTTP
    'http://proxy2:port',
    # Agrega 10-20 más para rotación
]

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
]

def get_working_proxy():
    # Función simple para chequear proxy (usa uno válido o None)
    for proxy in PROXIES:
        try:
            requests.get('https://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=5)
            return proxy
        except:
            continue
    return None  # Sin proxy si fallan

def create_driver(proxy=None):
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(f'--user-agent={random.choice(USER_AGENTS)}')
    options.add_argument('--window-size=1920,1080')
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
    driver = uc.Chrome(options=options, version_main=None)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def boost_session(driver, video_url, views_in_session=50, likes_per_session=10):
    try:
        print(f"Sesión iniciada: {views_in_session} vistas para {video_url}")
        driver.get(video_url)
        wait = WebDriverWait(driver, 15)
        time.sleep(random.uniform(5, 10))  # Carga inicial
        
        liked_count = 0
        for i in range(views_in_session):
            # Vista orgánica: scroll + pausa larga (simula watch completo)
            driver.execute_script(f"window.scrollTo(0, {random.randint(200, 800)});")
            watch_time = random.uniform(15, 45)  # 15-45s de "visualización" real
            time.sleep(watch_time)
            print(f"Vista {i+1}/{views_in_session} - Watch time: {watch_time:.1f}s")
            
            # Like aleatorio (no en todas las vistas)
            if likes_per_session > 0 and random.random() < 0.2 and liked_count < likes_per_session:  # 20% chance
                try:
                    like_selectors = ['[data-e2e="like-icon"]', 'button[aria-label*="like"]']
                    like_btn = None
                    for sel in like_selectors:
                        try:
                            like_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, sel)))
                            break
                        except:
                            continue
                    if like_btn and 'selected' not in like_btn.get_attribute('class', ''):
                        like_btn.click()
                        print(f"Like {liked_count+1} agregado")
                        liked_count += 1
                except:
                    pass
            
            # Cooldown natural (1-3 min, simula usuario navegando)
            cooldown = random.uniform(60, 180)
            print(f"Cooldown: {cooldown/60:.1f} min")
            time.sleep(cooldown)
        
        print("Sesión completada.")
    except Exception as e:
        print(f"Error en sesión: {e}")
    finally:
        driver.quit()

def run_daily_boost(video_url, total_views=500, sessions_per_day=5):
    views_per_session = total_views // sessions_per_day
    proxy = get_working_proxy()
    
    for session in range(sessions_per_day):
        print(f"\n--- Sesión {session+1}/{sessions_per_day} ---")
        driver = create_driver(proxy)
        likes_this_session = random.randint(5, 15)  # Aleatorio para naturalidad
        boost_session(driver, video_url, views_per_session, likes_this_session)
        
        # Break entre sesiones (1-2h para simular uso diario)
        if session < sessions_per_day - 1:
            break_time = random.uniform(3600, 7200)  # 1-2h
            print(f"Break hasta próxima sesión: {break_time/3600:.1f}h")
            time.sleep(break_time)  # En producción, usa scheduler como cron para pausas largas

# Configuración para tu video
if __name__ == "__main__":
    video_url = "https://www.tiktok.com/@ejmichelotti/video/7575330510566690055"
    total_daily_views = 500  # Escala aquí (empieza con 100 para test)
    sessions = 5  # Divide en 5 sesiones de ~100 vistas cada una
    run_daily_boost(video_url, total_daily_views, sessions)
    print("Boost diario completado. Monitorea views en 24h.")