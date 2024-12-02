import time
import pyautogui
import pygetwindow as gw
from pytesseract import pytesseract
from datetime import datetime
import hashlib

# Configuração do Tesseract OCR
pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Nome exato do programa a ser monitorado
program_title = "TipChat"

# Coordenadas da região específica (definida a partir da imagem do segundo print)
specific_region = (400, 550, 500, 450)  # (x, y, largura, altura) -> ajustar conforme necessário

# Função para localizar a região da janela do programa
def get_window_region(title):
    try:
        windows = gw.getWindowsWithTitle(title)
        if not windows:
            raise IndexError(f"Nenhuma janela encontrada com título '{title}'")
        window = windows[0]
        # Ativa a janela para garantir visibilidade
        window.activate()
        return (window.left, window.top, window.width, window.height)
    except IndexError as e:
        print(f"Erro: {e}")
        return None

# Função para calcular o hash de uma imagem
def calculate_image_hash(image):
    image_bytes = image.tobytes()
    return hashlib.md5(image_bytes).hexdigest()

# Localiza a janela do TipChat
print(f"Tentando localizar a janela '{program_title}'...")
region = get_window_region(program_title)

if region is None:
    exit("Janela do TipChat não encontrada.")

# Ajusta a região para a área específica da tela
adjusted_region = (
    region[0] + specific_region[0],  # x ajustado
    region[1] + specific_region[1],  # y ajustado
    specific_region[2],  # Largura
    specific_region[3],  # Altura
)

print(f"Janela encontrada. Monitorando a região específica: {adjusted_region}")

# Inicializa o hash anterior para detectar mudanças
previous_hash = None

while True:
    try:
        # Captura apenas a região específica
        screenshot = pyautogui.screenshot(region=adjusted_region)

        # Calcula o hash da captura atual
        current_hash = calculate_image_hash(screenshot)

        # Verifica se algo mudou na tela
        if current_hash != previous_hash:
            print("Mudança detectada na região específica! Capturando dados...")
            
            # Atualiza o hash anterior
            previous_hash = current_hash

            # Salva o screenshot com timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_filename = f"Region_{timestamp}.png"
            screenshot.save(screenshot_filename)
            print(f"Captura salva: {screenshot_filename}")
            
            # Realiza OCR na imagem capturada
            extracted_text = pytesseract.image_to_string(screenshot, lang="por")
            
            # Salva o texto extraído em um arquivo .txt
            text_filename = f"Region_{timestamp}.txt"
            with open(text_filename, "w", encoding="utf-8") as text_file:
                text_file.write(extracted_text)
            print(f"Texto extraído salvo em: {text_filename}")
        else:
            print("Nenhuma mudança detectada na região específica.")
        
        # Aguarda antes de verificar novamente
        time.sleep(2)

    except Exception as e:
        print(f"Erro durante a execução: {e}")
