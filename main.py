import selenium.webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random

# Configuración de login (opcional)
TIKTOK_USERNAME = None  # Pon tu usuario aquí si quieres login
TIKTOK_PASSWORD = None  # Pon tu contraseña aquí si quieres login
USE_LOGIN = False  # Cambia a True si quieres usar login

print("🚀 Iniciando TikTok View Booster (versión estable con login opcional)")

def create_driver():
    try:
        print("📥 Descargando ChromeDriver automáticamente...")
        options = selenium.webdriver.ChromeOptions()
        # Quita el comentario para modo invisible: options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        options.add_argument('--window-size=1920,1080')
        
        service = Service(ChromeDriverManager().install())
        driver = selenium.webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        print("✅ Driver creado exitosamente!")
        return driver
    except Exception as e:
        print(f"❌ Error creando driver: {e}")
        print("💡 Asegúrate de tener Google Chrome instalado")
        return None

def login_tiktok(driver):
    """Login opcional a TikTok para vistas más auténticas"""
    if not USE_LOGIN or not TIKTOK_USERNAME or not TIKTOK_PASSWORD:
        print("ℹ️ Modo anónimo: No se requiere login")
        return True
    
    try:
        print("🔐 Intentando login en TikTok...")
        driver.get("https://www.tiktok.com/login")
        time.sleep(5)
        
        # Espera selector de login (puede variar)
        wait = WebDriverWait(driver, 10)
        
        # Intenta login con email/username
        username_field = wait.until(EC.element_to_be_clickable((By.NAME, "username")))
        username_field.clear()
        username_field.send_keys(TIKTOK_USERNAME)
        
        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys(TIKTOK_PASSWORD)
        
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        print("⏳ Esperando confirmación de login (5s)...")
        time.sleep(5)
        
        # Verifica si login fue exitoso (chequea URL o elementos)
        if "login" not in driver.current_url.lower():
            print("✅ Login exitoso!")
            return True
        else:
            print("⚠️ Login falló o requiere verificación adicional")
            return False
            
    except Exception as e:
        print(f"❌ Error durante login: {e}")
        print("ℹ️ Continuando en modo anónimo...")
        return False

def boost_video(driver, video_url, total_views=20, likes_target=5):
    try:
        print(f"🎥 Iniciando boost: {video_url}")
        print(f"📊 Plan: {total_views} vistas, ~{min(likes_target, total_views//5)} likes")
        
        # Navega al video
        driver.get(video_url)
        wait = WebDriverWait(driver, 15)
        time.sleep(random.uniform(3, 7))  # Carga natural
        
        liked_count = 0
        for i in range(total_views):
            print(f"\n👁️  Vista {i+1}/{total_views} ({(i/total_views*100):.0f}%) -", end=" ")
            
            # Simula comportamiento humano
            # Scroll aleatorio
            scroll_amount = random.randint(200, 1000)
            driver.execute_script(f"window.scrollTo(0, {scroll_amount});")
            
            # Watch time realista (10-40s)
            watch_time = random.uniform(10, 40)
            print(f"Watch: {watch_time:.1f}s", end=" | ")
            time.sleep(watch_time)
            
            # Opcional: like (solo 10-20% de vistas, max likes_target)
            if USE_LOGIN and likes_target > 0 and random.random() < 0.15 and liked_count < likes_target:
                try:
                    # Múltiples selectores para botón like
                    like_selectors = [
                        '[data-e2e="like-icon"]',
                        'button[aria-label*="like"]',
                        'svg[aria-label*="like"] + *',
                        '.like-button'
                    ]
                    
                    like_btn = None
                    for selector in like_selectors:
                        try:
                            like_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                            break
                        except TimeoutException:
                            continue
                    
                    if like_btn:
                        # Verifica si ya está likeado
                        is_liked = 'liked' in like_btn.get_attribute('class', '').lower() or 'selected' in like_btn.get_attribute('class', '').lower()
                        
                        if not is_liked:
                            driver.execute_script("arguments[0].click();", like_btn)
                            print("❤️ Like!", end=" | ")
                            liked_count += 1
                        else:
                            print("ℹ️ Ya likeado", end=" | ")
                    else:
                        print("❓ Like no encontrado", end=" | ")
                        
                except Exception as like_error:
                    print(f"⚠️ Like error: {str(like_error)[:30]}...", end=" | ")
            else:
                print("ℹ️ Sin like", end=" | ")
            
            # Cooldown natural (45s - 3min)
            cooldown = random.uniform(45, 180)
            print(f"Cooldown: {cooldown/60:.1f}min")
            time.sleep(cooldown)
            
            # Cada 5 vistas, simula navegación (mejora indetectabilidad)
            if (i + 1) % 5 == 0:
                print(f"🌐 Navegación natural...", end=" | ")
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(random.uniform(2, 5))
                
        print(f"\n🎉 Boost completado!")
        print(f"📈 Resultado: {total_views} vistas procesadas, {liked_count} likes dados")
        print(f"⏰ Monitorea tu video en 1-3 horas para ver el impacto")
        
    except KeyboardInterrupt:
        print("\n⏹️  Boost interrumpido por usuario")
    except Exception as e:
        print(f"\n❌ Error durante boost: {e}")
        print(f"💡 Intenta reducir total_views o verificar conexión")
    finally:
        print("\n🔄 Manteniendo sesión abierta 30s para simular comportamiento natural...")
        time.sleep(30)

if __name__ == "__main__":
    # Configuración del video
    video_url = "https://www.tiktok.com/@ejmichelotti/video/7575330510566690055"
    total_views = 25  # Empieza conservador
    likes_target = 5   # Máximo likes
    
    # Si quieres login, descomenta y configura:
    # TIKTOK_USERNAME = "tu_usuario"
    # TIKTOK_PASSWORD = "tu_contraseña"
    # USE_LOGIN = True
    
    driver = create_driver()
    if driver:
        # Login opcional
        if USE_LOGIN:
            login_success = login_tiktok(driver)
            if not login_success:
                print("⚠️ Continuando sin login...")
        
        # Boost principal
        boost_video(driver, video_url, total_views, likes_target)
        
        # Cierre limpio
        input("\n💬 Presiona ENTER para cerrar Chrome y finalizar...")
        driver.quit()
        print("👋 Sesión cerrada. ¡Buena suerte con tu video!")
    else:
        print("\n❌ No se pudo iniciar el bot. Verifica:")
        print("   1. Google Chrome instalado")
        print("   2. Conexión a internet")
        print("   3. Librerías: pip install selenium webdriver-manager")
