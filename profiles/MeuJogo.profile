# Nome do Jogo
GAME_NAME="Meu Jogo Incrível com InputPlumber"

# Caminho do Executável
EXE_PATH="/path/to/your/steamapps/common/Meu Jogo Incrível/Binaries/Win64/MeuJogo-Win64-Shipping.exe"

# Versão do Proton
PROTON_VERSION="GE-Proton8-25"

# Número de jogadores/instâncias
NUM_PLAYERS=2

# Resolução por instância
INSTANCE_WIDTH=960
INSTANCE_HEIGHT=1080

# --- Configuração InputPlumber ---
# Nome base para os dispositivos virtuais que serão criados
# (Resultará em: virtual-gamepad-p1, virtual-gamepad-p2)
VIRTUAL_DEVICE_BASENAME="virtual-gamepad-p"

# Array com identificadores PERSISTENTES dos controles FÍSICOS
# Use caminhos de /dev/input/by-id/* ou nomes/IDs únicos
PLAYER_PHYSICAL_DEVICE_IDS=(
  "/dev/input/by-id/usb-Sony_Interactive_Entertainment_Wireless_Controller-event-joystick" # Jogador 1
  "/dev/input/by-id/usb-Microsoft_X-Box_360_pad_12345678-event-joystick" # Jogador 2
)
# Garantir que a ordem aqui corresponda à ordem dos jogadores

# (Opcional) Argumentos do jogo
# GAME_ARGS="-nologin"
