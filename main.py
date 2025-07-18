import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Bot, TelegramError
import logging
from datetime import datetime
import random

# Configuração
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vfs_monitor.log'),
        logging.StreamHandler()
    ]
)

def load_config():
    try:
        with open('config.json') as f:
            config = json.load(f)
            if not all(key in config for key in ['telegram_token', 'chat_id']):
                raise ValueError("Configurações incompletas no config.json")
            return config
    except Exception as e:
        logging.error(f"Erro ao carregar configurações: {e}")
        exit(1)

config = load_config()
TELEGRAM_TOKEN = config["telegram_token"]
CHAT_ID = config["chat_id"]
VFS_URL = "https://visa.vfsglobal.com/ago/pt/prt/application-detail"

def send_alert(available: bool, screenshot_path=None):
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        if available:
            message = f"🚨 *VAGAS ABERTAS!* 🚨\nData: {timestamp}\n[Agende agora!]({VFS_URL})"
            if screenshot_path:
                with open(screenshot_path, 'rb') as photo:
                    bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=message, parse_mode="Markdown")
            else:
                bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
            
            logging.info("Notificação de vagas abertas enviada")
        # Removido o envio de mensagens quando está fechado
            
    except TelegramError as e:
        logging.error(f"Erro no Telegram: {e}")
    except Exception as e:
        logging.error(f"Erro inesperado ao enviar alerta: {e}")

def check_slots():
    driver = None
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        logging.info("Acessando página da VFS Global...")
        driver.get(VFS_URL)
        time.sleep(5 + random.uniform(0, 3))  # Espera aleatorizada
        
        page_text = driver.page_source.lower()
        
        closed_conditions = [
            "não há horários disponíveis",
            "lamentamos, mas no momento",
            "no appointments available",
            "agendamento indisponível",
            "tente novamente mais tarde",
            "horários esgotados",
            "indisponível no momento"
        ]
        
        open_conditions = [
            "selecione o horário",
            "agendar agora",
            "book appointment",
            "selecione o centro de atendimento",
            "escolha a data",
            "disponível para agendamento"
        ]
        
        try:
            driver.find_element(By.XPATH, "//button[contains(text(), 'Agendar')]")
            open_conditions.append("elemento_agendar_encontrado")
        except:
            pass
            
        is_closed = any(cond in page_text for cond in closed_conditions)
        is_open = any(cond in page_text for cond in open_conditions)
        
        if is_open and not is_closed:
            logging.info("VAGAS ABERTAS - Condições positivas encontradas")
            screenshot_path = f"vfs_open_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            driver.save_screenshot(screenshot_path)
            return True, screenshot_path
        return False, None
            
    except Exception as e:
        logging.error(f"Erro durante a verificação: {e}")
        return False, None
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    logging.info("Iniciando monitoramento VFS Global Angola-Portugal")
    send_alert(False)  # Mensagem inicial de boas-vindas
    
    try:
        last_status = None
        while True:
            current_status, screenshot_path = check_slots()
            
            if current_status and (last_status != current_status):
                send_alert(current_status, screenshot_path)
            
            last_status = current_status if current_status else last_status
            
            # Intervalo fixo de 2 minutos com pequena variação aleatória
            wait_time = 120 + random.uniform(0, 15)  # 2-2.25 minutos
            logging.info(f"Próxima verificação em ~{int(wait_time//60)} minutos")
            time.sleep(wait_time)
            
    except KeyboardInterrupt:
        logging.info("Monitoramento encerrado pelo usuário")
    except Exception as e:
        logging.error(f"Erro fatal: {e}")
        send_alert(False)  # Notifica falha do sistema
