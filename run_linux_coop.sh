#!/bin/bash

# Verifica se um argumento (nome do perfil) foi fornecido
if [ -z "$1" ]; then
  echo "Erro: Nome do perfil não fornecido."
  echo "Uso: $0 <nome_do_perfil>"
  exit 1
fi

# Obtém o diretório onde o script .sh está localizado
SCRIPT_DIR_PATH=$(dirname "$(readlink -f "$0")")

# Constrói o caminho para o linuxcoop.py
PYTHON_SCRIPT_PATH="$SCRIPT_DIR_PATH/linuxcoop.py"

# Verifica se o linuxcoop.py existe
if [ ! -f "$PYTHON_SCRIPT_PATH" ]; then
    echo "Erro: linuxcoop.py não encontrado em $SCRIPT_DIR_PATH"
    exit 1
fi

# Navega para o diretório do script .sh (raiz do projeto)
# Isso é importante para que o linuxcoop.py possa resolver seus imports relativos corretamente
cd "$SCRIPT_DIR_PATH" || exit

# Executa o script Python, repassando o primeiro argumento ($1)
echo "Executando: python ./linuxcoop.py $1"
python ./linuxcoop.py "$1" 