#!/bin/bash
# filepath: /home/mallor/Documentos/GitHub/Linux-Coop/Linux-coop.sh

# --- Configuração Inicial ---
SCRIPT_NAME=$(basename "$0")
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
PROFILE_DIR="${SCRIPT_DIR}/profiles"
LOG_DIR="$HOME/.local/share/linux-coop/logs"
PREFIX_BASE_DIR="$HOME/.local/share/linux-coop/prefixes"
# Diretório temporário para configs do InputPlumber geradas por este script
INPUTPLUMBER_TEMP_CONFIG_DIR="/tmp/linux-coop-inputplumber-configs"
INPUTPLUMBER_SERVICE_NAME="inputplumber.service" # Nome correto do serviço systemd
INPUTPLUMBER_CTL_CMD="inputplumberctl" # Comando hipotético de controle do InputPlumber, ajustar conforme necessário.

# --- Funções Auxiliares ---
log_message() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

find_proton_path() {
  local version_string="$1"
  local proton_run_script=""
  local steam_root
  local search_paths=(
    "$HOME/.steam/root" "$HOME/.local/share/Steam" "$HOME/.steam/steam"
    "$HOME/.steam/debian-installation" "/var/mnt/games/messi/Games/Steam"
  )
  log_message "Procurando por Proton: $version_string"
  for steam_path in "${search_paths[@]}"; do
    [ ! -d "$steam_path" ] && continue
    log_message "Verificando diretório Steam: $steam_path"
    steam_root="$steam_path"
    local potential_path=""
    if [[ "$version_string" == "Experimental" ]]; then
      potential_path=$(find "$steam_path/steamapps/common/" -maxdepth 1 -type d -name "Proton - Experimental" 2>/dev/null | head -n 1)
    else
      potential_path=$(find "$steam_path/steamapps/common/" "$steam_path/compatibilitytools.d/" -maxdepth 1 -type d \( -name "Proton $version_string" -o -name "$version_string" \) 2>/dev/null | head -n 1)
    fi
    if [ -n "$potential_path" ] && [ -f "$potential_path/proton" ]; then
      proton_run_script="$potential_path/proton"
      break
    fi
  done
  if [ -z "$proton_run_script" ]; then
    log_message "ERRO: Proton '$version_string' não encontrado."
    return 1
  fi
  log_message "Proton encontrado: $proton_run_script"
  export STEAM_COMPAT_CLIENT_INSTALL_PATH="$steam_root"
  echo "$proton_run_script"
  return 0
}

# --- Funções InputPlumber (Hipotéticas) ---

# Garante que o serviço InputPlumber esteja rodando
ensure_inputplumber_running() {
  log_message "Verificando status do serviço ${INPUTPLUMBER_SERVICE_NAME}..."
  if ! systemctl is-active --quiet "$INPUTPLUMBER_SERVICE_NAME"; then
    log_message "Serviço não está ativo. Tentando iniciar..."
    sudo systemctl start "$INPUTPLUMBER_SERVICE_NAME" || {
      log_message "ERRO: Falha ao iniciar ${INPUTPLUMBER_SERVICE_NAME}. Verifique se está instalado e configurado."
      exit 1
    }
    log_message "Serviço iniciado."
    sleep 2 # Dar um tempo para o serviço inicializar
  else
    log_message "Serviço já está ativo."
  fi
}

# Gera um arquivo de configuração temporário para o InputPlumber
# NOTA: A sintaxe do arquivo é COMPLETAMENTE HIPOTÉTICA!
generate_inputplumber_config() {
  local profile_name="$1"
  local config_file="$2"
  local num_players="$3"
  local base_name="$4"
  # A var @P transforma o argumento (o array do profile) em elementos separados
  local -n physical_ids=$5 # Passa o array por referência

  log_message "Gerando configuração InputPlumber em: $config_file"
  # Limpa o arquivo se existir
  > "$config_file"

  echo "# Configuração InputPlumber gerada por $SCRIPT_NAME para o perfil $profile_name" >> "$config_file"
  echo "" >> "$config_file"

  for (( p=0; p<num_players; p++ )); do
    local player_num=$((p+1))
    local physical_id="${physical_ids[$p]}"
    local virtual_name="${base_name}${player_num}" # Ex: virtual-gamepad-p1

    # Define o dispositivo físico
    echo "[device \"physical_p${player_num}\"]" >> "$config_file"
    echo "  match_type = \"path\"" >> "$config_file"
    echo "  match_string = \"${physical_id}\"" >> "$config_file"
    echo "  grab = true  # Captura exclusiva" >> "$config_file"
    echo "  optional = true" >> "$config_file"   # Nova linha para não falhar se o dispositivo físico estiver ausente
    echo "  driver = \"evdev\"" >> "$config_file"
    echo "" >> "$config_file"

    # Define o dispositivo virtual de saída
    echo "[output \"virtual_p${player_num}\"]" >> "$config_file"
    echo "  driver = \"uinput\"" >> "$config_file"
    echo "  name = \"${virtual_name}\" # Nome usado para /dev/input/${virtual_name}" >> "$config_file"
    # TODO: Idealmente, copiar capacidades (ABS, KEY, REL) do físico
    echo "" >> "$config_file"

    # Define a rota
    echo "[route \"route_p${player_num}\"]" >> "$config_file"
    echo "  input = \"physical_p${player_num}\"" >> "$config_file"
    echo "  output = \"virtual_p${player_num}\"" >> "$config_file"
    echo "" >> "$config_file"
  done

  log_message "Configuração InputPlumber gerada."
}

# Recarrega a configuração do InputPlumber
reload_inputplumber() {
  local config_file="$1"
  log_message "Iniciando daemon InputPlumber com a configuração: $config_file..."
  sudo ./inputplumber --config "$config_file" &
  sleep 5  # Aumentado para garantir a criação do dispositivo virtual
}

# Remove a configuração temporária e recarrega InputPlumber para liberar devices
cleanup_inputplumber_config() {
  log_message "Limpando configuração temporária do InputPlumber..."
  if [ -d "$INPUTPLUMBER_TEMP_CONFIG_DIR" ]; then
    rm -f "$INPUTPLUMBER_TEMP_CONFIG_DIR"/*.conf
    if command -v "$INPUTPLUMBER_CTL_CMD" &> /dev/null; then
       log_message "Solicitando recarregamento do InputPlumber para liberar dispositivos..."
       "$INPUTPLUMBER_CTL_CMD" reload --config-dir "$INPUTPLUMBER_TEMP_CONFIG_DIR" || log_message "Aviso: Falha ao recarregar InputPlumber durante limpeza."
    fi
  fi
  log_message "Limpeza da configuração InputPlumber concluída."
}

# --- Função de Limpeza Geral ---
cleanup_previous_instances() {
  local proton_cmd_path="$1"
  local exe_path_pattern="$2"
  log_message "Tentando encerrar instâncias anteriores de '$exe_path_pattern'..."
  pkill -f "gamescope.*-- '$proton_cmd_path' run '$exe_path_pattern'" && sleep 1 || true
  pkill -f "'$proton_cmd_path' run '$exe_path_pattern'" && sleep 1 || true
}

terminate_instances() {
  log_message "Recebido sinal de interrupção. Encerrando instâncias..."
  if [ ${#PIDS[@]} -gt 0 ]; then
    log_message "Encerrando PIDs das instâncias: ${PIDS[@]}"
    kill "${PIDS[@]}" 2>/dev/null && sleep 2
    kill -9 "${PIDS[@]}" 2>/dev/null
  fi
  cleanup_inputplumber_config
  log_message "Limpeza concluída."
  exit 0
}

# Nova função para aguardar a senha do sudo
prompt_sudo_password() {
  echo "Por favor, insira sua senha de sudo (será solicitada se necessário):"
  sudo -v
}

# --- Script Principal ---

if [ -z "$1" ]; then
  echo "Uso: $SCRIPT_NAME <nome_do_perfil>"
  exit 1
fi
PROFILE_NAME="$1"
PROFILE_FILE="$PROFILE_DIR/$PROFILE_NAME.profile"
if [ ! -f "$PROFILE_FILE" ]; then
  echo "Erro: Perfil não encontrado: $PROFILE_FILE"
  exit 1
fi

log_message "Carregando perfil: $PROFILE_NAME"
source "$PROFILE_FILE"

# Validar variáveis obrigatórias
missing_vars=()
[[ -z "$GAME_NAME" ]] && missing_vars+=("GAME_NAME")
[[ -z "$EXE_PATH" ]] && missing_vars+=("EXE_PATH")
[[ -z "$PROTON_VERSION" ]] && missing_vars+=("PROTON_VERSION")
[[ -z "$NUM_PLAYERS" ]] && missing_vars+=("NUM_PLAYERS")
[[ -z "$INSTANCE_WIDTH" ]] && missing_vars+=("INSTANCE_WIDTH")
[[ -z "$INSTANCE_HEIGHT" ]] && missing_vars+=("INSTANCE_HEIGHT")
[[ -z "$VIRTUAL_DEVICE_BASENAME" ]] && missing_vars+=("VIRTUAL_DEVICE_BASENAME")
[[ ${#PLAYER_PHYSICAL_DEVICE_IDS[@]} -eq 0 && "$NUM_PLAYERS" -gt 0 ]] && missing_vars+=("PLAYER_PHYSICAL_DEVICE_IDS (array não pode ser vazio para NUM_PLAYERS > 0)")
[[ ${#PLAYER_PHYSICAL_DEVICE_IDS[@]} -ne "$NUM_PLAYERS" && "$NUM_PLAYERS" -gt 0 ]] && missing_vars+=("Número de elementos em PLAYER_PHYSICAL_DEVICE_IDS (${#PLAYER_PHYSICAL_DEVICE_IDS[@]}) diferente de NUM_PLAYERS ($NUM_PLAYERS)")

if [ ${#missing_vars[@]} -gt 0 ]; then
  echo "Erro: Variáveis obrigatórias faltando no perfil:"
  printf " - %s\n" "${missing_vars[@]}"
  exit 1
fi

log_message "Verificando dependências..."
command -v gamescope &> /dev/null || { echo "Erro: 'gamescope' não encontrado."; exit 1; }
command -v bwrap &> /dev/null || { echo "Erro: 'bwrap' (bubblewrap) não encontrado."; exit 1; }
log_message "Dependências verificadas com sucesso."

prompt_sudo_password

mkdir -p "$LOG_DIR"
mkdir -p "$PREFIX_BASE_DIR"
mkdir -p "$INPUTPLUMBER_TEMP_CONFIG_DIR" || { echo "ERRO: Não foi possível criar diretório temporário para InputPlumber: $INPUTPLUMBER_TEMP_CONFIG_DIR"; exit 1; }

PROTON_CMD_PATH=$(find_proton_path "$PROTON_VERSION") || exit 1 
[ ! -f "$EXE_PATH" ] && { echo "Erro: Executável do jogo não existe: $EXE_PATH"; exit 1; }
EXE_NAME=$(basename "$EXE_PATH") 

if [ ! -f "$EXE_PATH" ]; then
    echo "Erro: Executável do jogo não encontrado em: $EXE_PATH"
    exit 1
fi

ensure_inputplumber_running
INPUTPLUMBER_CONF_FILE="$INPUTPLUMBER_TEMP_CONFIG_DIR/${PROFILE_NAME}.conf"
generate_inputplumber_config "$PROFILE_NAME" "$INPUTPLUMBER_CONF_FILE" "$NUM_PLAYERS" "$VIRTUAL_DEVICE_BASENAME" PLAYER_PHYSICAL_DEVICE_IDS
reload_inputplumber "$INPUTPLUMBER_CONF_FILE"

declare -a VIRTUAL_DEVICE_PATHS=()
log_message "Procurando por dispositivos virtuais criados..."
for (( p=1; p<=NUM_PLAYERS; p++ )); do
    virt_name="${VIRTUAL_DEVICE_BASENAME}${p}"
    found_path=$(find /dev/input/by-id/ -name "$virt_name" -print -quit)
    if [ -z "$found_path" ]; then
        log_message "ERRO: Dispositivo virtual '$virt_name' não encontrado em /dev/input/by-id/ após recarregar InputPlumber."
        cleanup_inputplumber_config
        exit 1
    fi
    log_message "Encontrado dispositivo virtual para Jogador $p: $found_path"
    VIRTUAL_DEVICE_PATHS+=("$found_path")
done
if [ ${#VIRTUAL_DEVICE_PATHS[@]} -ne "$NUM_PLAYERS" ]; then
   log_message "ERRO: Número de dispositivos virtuais encontrados (${#VIRTUAL_DEVICE_PATHS[@]}) não bate com NUM_PLAYERS ($NUM_PLAYERS)."
   cleanup_inputplumber_config
   exit 1
fi

cleanup_previous_instances "$PROTON_CMD_PATH" "$EXE_PATH"

declare -a PIDS=()
trap terminate_instances SIGINT SIGTERM

log_message "Iniciando $NUM_PLAYERS instância(s) de '$GAME_NAME' usando InputPlumber e Bubblewrap..."

for (( i=1; i<=NUM_PLAYERS; i++ )); do
  instance_num=$i
  player_index=$((i-1))
  log_message "Preparando instância $instance_num..."

  prefix_dir="$PREFIX_BASE_DIR/${PROFILE_NAME}_instance_${instance_num}"
  mkdir -p "$prefix_dir/pfx" || { log_message "Erro ao criar diretório do prefixo: $prefix_dir"; terminate_instances; exit 1; }
  log_message "WINEPREFIX para instância $instance_num: $prefix_dir/pfx"

  current_virtual_device_path="${VIRTUAL_DEVICE_PATHS[$player_index]}"
  if [ ! -e "$current_virtual_device_path" ]; then
      log_message "ERRO: O dispositivo virtual '$current_virtual_device_path' para jogador $instance_num desapareceu!"
      terminate_instances
      exit 1
  fi
  # Utilize o mesmo nome virtual gerado anteriormente
  virt_name="${VIRTUAL_DEVICE_BASENAME}${instance_num}"
  log_message "Instância $instance_num usará o dispositivo virtual: $current_virtual_device_path"

  bwrap_cmd=(
    bwrap
    --unshare-all --share-net
    --proc /proc --dev /dev
    --dev-bind /dev/dri /dev/dri
    --dev-bind /dev/snd /dev/snd
    --ro-bind /dev/shm /dev/shm
    --ro-bind /etc/machine-id /etc/machine-id
    --ro-bind /var/lib/dbus /var/lib/dbus
    --bind /tmp/.X11-unix /tmp/.X11-unix
    --bind "$XDG_RUNTIME_DIR/pulse" "$XDG_RUNTIME_DIR/pulse"
    "--dev-bind" "$current_virtual_device_path" "/dev/input/${virt_name}"  # Corrigido: mapeamento dinâmico para cada virtual device
    --ro-bind /usr /usr
    --bind "$prefix_dir" "$prefix_dir"
    --bind "$HOME" "$HOME"
    --bind "$(dirname "$EXE_PATH")" "$(dirname "$EXE_PATH")"
    --bind "$(dirname "$PROTON_CMD_PATH")/../../.." "$(dirname "$PROTON_CMD_PATH")/../../.."
    --setenv STEAM_COMPAT_DATA_PATH "$prefix_dir"
    --setenv WINEPREFIX "$prefix_dir/pfx"
    --setenv DXVK_ASYNC "1"
    --setenv PROTON_LOG "1"
    --setenv PROTON_LOG_DIR "$LOG_DIR"
  )

  gamescope_cmd=(
    gamescope
    -W "$INSTANCE_WIDTH" -H "$INSTANCE_HEIGHT" -f
    -- 
  )

  proton_cmd=(
    "$PROTON_CMD_PATH" run "$EXE_PATH"
  )

  log_file="$LOG_DIR/${PROFILE_NAME}_instance_${instance_num}.log"
  log_message "Lançando instância $instance_num (Log: $log_file)..."

  "${bwrap_cmd[@]}" "${gamescope_cmd[@]}" "${proton_cmd[@]}" > "$log_file" 2>&1 &
  pid=$!
  PIDS+=($pid)
  log_message "Instância $instance_num iniciada com PID: $pid"
  sleep 5
done

log_message "Todas as $NUM_PLAYERS instâncias foram lançadas."
log_message "PIDs: ${PIDS[@]}"
log_message "Pressione CTRL+C neste terminal para encerrar todas as instâncias e liberar os controles."

while true; do
    all_dead=true
    for pid in "${PIDS[@]}"; do [ -e "/proc/$pid" ] && all_dead=false && break; done
    if $all_dead; then log_message "Todas as instâncias parecem ter sido encerradas."; break; fi
    sleep 5
done

cleanup_inputplumber_config
log_message "Script concluído."
exit 0