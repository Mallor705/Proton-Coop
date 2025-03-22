#!/bin/bash

# Diretório para armazenar as configurações de controladores
DIR_CO_OP_CONT="./controller_config"

# Solicitar o nome do arquivo de perfil
PROFILE_FILE=$(zenity --file-selection --save --confirm-overwrite --title="Escolha o nome do arquivo de perfil" --filename="./profiles/profile")
if [ -z "$PROFILE_FILE" ]; then
  echo "Erro: Nome do arquivo de perfil não fornecido."
  exit 1
fi

# Solicitar o caminho do executável .exe se não estiver definido
if [ -z "$EXE_PATH" ]; then
  EXE_PATH=$(zenity --file-selection --title="Selecione o executável do jogo (.exe)" --file-filter="*.exe")
  if [ -z "$EXE_PATH" ]; then
    echo "Erro: Caminho do executável não fornecido."
    exit 1
  fi
fi

# Solicitar a versão do Proton se não estiver definida
if [ -z "$PROTON_VERSION" ]; then
  PROTON_VERSION=$(zenity --list --title="Versão do Proton" --text="Selecione a versão do Proton:" \
    --column="Versão" "Experimental" "Hotfix" "9.0 (Beta)" "8.0" "7.0" "6.0" "GE-Proton9-26" "GE-Proton8-15")
  if [ -z "$PROTON_VERSION" ]; then
    echo "Erro: Versão do Proton não fornecida."
    exit 1
  fi
fi

# Solicitar a resolução da janela do jogo se não estiver definida
if [ -z "$WIDTH" ] || [ -z "$HEIGHT" ]; then
  RESOLUTION=$(zenity --forms --title="Resolução do Jogo" --text="Insira a resolução desejada:" \
    --add-entry="Largura (ex: 1920)" \
    --add-entry="Altura (ex: 1080)")
  if [ -z "$RESOLUTION" ]; then
    echo "Erro: Resolução não fornecida."
    exit 1
  fi

  WIDTH=$(echo "$RESOLUTION" | cut -d'|' -f1)
  HEIGHT=$(echo "$RESOLUTION" | cut -d'|' -f2)

  if [ -z "$WIDTH" ] || [ -z "$HEIGHT" ]; then
    echo "Erro: Resolução inválida fornecida."
    exit 1
  fi
fi

# Gerenciar controladores de jogo
if [ "$1" = "--quickrun" ] && [ -d "$DIR_CO_OP_CONT" ]; then
  echo "Controladores já configurados."
else
  # Limpar e recriar o diretório de controladores
  rm -rf "$DIR_CO_OP_CONT"
  mkdir -p "$DIR_CO_OP_CONT"

  # Listar controladores disponíveis
  CONTROLLER_LIST=$(ls -l /dev/input/by-id/ | grep joystick | awk '{gsub("-joystick", ""); gsub("-event", ""); print $9}' | uniq)

  if [ -z "$CONTROLLER_LIST" ]; then
    echo "Erro: Nenhum controlador detectado. Conecte os controladores e tente novamente."
    exit 1
  fi

  # Selecionar controladores para os jogadores
  CONTROLLER_1=$(zenity --list --title="Escolha o controlador para o jogador 1" --text="Selecione o controlador para o jogador 1:" \
    --column="Controladores" $CONTROLLER_LIST)
  CONTROLLER_2=$(zenity --list --title="Escolha o controlador para o jogador 2" --text="Selecione o controlador para o jogador 2:" \
    --column="Controladores" $CONTROLLER_LIST)

  if [ -z "$CONTROLLER_1" ] || [ -z "$CONTROLLER_2" ]; then
    echo "Erro: Você deve selecionar controladores para ambos os jogadores."
    exit 1
  fi

  # Criar arquivos de blacklist para os controladores
  ls -l /dev/input/by-id/ | grep joystick | grep -wv "$CONTROLLER_1" | awk '{print "--blacklist=/dev/input/by-id/" $9;}' > "$DIR_CO_OP_CONT/Player1_Controller_Blacklist"
  ls -l /dev/input/by-id/ | grep joystick | grep -wv "$CONTROLLER_2" | awk '{print "--blacklist=/dev/input/by-id/" $9;}' > "$DIR_CO_OP_CONT/Player2_Controller_Blacklist"

  # Criar arquivos de configuração de controladores
  ls -l /dev/input/by-id/ | grep joystick | grep -wv "$CONTROLLER_1" | awk '{print "/dev/input/by-id/" $9;}' > "$DIR_CO_OP_CONT/Player1_Controller"
  ls -l /dev/input/by-id/ | grep joystick | grep -wv "$CONTROLLER_2" | awk '{print "/dev/input/by-id/" $9;}' > "$DIR_CO_OP_CONT/Player2_Controller"
fi

# Salvar as configurações no arquivo profile
cat <<EOL > "$PROFILE_FILE"
EXE_PATH="$EXE_PATH"
PROTON_VERSION="$PROTON_VERSION"
WIDTH="$WIDTH"
HEIGHT="$HEIGHT"
DIR_CO_OP_CONT="$DIR_CO_OP_CONT"
EOL

echo "Configurações salvas no arquivo $PROFILE_FILE."