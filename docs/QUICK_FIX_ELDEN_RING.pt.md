# 🚀 Guia Rápido: Elden Ring Crackeado no Linux-Coop

## ⚡ Solução Rápida em 5 Passos

### 1️⃣ Extrair Configuração do Lutris

```bash
# Ver configuração que funciona
cat ~/.config/lutris/games/elden-ring-*.yml
```

**Anote:**
- Caminho do executável (`exe:`)
- Versão do Wine (`wine.version:`)
- Variáveis de ambiente (`system.env:`)

---

### 2️⃣ Criar Perfil JSON

Crie o arquivo `profiles/elden-ring.json`:

```json
{
  "game_name": "Elden Ring",
  "exe_path": "/CAMINHO/COMPLETO/DO/LUTRIS/eldenring.exe",
  "players": [
    {"account_name": "Player1", "language": "brazilian", "listen_port": "", "user_steam_id": "76561190000000001"},
    {"account_name": "Player2", "language": "brazilian", "listen_port": "", "user_steam_id": "76561190000000002"}
  ],
  "proton_version": "wine-ge-8-26",
  "instance_width": 1920,
  "instance_height": 1080,
  "player_physical_device_ids": ["", ""],
  "player_mouse_event_paths": ["", ""],
  "player_keyboard_event_paths": ["", ""],
  "player_audio_device_ids": ["", ""],
  "app_id": "1245620",
  "game_args": "",
  "use_goldberg_emu": true,
  "env_vars": {
    "WINEDLLOVERRIDES": "steam_api64=n,b;xinput1_3=n,b",
    "DXVK_ASYNC": "1",
    "DXVK_STATE_CACHE": "1",
    "PROTON_NO_ESYNC": "0",
    "PROTON_NO_FSYNC": "0",
    "__GL_SHADER_DISK_CACHE": "1"
  },
  "is_native": false,
  "mode": "splitscreen",
  "splitscreen": {"orientation": "horizontal", "instances": 2}
}
```

**⚠️ CRITICAL:**
- `exe_path`: Caminho ABSOLUTO (mesma linha `exe:` do Lutris)
- `proton_version`: Mesma versão do Lutris (`wine.version:`)
- `WINEDLLOVERRIDES`: DEVE incluir `steam_api64=n,b`

---

### 3️⃣ Copiar Prefix do Lutris (Opcional mas Recomendado)

```bash
# 1. Localizar prefix do Lutris
LUTRIS_PREFIX=$(cat ~/.config/lutris/games/elden-ring-*.yml | grep "prefix:" | awk '{print $2}')
echo "Prefix do Lutris: $LUTRIS_PREFIX"

# 2. Copiar para Linux-Coop
mkdir -p ~/Games/linux-coop/prefixes/Elden\ Ring/instance_1/
mkdir -p ~/Games/linux-coop/prefixes/Elden\ Ring/instance_2/

cp -r "$LUTRIS_PREFIX" ~/Games/linux-coop/prefixes/Elden\ Ring/instance_1/pfx
cp -r "$LUTRIS_PREFIX" ~/Games/linux-coop/prefixes/Elden\ Ring/instance_2/pfx
```

---

### 4️⃣ Verificar Arquivos do Crack

```bash
# Listar arquivos do jogo
ls -la /CAMINHO/DO/JOGO/Game/

# Deve conter:
# - eldenring.exe
# - steam_api64.dll (ou similar do crack)
# - Outros arquivos do crack
```

**Se faltar algum arquivo:**
- Copie da instalação original do Lutris
- Ou reinstale o crack

---

### 5️⃣ Executar

```bash
cd /workspace
python linuxcoop.py elden-ring

# Verificar logs se der erro
tail -f ~/.local/share/linux-coop/logs/latest.log
```

---

## 🔧 Troubleshooting Rápido

### Erro: "Page Fault" (mesmo após seguir os passos)

**Teste 1: Versão do Wine**
```bash
# No perfil JSON, mude para:
"proton_version": "GE-Proton9-20"
```

**Teste 2: Adicionar mais DLL overrides**
```json
"WINEDLLOVERRIDES": "steam_api64=n,b;xinput1_3=n,b;dinput8=n,b;d3d11=n,b"
```

**Teste 3: Desabilitar FSYNC/ESYNC**
```json
"PROTON_NO_ESYNC": "1",
"PROTON_NO_FSYNC": "1"
```

---

### Erro: "Executável não encontrado"

```bash
# Verifique se o caminho está correto
ls -la /CAMINHO/DO/exe_path/eldenring.exe

# Se não existir, encontre o caminho correto:
find ~/Games -name "eldenring.exe" 2>/dev/null
```

---

### Jogo abre mas fecha imediatamente

1. **Verificar DLLs do crack:**
   ```bash
   ls -la /CAMINHO/DO/JOGO/Game/*.dll
   ```
   
2. **Adicionar debug ao perfil:**
   ```json
   "env_vars": {
     "WINEDEBUG": "+all",
     ...
   }
   ```

3. **Verificar logs:**
   ```bash
   tail -100 ~/.local/share/linux-coop/logs/instance_1_*.log
   ```

---

## 📋 Checklist Ultra-Rápido

- [ ] `exe_path` é caminho ABSOLUTO (começa com `/`)
- [ ] Mesma versão do Wine do Lutris
- [ ] `WINEDLLOVERRIDES` contém `steam_api64=n,b`
- [ ] `use_goldberg_emu: true`
- [ ] Prefix copiado do Lutris OU criado limpo
- [ ] Todas as DLLs do crack presentes

---

## 🎯 Diferenças Principais: Lutris vs Linux-Coop

| Aspecto | Lutris | Linux-Coop |
|---------|--------|------------|
| **Caminho exe** | Relativo ou absoluto | DEVE ser absoluto |
| **ESYNC ativo** | `esync: true` | `PROTON_NO_ESYNC: "0"` |
| **FSYNC ativo** | `fsync: true` | `PROTON_NO_FSYNC: "0"` |
| **DLL override** | Interface gráfica | `WINEDLLOVERRIDES` manual |
| **Prefix** | Único | Um por instância |

---

## 💾 Template Mínimo Funcional

```json
{
  "game_name": "Elden Ring",
  "exe_path": "/home/SEU_USUARIO/Games/EldenRing/Game/eldenring.exe",
  "players": [
    {"account_name": "P1", "language": "brazilian", "listen_port": "", "user_steam_id": "76561190000000001"},
    {"account_name": "P2", "language": "brazilian", "listen_port": "", "user_steam_id": "76561190000000002"}
  ],
  "proton_version": "wine-ge-8-26",
  "instance_width": 1920,
  "instance_height": 1080,
  "app_id": "1245620",
  "use_goldberg_emu": true,
  "env_vars": {
    "WINEDLLOVERRIDES": "steam_api64=n,b"
  },
  "mode": "splitscreen",
  "splitscreen": {"orientation": "horizontal", "instances": 2}
}
```

---

## 📖 Documentação Completa

Para informações detalhadas:
- [Troubleshooting Completo](TROUBLESHOOTING_ELDEN_RING.pt.md)
- [Comparar com Lutris](COMPARAR_LUTRIS_CONFIG.pt.md)

---

**Última atualização**: 2025-10-06
