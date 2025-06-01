#!/bin/bash

# Script para verificar se as variáveis de ambiente DXVK estão sendo aplicadas aos jogos em execução
# Uso: ./check_dxvk_env.sh [nome_do_processo]

echo "=== Verificador de Variáveis DXVK ==="
echo

# Se um nome de processo foi fornecido, usar esse; caso contrário, procurar por processos de jogos comuns
if [ $# -eq 1 ]; then
    PROCESS_NAME="$1"
else
    echo "Procurando por processos de jogos comuns..."
    PROCESS_NAME=""
fi

# Lista de processos de jogos comuns para verificar
COMMON_GAMES=("wine" "wine64" "proton" "steam" "game" "Game" ".exe")

# Função para verificar variáveis de ambiente de um PID
check_process_env() {
    local pid=$1
    local cmd=$2
    
    echo "----------------------------------------"
    echo "PID: $pid"
    echo "Comando: $cmd"
    echo "----------------------------------------"
    
    if [ -r "/proc/$pid/environ" ]; then
        # Verificar variáveis DXVK específicas
        echo "Variáveis DXVK encontradas:"
        cat "/proc/$pid/environ" 2>/dev/null | tr '\0' '\n' | grep -E "^DXVK_" | while read -r var; do
            echo "  ✓ $var"
        done
        
        # Verificar outras variáveis relevantes
        echo
        echo "Outras variáveis relevantes:"
        cat "/proc/$pid/environ" 2>/dev/null | tr '\0' '\n' | grep -E "^(WINE|STEAM_|VK_)" | while read -r var; do
            echo "  • $var"
        done
        
        # Verificar especificamente DXVK_ASYNC
        dxvk_async=$(cat "/proc/$pid/environ" 2>/dev/null | tr '\0' '\n' | grep "^DXVK_ASYNC=" | cut -d'=' -f2)
        if [ -n "$dxvk_async" ]; then
            if [ "$dxvk_async" = "1" ]; then
                echo
                echo "  🟢 DXVK_ASYNC está ATIVO (valor: $dxvk_async)"
            else
                echo
                echo "  🟡 DXVK_ASYNC está definido mas não ativo (valor: $dxvk_async)"
            fi
        else
            echo
            echo "  🔴 DXVK_ASYNC NÃO encontrado"
        fi
    else
        echo "  ❌ Não é possível ler as variáveis de ambiente (sem permissão)"
    fi
    echo
}

# Se um processo específico foi fornecido
if [ -n "$PROCESS_NAME" ]; then
    echo "Procurando por processos com nome: $PROCESS_NAME"
    pids=$(pgrep -f "$PROCESS_NAME")
    
    if [ -z "$pids" ]; then
        echo "❌ Nenhum processo encontrado com nome '$PROCESS_NAME'"
        exit 1
    fi
    
    for pid in $pids; do
        cmd=$(ps -p "$pid" -o comm= 2>/dev/null)
        check_process_env "$pid" "$cmd"
    done
else
    # Procurar por processos de jogos comuns
    found=false
    
    for game in "${COMMON_GAMES[@]}"; do
        pids=$(pgrep -f "$game")
        
        if [ -n "$pids" ]; then
            found=true
            echo "Encontrados processos relacionados a '$game':"
            
            for pid in $pids; do
                cmd=$(ps -p "$pid" -o args= 2>/dev/null | head -c 100)
                check_process_env "$pid" "$cmd"
            done
        fi
    done
    
    if [ "$found" = false ]; then
        echo "❌ Nenhum processo de jogo encontrado."
        echo
        echo "Dica: Execute este script enquanto um jogo estiver rodando, ou especifique um nome de processo:"
        echo "  $0 nome_do_jogo"
        echo
        echo "Para ver todos os processos atuais:"
        echo "  ps aux | grep -E '(wine|proton|steam|game)'"
    fi
fi

echo "=== Fim da verificação ==="

# Dicas adicionais
echo
echo "💡 Dicas:"
echo "   • Se DXVK_ASYNC=1 não aparecer, o jogo pode estar usando DirectX nativo"
echo "   • Use 'DXVK_HUD=compiler' para ver informações na tela do jogo"
echo "   • Verifique os logs do Steam/Proton em ~/.steam/steam/logs/"
echo "   • Para jogos nativos Linux, DXVK não é usado"