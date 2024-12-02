import time
import pyautogui
import pygetwindow as gw
from datetime import datetime

# Nome do programa a ser capturado
program_title = "TipChat"  # Ajuste aqui se o título da janela for diferente

# Função para localizar a janela do programa
def get_window_region(title):
    try:
        window = gw.getWindowsWithTitle(title)[0]  # Seleciona a primeira janela com o título
        return (window.left, window.top, window.width, window.height)
    except IndexError:
        print(f"Erro: Janela com título '{title}' não encontrada.")
        return None

# Iniciar o monitoramento
print(f"Tentando localizar a janela '{program_title}'...")
region = get_window_region(program_title)

if region is None:
    exit()

print(f"Janela encontrada. Monitorando a região: {region}")

while True:
    # Captura a janela específica
    screenshot = pyautogui.screenshot(region=region)
    
    # Salva o screenshot com timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"TipChat_{timestamp}.png"
    screenshot.save(filename)
    print(f"Captura salva: {filename}")
    
    # Aguarda antes de capturar novamente (ajuste o intervalo se necessário)
    time.sleep(5)
