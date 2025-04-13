#!/bin/bash

# Edite esse caminho para o arquivo de perfil do seu jogo
PROFILE_FILE="/home/mallor/Documentos/GitHub/Linux-Coop/profiles/Palworld"

# Verificar se o arquivo de perfil existe
if [ ! -f "$PROFILE_FILE" ]; then
  echo "Erro: O arquivo de perfil ($PROFILE_FILE) não foi encontrado. Execute o Create_new_profile.sh primeiro."
  exit 1
fi

# Carregar as configurações do arquivo de perfil
source "$PROFILE_FILE"

# Verificar se as variáveis obrigatórias foram definidas
required_vars=("EXE_PATH" "PROTON_VERSION" "WIDTH" "HEIGHT")
for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    echo "Erro: A variável $var não está definida no arquivo de perfil."
    exit 1
  fi
done

# Verificar se o arquivo executável existe
if [ ! -f "$EXE_PATH" ]; then
  echo "Erro: O arquivo executável não existe: $EXE_PATH"
  exit 1
fi

# Extrair o nome do executável sem o caminho
EXE_NAME=$(basename "$EXE_PATH")

# Verificar se o gamescope está instalado
if ! command -v gamescope &> /dev/null; then
  echo "Erro: Gamescope não está instalado. Instale com: sudo apt install gamescope"
  exit 1
fi

# Verificar se o Steam está em execução
start_steam_if_needed() {
  if ! pgrep -x "steam" > /dev/null; then
    echo "Aviso: Steam não está em execução. Iniciando..."
    steam -silent &
    local attempts=0
    while [ $attempts -lt 5 ] && ! pgrep -x "steam" > /dev/null; do
      sleep 2
      ((attempts++))
    done
    if [ $attempts -eq 5 ]; then
      echo "Erro: Falha ao iniciar o Steam."
      exit 1
    fi
  fi
}
start_steam_if_needed

# Função aprimorada para encontrar o Proton
find_proton_path() {
  local version=$1
  local steam_paths=(
    "$HOME/.steam/steam"
    "$HOME/.local/share/Steam"
    "$HOME/.steam/debian-installation"
    "/var/mnt/games/messi/Games/Steam"
  )

  for steam_path in "${steam_paths[@]}"; do
    if [ -d "$steam_path" ]; then
      # Procurar Proton Experimental
      if [[ "$version" == "Experimental" ]]; then
        local experimental_path="$steam_path/steamapps/common/Proton - Experimental/proton"
        [ -f "$experimental_path" ] && echo "$experimental_path" && return
      fi

      # Procurar versões numeradas
      local proton_path="$steam_path/steamapps/common/Proton $version/proton"
      [ -f "$proton_path" ] && echo "$proton_path" && return

      # Procurar GE-Proton
      if [[ "$version" == GE-Proton* ]]; then
        local ge_path="$steam_path/compatibilitytools.d/$version/proton"
        [ -f "$ge_path" ] && echo "$ge_path" && return
      fi
    fi
  done

  echo "Erro: Proton $version não encontrado." >&2
  exit 1
}

PROTON_PATH=$(find_proton_path "$PROTON_VERSION")

# Configurações de controle
CONTROLLER_DIR="./controller_config/"
mkdir -p "$CONTROLLER_DIR"

# Verificar arquivos de controle e mapeamento
for player in 1 2; do
  # Verificar dispositivo físico
  controller_file="${CONTROLLER_DIR}/Player${player}_Controller"
  if [ ! -f "$controller_file" ]; then
    echo "Erro: Arquivo de controle não encontrado: $controller_file"
    echo "Crie com: sudo evdev-joystick --evdev /dev/input/eventX --name Player${player}_Controller --device /dev/input/js$((player-1))"
    exit 1
  fi

  # Verificar mapeamento SDL
  mapping_file="${CONTROLLER_DIR}/Player${player}_mapping.cfg"
  if [ ! -f "$mapping_file" ]; then
    echo "Erro: Arquivo de mapeamento não encontrado: $mapping_file"
    echo "Crie um arquivo com o layout do seu controle usando o formato SDL_GAMECONTROLLERCONFIG"
    exit 1
  fi
done

# Função de inicialização do jogo com isolamento de controles
launch_game_instance() {
  local instance_num=$1
  local controller_file=$2
  local joy_device=$(<"$controller_file")
  local prefix_dir="$HOME/.proton_prefixes/${EXE_NAME}_instance_${instance_num}"

  mkdir -p "$prefix_dir" || {
    echo "Erro ao criar prefixo em: $prefix_dir"
    exit 1
  }

  # Variáveis de ambiente para isolamento de controles
  export SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS=1
  export SDL_JOYSTICK_DEVICE="/dev/input/by-id/${joy_device}"
  export SDL_GAMECONTROLLERCONFIG_FILE="${CONTROLLER_DIR}/Player${instance_num}_mapping.cfg"
  export UDEV_INPUT="/dev/input/by-id/${joy_device}"

  # Configurações do Proton
  export STEAM_COMPAT_CLIENT_INSTALL_PATH="$HOME/.steam/steam"
  export STEAM_COMPAT_DATA_PATH="$prefix_dir"
  export WINEPREFIX="$prefix_dir/pfx"
  export DXVK_ASYNC=1
  export PROTON_LOG=1

  # Executar com gamescope
  gamescope -W $WIDTH -H $HEIGHT -f -- \
    "$PROTON_PATH" run "$EXE_PATH" > "${prefix_dir}.log" 2>&1 &

  echo $!
}

# Iniciar instâncias
echo "Iniciando instâncias com gamescope (${WIDTH}x${HEIGHT})..."
PID1=$(launch_game_instance 1 "${CONTROLLER_DIR}/Player1_Controller")
sleep 2
PID2=$(launch_game_instance 2 "${CONTROLLER_DIR}/Player2_Controller")

# Monitoramento
echo -e "\nInstâncias iniciadas:"
echo "Player 1 PID: $PID1 | Dispositivo: $(cat "${CONTROLLER_DIR}/Player1_Controller")"
echo "Player 2 PID: $PID2 | Dispositivo: $(cat "${CONTROLLER_DIR}/Player2_Controller")"
echo "Logs disponíveis em: $HOME/.proton_prefixes/"

# Finalização limpa
cleanup() {
  echo "Encerrando processos..."
  kill -SIGTERM $PID1 $PID2
  wait
  exit 0
}

trap cleanup SIGINT SIGTERM
wait