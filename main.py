import pygetwindow as gw
import mss
import mss.tools
import time
from datetime import datetime
import hashlib
from telegram import Bot
import asyncio

TELEGRAM_BOT_TOKEN = "7629868246:AAGEhjVGuuIgEWdagRtc34etB-351VMvDDM"
CHAT_ID = "-4790240031" 
bot = Bot(token=TELEGRAM_BOT_TOKEN)

program_title = "TipChat"

specific_region = (400, 550, 500, 450)

def get_window_region(title):
    try:
        windows = gw.getWindowsWithTitle(title)
        if not windows:
            raise IndexError(f"Nenhuma janela encontrada com título '{title}'")
        window = windows[0]
        window.activate()
        return (window.left, window.top, window.width, window.height)
    except IndexError as e:
        print(f"Erro: {e}")
        return None

def calculate_image_hash(image):
    return hashlib.md5(image.rgb).hexdigest()

async def send_screenshot_to_telegram(file_path):
    try:
        with open(file_path, "rb") as file:
            await bot.send_document(chat_id=CHAT_ID, document=file, caption="Mudança detectada na região específica!")
            print(f"Screenshot enviado para o Telegram: {file_path}")
    except Exception as e:
        print(f"Erro ao enviar para o Telegram: {e}")

print(f"Tentando localizar a janela '{program_title}'...")
region = get_window_region(program_title)

if region is None:
    exit(f"Janela do programa '{program_title}' não encontrada.")

adjusted_region = {
    "top": region[1] + specific_region[1],  
    "left": region[0] + specific_region[0], 
    "width": specific_region[2],
    "height": specific_region[3], 
}

print(f"Janela encontrada. Monitorando a região específica: {adjusted_region}")


previous_hash = None


async def main():
    global previous_hash
    while True:
        try:
            with mss.mss() as sct:

                screenshot = sct.grab(adjusted_region)

                current_hash = calculate_image_hash(screenshot)

                if current_hash != previous_hash:
                    print("Mudança detectada na região específica!")
                    
  
                    previous_hash = current_hash

    
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    screenshot_filename = f"Region_{timestamp}.png"
                    mss.tools.to_png(screenshot.rgb, screenshot.size, output=screenshot_filename)
                    print(f"Captura salva: {screenshot_filename}")

             
                    await send_screenshot_to_telegram(screenshot_filename)
                else:
                    print("Nenhuma mudança detectada.")

           
            time.sleep(2)

        except Exception as e:
            print(f"Erro durante a captura: {e}")


if __name__ == "__main__":
    asyncio.run(main())
