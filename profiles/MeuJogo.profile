# Nome do Jogo (para logs e diretórios)
GAME_NAME="Palworld"

# Caminho COMPLETO para o executável principal do jogo
EXE_PATH="/mnt/games/messi/Games/Steam/steamapps/common/Palworld/Pal/Binaries/Win64/Palworld-Win64-Shipping.exe"

# Versão do Proton a ser usada (Ex: "9.0 (Beta)", "GE-Proton9-27", "Experimental")
PROTON_VERSION="GE-Proton9-27"

# Número de jogadores/instâncias
NUM_PLAYERS=2

# Resolução para CADA instância dentro do gamescope
INSTANCE_WIDTH=960
INSTANCE_HEIGHT=1080 # Ex: Para tela dividida verticalmente em um monitor 1920x1080

# Array com os caminhos dos dispositivos de controle para cada jogador
# Use 'evtest' ou olhe em /dev/input/by-id/ para encontrar os caminhos persistentes!
CONTROLLER_PATHS=(
  "/dev/input/by-id/usb-11c0_Gamesir-T4w_1.39-event-joystick" # Jogador 1
  "/dev/input/by-id/usb-Microsoft_Inc._Controller_188A6F4-event-joystick" # Jogador 2
)

# (Opcional) Argumentos adicionais para passar para o executável do jogo
GAME_ARGS="-dx12"
