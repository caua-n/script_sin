import pygetwindow as gw
import mss
import mss.tools
import time
from datetime import datetime
import hashlib

# Nome exato do programa a ser monitorado
program_title = "Spotify Premium"

# Região específica dentro da janela (x_offset, y_offset, largura, altura)
specific_region = (400, 550, 500, 450)

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
    return hashlib.md5(image.rgb).hexdigest()

# Localiza a janela do programa
print(f"Tentando localizar a janela '{program_title}'...")
region = get_window_region(program_title)

if region is None:
    exit(f"Janela do programa '{program_title}' não encontrada.")

# Calcula a região ajustada para a área específica da janela
adjusted_region = {
    "top": region[1] + specific_region[1],  # Coordenada Y ajustada
    "left": region[0] + specific_region[0],  # Coordenada X ajustada
    "width": specific_region[2],  # Largura
    "height": specific_region[3],  # Altura
}

print(f"Janela encontrada. Monitorando a região específica: {adjusted_region}")

# Inicializa o hash anterior para detectar mudanças
previous_hash = None

# Loop para capturar a região apenas quando houver alteração
while True:
    try:
        with mss.mss() as sct:
            # Captura a região ajustada
            screenshot = sct.grab(adjusted_region)

            # Calcula o hash do screenshot atual
            current_hash = calculate_image_hash(screenshot)

            # Verifica se houve alteração
            if current_hash != previous_hash:
                print("Mudança detectada na região específica!")
                
                # Atualiza o hash anterior
                previous_hash = current_hash

                # Salva o screenshot com timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                screenshot_filename = f"Region_{timestamp}.png"
                mss.tools.to_png(screenshot.rgb, screenshot.size, output=screenshot_filename)
                print(f"Captura salva: {screenshot_filename}")
            else:
                print("Nenhuma mudança detectada.")

        # Aguarda antes de verificar novamente
        time.sleep(2)

    except Exception as e:
        print(f"Erro durante a captura: {e}")
