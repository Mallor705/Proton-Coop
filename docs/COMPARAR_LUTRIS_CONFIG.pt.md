# Como Comparar Configurações do Lutris com Linux-Coop

## 🎯 Objetivo

Este guia mostra como extrair as configurações que funcionam no Lutris e adaptá-las para o Linux-Coop.

---

## 📋 Passo 1: Localizar Arquivo de Configuração do Lutris

```bash
# Listar todos os jogos configurados no Lutris
ls -la ~/.config/lutris/games/

# Procurar especificamente por Elden Ring
ls -la ~/.config/lutris/games/ | grep -i elden
```

Exemplo de saída:
```
elden-ring-1234567.yml
```

---

## 🔍 Passo 2: Examinar Configuração do Lutris

```bash
# Ver configuração completa
cat ~/.config/lutris/games/elden-ring-*.yml
```

### Exemplo de saída do arquivo .yml:

```yaml
game:
  exe: /home/usuario/Games/EldenRing/Game/eldenring.exe
  prefix: /home/usuario/Games/elden-ring

wine:
  Desktop: false
  dxvk: true
  dxvk_nvapi: false
  esync: true
  fsync: true
  version: wine-ge-8-26

system:
  disable_compositor: true
  env:
    DXVK_ASYNC: '1'
    DXVK_HUD: '0'
    DXVK_STATE_CACHE: '1'
    STAGING_SHARED_MEMORY: '1'
    __GL_SHADER_DISK_CACHE: '1'
    __GL_SHADER_DISK_CACHE_PATH: /tmp/elden_shaders
    WINEDLLOVERRIDES: steam_api64=n,b;xinput1_3=n,b
```

---

## 🔄 Passo 3: Mapear Configurações Lutris → Linux-Coop

| **Lutris (.yml)** | **Linux-Coop (JSON)** | **Exemplo** |
|-------------------|------------------------|-------------|
| `game.exe` | `exe_path` | `/home/usuario/Games/EldenRing/Game/eldenring.exe` |
| `wine.version` | `proton_version` | `wine-ge-8-26` |
| `system.env` | `env_vars` | Todas as variáveis de ambiente |
| `wine.esync` | `PROTON_NO_ESYNC` | `true` → `"0"`, `false` → `"1"` |
| `wine.fsync` | `PROTON_NO_FSYNC` | `true` → `"0"`, `false` → `"1"` |
| `wine.dxvk` | Automático no Proton | - |

---

## 📝 Passo 4: Criar Perfil Linux-Coop Baseado no Lutris

Baseado no exemplo acima, crie um perfil JSON:

```json
{
  "game_name": "Elden Ring",
  "exe_path": "/home/usuario/Games/EldenRing/Game/eldenring.exe",
  "players": [
    {
      "account_name": "Player1",
      "language": "brazilian",
      "listen_port": "",
      "user_steam_id": "76561190000000001"
    },
    {
      "account_name": "Player2",
      "language": "brazilian",
      "listen_port": "",
      "user_steam_id": "76561190000000002"
    }
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
    "DXVK_ASYNC": "1",
    "DXVK_HUD": "0",
    "DXVK_STATE_CACHE": "1",
    "STAGING_SHARED_MEMORY": "1",
    "__GL_SHADER_DISK_CACHE": "1",
    "__GL_SHADER_DISK_CACHE_PATH": "/tmp/elden_shaders",
    "WINEDLLOVERRIDES": "steam_api64=n,b;xinput1_3=n,b",
    "PROTON_NO_ESYNC": "0",
    "PROTON_NO_FSYNC": "0"
  },
  "is_native": false,
  "mode": "splitscreen",
  "splitscreen": {
    "orientation": "horizontal",
    "instances": 2
  }
}
```

---

## 🔧 Passo 5: Copiar Prefix do Lutris (Opcional)

Se quiser usar o mesmo prefix Wine que funciona no Lutris:

```bash
# 1. Ver onde está o prefix do Lutris
cat ~/.config/lutris/games/elden-ring-*.yml | grep prefix

# Exemplo de saída:
# prefix: /home/usuario/Games/elden-ring

# 2. Criar estrutura de pastas do Linux-Coop
mkdir -p ~/Games/linux-coop/prefixes/Elden\ Ring/instance_1/
mkdir -p ~/Games/linux-coop/prefixes/Elden\ Ring/instance_2/

# 3. Copiar prefix do Lutris para ambas as instâncias
cp -r /home/usuario/Games/elden-ring \
      ~/Games/linux-coop/prefixes/Elden\ Ring/instance_1/pfx

cp -r /home/usuario/Games/elden-ring \
      ~/Games/linux-coop/prefixes/Elden\ Ring/instance_2/pfx
```

---

## 🐛 Passo 6: Debug e Comparação

### Verificar DLLs no Prefix do Lutris

```bash
LUTRIS_PREFIX="/home/usuario/Games/elden-ring"

# Ver todas as DLLs na pasta do jogo
ls -la $LUTRIS_PREFIX/drive_c/games/EldenRing/Game/*.dll

# Ver DLLs do sistema
ls -la $LUTRIS_PREFIX/drive_c/windows/system32/*.dll | grep -E "steam|xinput|dinput"
```

### Executar com Debug Ativado

Adicione ao perfil para ver logs detalhados:

```json
{
  "env_vars": {
    "WINEDEBUG": "+all",
    "DXVK_LOG_LEVEL": "debug",
    ...
  }
}
```

---

## 📊 Comparação: Heroic Game Launcher

Se você usa o Heroic:

```bash
# Configurações do Heroic estão em:
cat ~/.config/heroic/gog_store/installed.json
# ou
cat ~/.config/heroic/sideload_apps/elden-ring.json
```

O processo é similar ao Lutris.

---

## ✅ Checklist de Verificação

Após criar o perfil baseado no Lutris, verifique:

- [ ] Caminho do executável é exatamente o mesmo
- [ ] Versão do Wine/Proton é a mesma
- [ ] Todas as variáveis de ambiente foram copiadas
- [ ] WINEDLLOVERRIDES inclui todas as DLLs necessárias
- [ ] esync/fsync configurados corretamente (invertidos!)
- [ ] Prefix foi copiado ou será criado limpo

---

## 🎮 Teste Final

```bash
# Execute o Linux-Coop com o novo perfil
python linuxcoop.py elden-ring

# Verifique os logs
tail -f ~/.local/share/linux-coop/logs/latest.log
```

---

## 💡 Dicas Adicionais

### ESYNC/FSYNC - Atenção!

No Lutris:
- `esync: true` significa ativado
- `fsync: true` significa ativado

No Linux-Coop (Proton):
- `PROTON_NO_ESYNC: "0"` significa ativado
- `PROTON_NO_FSYNC: "0"` significa ativado

**É invertido!** O `NO_` no nome inverte a lógica.

### DLL Overrides - Sintaxe Correta

```
"WINEDLLOVERRIDES": "dll1=n,b;dll2=n,b;dll3=n,b"
```

- Separar múltiplas DLLs com `;` (ponto e vírgula)
- `n` = native (usar DLL do jogo/crack primeiro)
- `b` = builtin (usar DLL do Wine como fallback)
- `n,b` = tentar native primeiro, se falhar usar builtin

---

## 🆘 Problemas Comuns

### Erro: "Failed to create Wine prefix"

```bash
# Verifique permissões
ls -ld ~/Games/linux-coop/prefixes/

# Criar manualmente se necessário
mkdir -p ~/Games/linux-coop/prefixes/Elden\ Ring/instance_1/pfx
chmod -R 755 ~/Games/linux-coop/prefixes/
```

### Erro: "Wine version not found"

```bash
# Verificar onde o Lutris armazena o Wine
ls -la ~/.local/share/lutris/runners/wine/

# Copiar para onde o Linux-Coop procura
# (Verifique o código do Linux-Coop para ver onde ele procura)
```

### Jogo inicia mas crashea imediatamente

- Verifique se TODAS as DLLs do crack estão no lugar certo
- Confirme que WINEDLLOVERRIDES está correto
- Teste primeiro com uma instância só (desabilite splitscreen temporariamente)

---

**Última atualização**: 2025-10-06
