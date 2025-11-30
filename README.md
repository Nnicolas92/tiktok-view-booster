# TikTok Safe View Booster

Bot para boostear vistas de videos TikTok de forma segura usando undetected-chromedriver.

## Instalación

1. Clona el repo: `git clone https://github.com/Nnicolas92/tiktok-view-booster`
2. Instala dependencias: `pip install -r requirements.txt`
3. Edita main.py con tu URL de video
4. Ejecuta: `python main.py`

## Configuración

- Cambia `video_url` en main.py
- Ajusta `total_daily_views` (recomendado: 100-200/día)
- Para 500+ vistas, configura proxies en PROXIES list

## Anti-ban

- Delays aleatorios 1-3 min
- User-agents rotativos
- Sesiones distribuidas
- Max 20% likes por vistas

**Nota**: Usa con responsabilidad. TikTok puede detectar patrones agresivos.

## Troubleshooting

Si `ModuleNotFoundError: undetected_chromedriver`:

1. **Virtual environment (recomendado)**:
```powershell
cd tiktok-view-booster
python -m venv tiktok_env
tiktok_env\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

2. **Instalación manual**:
```powershell
pip uninstall undetected-chromedriver selenium requests -y
pip cache purge
pip install --no-cache-dir undetected-chromedriver selenium requests
```

3. **Verificar instalación**:
```powershell
pip list | findstr -i "undetected selenium requests"
```

4. **Si persiste, usa webdriver-manager** (ver alternativa abajo)

## Alternativa: Versión con webdriver-manager

Si undetected-chromedriver falla, reemplaza en main.py:

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Reemplaza create_driver() con:
def create_driver(proxy=None):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver
```

Y agrega a requirements.txt:
```
webdriver-manager
```