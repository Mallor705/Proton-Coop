#!/bin/bash

echo "═══════════════════════════════════════════════════════════"
echo "  🧪 TESTE DE SALVAMENTO - USE_GAMESCOPE"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Este script irá:"
echo "1. Mostrar onde os perfis são salvos"
echo "2. Verificar se USE_GAMESCOPE está nos perfis existentes"
echo "3. Dar instruções para testar manualmente"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""

# Diretório de perfis
PROFILE_DIR="$HOME/.config/linux-coop/profiles"

echo "📁 Diretório de perfis: $PROFILE_DIR"

if [ -d "$PROFILE_DIR" ]; then
    echo "   ✅ Diretório existe"
    
    # Listar perfis
    profiles=$(ls -1 "$PROFILE_DIR"/*.json 2>/dev/null)
    
    if [ -n "$profiles" ]; then
        echo ""
        echo "📄 Perfis encontrados:"
        echo "$profiles" | while read profile; do
            echo "   - $(basename "$profile")"
        done
        
        echo ""
        echo "🔍 Verificando se USE_GAMESCOPE está nos perfis:"
        echo ""
        
        echo "$profiles" | while read profile; do
            echo "   📝 $(basename "$profile"):"
            if grep -q "USE_GAMESCOPE" "$profile"; then
                value=$(grep "USE_GAMESCOPE" "$profile" | head -1)
                echo "      ✅ Campo encontrado: $value"
            else
                echo "      ❌ Campo USE_GAMESCOPE NÃO encontrado"
            fi
        done
    else
        echo "   ⚠️  Nenhum perfil salvo ainda"
    fi
else
    echo "   ⚠️  Diretório não existe (nenhum perfil criado ainda)"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  📝 COMO TESTAR:"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "1. Abra a GUI em um terminal separado:"
echo "   python3 /workspace/linuxcoop.py gui"
echo ""
echo "2. Crie um perfil de teste:"
echo "   - Game Name: TestGamescope"
echo "   - Executable Path: /tmp/test.exe"
echo "   - DESMARQUE 'Use Gamescope?'"
echo "   - Clique em 'Save'"
echo ""
echo "3. Verifique se foi salvo:"
echo "   cat ~/.config/linux-coop/profiles/testgamescope.json | grep USE_GAMESCOPE"
echo ""
echo "4. Deve mostrar:"
echo "   \"USE_GAMESCOPE\": false"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "💡 LOGS DE DEBUG:"
echo ""
echo "Se executar a GUI pelo terminal, procure por linhas como:"
echo "   DEBUG: USE_GAMESCOPE value being saved: True/False"
echo ""
echo "Isso confirma se o valor está sendo capturado corretamente."
echo ""
echo "═══════════════════════════════════════════════════════════"

