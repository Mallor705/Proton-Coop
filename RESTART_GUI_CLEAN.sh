#!/bin/bash
set -e

echo "═══════════════════════════════════════════════════════════"
echo "  LIMPEZA COMPLETA E REINÍCIO DA GUI"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Passo 1: Matar processos
echo "1️⃣  Matando todos os processos Python..."
killall -9 python 2>/dev/null || true
killall -9 python3 2>/dev/null || true
pkill -9 -f protoncoop 2>/dev/null || true
sleep 1
echo "   ✅ Processos finalizados"

# Passo 2: Limpar caches Python
echo ""
echo "2️⃣  Limpando caches Python..."
cd /workspace
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
echo "   ✅ Caches limpos"

# Passo 3: Verificar código
echo ""
echo "3️⃣  Verificando integridade do código..."
if grep -q "self.use_gamescope_check = Gtk.CheckButton()" src/gui/app.py; then
    linha=$(grep -n "self.use_gamescope_check = Gtk.CheckButton()" src/gui/app.py | cut -d: -f1)
    echo "   ✅ Widget encontrado na linha $linha"
else
    echo "   ❌ ERRO: Widget NÃO encontrado!"
    exit 1
fi

if grep -q "game_details_grid.attach(self.use_gamescope_check" src/gui/app.py; then
    echo "   ✅ Widget anexado ao grid"
else
    echo "   ❌ ERRO: Widget NÃO anexado!"
    exit 1
fi

if grep -q "use_gamescope=self.use_gamescope_check.get_active()" src/gui/app.py; then
    echo "   ✅ Salvamento implementado"
else
    echo "   ❌ ERRO: Salvamento NÃO implementado!"
    exit 1
fi

# Passo 4: Mostrar onde procurar
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  ✅ TUDO PRONTO!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "🚀 Iniciando a GUI..."
sleep 1

cd /workspace
python3 protoncoop.py gui
