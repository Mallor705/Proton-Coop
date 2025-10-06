# Solução de Problemas - Elden Ring (Versão Crackeada)

## Erro: Page Fault on Read Access (0x0000000000000000)

### Descrição do Erro

Ao executar o Elden Ring crackeado via Linux-Coop, você pode encontrar o seguinte erro:

```
Unhandled exception: page fault on read access to 0x0000000000000000 in 64-bit code
```

Este erro indica uma tentativa de acesso a memória nula (null pointer dereference), onde o jogo tenta ler dados de um endereço de memória inválido (0x0000000000000000).

### Análise Técnica

- **Instrução que falhou**: `movq (%rcx), %rax`
- **Registrador RCX**: Contém 0x0000000000000000 (ponteiro nulo)
- **Local do crash**: `eldenring+0x1e9f53b`
- **Ambiente**: Wine 10.16, Linux kernel 6.17.0-4-cachyos

### ⚠️ Informação Importante

Como o jogo funciona no **Lutris** e **Heroic Game Launcher**, mas falha no Linux-Coop, o problema está nas diferenças de configuração do ambiente Wine/Proton entre os launchers.

**Causas mais prováveis para versões crackeadas:**
1. Variáveis de ambiente diferentes
2. DLLs ou overrides necessários não configurados
3. Versão do Wine/Proton incompatível
4. Prefix do Wine com configurações diferentes
5. Arquivos do crack faltando ou caminho incorreto

---

## Soluções Possíveis (Para Versões Crackeadas)

### 🔍 Solução 0: Comparar Configurações do Lutris/Heroic (RECOMENDADO)

**Passo 1: Verificar configuração do Lutris**

1. Abra o Lutris
2. Clique com botão direito no Elden Ring → **Configure**
3. Vá para a aba **Runner options**
4. Anote:
   - Versão do Wine/Proton
   - DLL overrides
   - Variáveis de ambiente

**Passo 2: Verificar configuração do Heroic**

1. Abra o Heroic Game Launcher
2. Vá em Settings → Wine/Proton
3. Clique no jogo → Settings
4. Anote as mesmas configurações

**Passo 3: Exportar configuração funcional do Lutris**

```bash
# Ver variáveis de ambiente do Lutris
cat ~/.config/lutris/games/elden-ring-*.yml
```

Procure por seções como:
```yaml
game:
  exe: /caminho/para/eldenring.exe
  prefix: /caminho/para/prefix

system:
  env:
    DXVK_ASYNC: '1'
    # Outras variáveis importantes
```

**Passo 4: Adaptar para o Linux-Coop**

Copie as configurações que funcionam para o seu perfil JSON.

---

### 🔧 Solução 1: Atualizar/Mudar Versão do Proton

O Elden Ring é sensível à versão do Proton. Tente diferentes versões:

**Versões recomendadas:**
- **Proton GE-Proton9-20** ou superior
- **Proton Experimental**
- **Proton 8.0-5** ou superior

**Como mudar no perfil:**
```json
{
  "proton_version": "GE-Proton9-20",
  ...
}
```

### 🔧 Solução 2: Verificar Arquivos do Crack

**Importante para versões crackeadas:**

1. **Verifique se todos os arquivos do crack estão presentes:**
   ```bash
   ls -la /caminho/para/elden/ring/Game/
   ```

   Procure por:
   - `eldenring.exe` (arquivo principal)
   - Possíveis DLLs do crack (ex: `steam_api64.dll`, `codex.dll`, etc.)
   - Arquivos `.ini` ou configuração do crack

2. **Use o executável correto no perfil:**

   Versões crackeadas geralmente têm múltiplos executáveis. Certifique-se de usar o mesmo que funciona no Lutris:

   ```json
   {
     "exe_path": "/caminho/completo/para/eldenring.exe",
     ...
   }
   ```

   **Evite usar caminhos relativos** com versões crackeadas. Use o caminho absoluto completo.

3. **Verifique permissões dos arquivos:**
   ```bash
   chmod +x /caminho/para/eldenring.exe
   ```

### 🔧 Solução 3: Variáveis de Ambiente Adicionais

Adicione estas variáveis de ambiente ao perfil do jogo:

```json
{
  "env_vars": {
    "PROTON_USE_WINED3D": "0",
    "PROTON_NO_ESYNC": "0",
    "PROTON_NO_FSYNC": "0",
    "PROTON_FORCE_LARGE_ADDRESS_AWARE": "1",
    "WINE_LARGE_ADDRESS_AWARE": "1",
    "DXVK_ASYNC": "1",
    "DXVK_STATE_CACHE_PATH": "/tmp/dxvk_cache",
    "MANGOHUD": "0"
  },
  ...
}
```

### 🔧 Solução 4: Copiar Prefix do Lutris (RECOMENDADO)

Se o jogo funciona no Lutris, você pode copiar o prefix configurado:

1. **Localizar o prefix do Lutris:**
   ```bash
   # Prefixes do Lutris geralmente estão em:
   ls -la ~/Games/elden-ring/
   # ou
   ls -la ~/.local/share/lutris/runners/wine/
   ```

2. **Verificar qual prefix o Lutris está usando:**
   ```bash
   cat ~/.config/lutris/games/elden-ring-*.yml | grep prefix
   ```

3. **Copiar o prefix funcional:**
   ```bash
   # Backup do prefix atual (se existir)
   mv ~/Games/linux-coop/prefixes/Elden\ Ring ~/Games/linux-coop/prefixes/Elden\ Ring.bak
   
   # Copiar prefix do Lutris
   cp -r /caminho/do/prefix/lutris ~/Games/linux-coop/prefixes/Elden\ Ring/instance_1/pfx
   ```

4. **Ou criar um prefix limpo:**
   ```bash
   rm -rf ~/Games/linux-coop/prefixes/Elden\ Ring/
   # O Linux-Coop criará um novo na próxima execução
   ```

### 🔧 Solução 5: Instalar Dependências do Wine

**Verificar o que o Lutris instalou no prefix:**

```bash
# Listar DLLs no prefix do Lutris
ls -la /caminho/do/prefix/lutris/drive_c/windows/system32/*.dll
```

**Instalar as mesmas dependências no Linux-Coop:**

```bash
# Configurar WINEPREFIX para o Linux-Coop
export WINEPREFIX=~/Games/linux-coop/prefixes/Elden\ Ring/instance_1/pfx

# Instalar dependências comuns para Elden Ring crackeado
winetricks -q vcrun2019 vcrun2022 dxvk vkd3d

# Se usar Proton diretamente
protontricks-launch --appid 1245620 winetricks vcrun2019 vcrun2022
```

**Dependências mais comuns para versões crackeadas:**
- `vcrun2019` ou `vcrun2022` (Visual C++ Runtime)
- `dxvk` (DirectX to Vulkan)
- `d3dcompiler_47` (DirectX shader compiler)
- `xinput1_3` (Controller support)

### 🔧 Solução 6: Verificar Integridade dos Arquivos

No Steam:

1. Clique com botão direito em **Elden Ring**
2. Selecione **Propriedades**
3. Vá para **Arquivos Instalados**
4. Clique em **Verificar integridade dos arquivos do jogo**

### 🔧 Solução 7: Argumentos de Lançamento

Adicione argumentos específicos para o Elden Ring:

```json
{
  "game_args": "-fullscreen -dx12",
  ...
}
```

Ou tente com DirectX 11:
```json
{
  "game_args": "-dx11",
  ...
}
```

### 🔧 Solução 8: Atualizar Drivers Gráficos

Certifique-se de estar usando os drivers gráficos mais recentes:

**Para NVIDIA:**
```bash
# Verifique a versão atual
nvidia-smi

# Atualize via gerenciador de pacotes da sua distro
```

**Para AMD:**
```bash
# Mesa deve estar atualizado
# Verifique a versão
glxinfo | grep "OpenGL version"
```

---

## Exemplo de Perfil Completo para Elden Ring Crackeado

### Perfil Otimizado (Baseado em configurações do Lutris)

```json
{
  "game_name": "Elden Ring",
  "exe_path": "/home/SEU_USUARIO/Games/EldenRing/Game/eldenring.exe",
  "players": [
    {
      "account_name": "Tarnished1",
      "language": "brazilian",
      "listen_port": "",
      "user_steam_id": "76561190000000001"
    },
    {
      "account_name": "Tarnished2",
      "language": "brazilian",
      "listen_port": "",
      "user_steam_id": "76561190000000002"
    }
  ],
  "proton_version": "wine-ge-8-26",
  "instance_width": 1920,
  "instance_height": 1080,
  "player_physical_device_ids": [
    "/dev/input/by-id/seu-controle-player1",
    "/dev/input/by-id/seu-controle-player2"
  ],
  "player_mouse_event_paths": ["", ""],
  "player_keyboard_event_paths": ["", ""],
  "player_audio_device_ids": ["", ""],
  "app_id": "1245620",
  "game_args": "",
  "use_goldberg_emu": true,
  "env_vars": {
    "WINEDLLOVERRIDES": "steam_api64=n,b;xinput1_3=n,b;dinput8=n,b",
    "DXVK_ASYNC": "1",
    "DXVK_STATE_CACHE": "1",
    "DXVK_HUD": "0",
    "PROTON_NO_ESYNC": "0",
    "PROTON_NO_FSYNC": "0",
    "PROTON_FORCE_LARGE_ADDRESS_AWARE": "1",
    "__GL_SHADER_DISK_CACHE": "1",
    "__GL_SHADER_DISK_CACHE_PATH": "/tmp/elden_shader_cache",
    "MANGOHUD": "0",
    "WINEFSYNC": "1",
    "WINEESYNC": "1"
  },
  "is_native": false,
  "mode": "splitscreen",
  "splitscreen": {
    "orientation": "horizontal",
    "instances": 2
  }
}
```

### Notas Importantes sobre o Perfil:

1. **exe_path**: Use o caminho ABSOLUTO completo do executável
2. **proton_version**: Pode ser `wine-ge-8-26`, `GE-Proton9-20`, ou a mesma versão do Lutris
3. **use_goldberg_emu**: Defina como `true` se o crack usa steam_api64.dll modificado
4. **WINEDLLOVERRIDES**: 
   - `steam_api64=n,b` é ESSENCIAL para cracks
   - `xinput1_3=n,b` para suporte a controles
   - `dinput8=n,b` pode ajudar com alguns cracks

---

## Checklist de Diagnóstico (Versão Crackeada)

Execute estas verificações em ordem:

### 🔍 Comparação com Lutris/Heroic
- [ ] Verificar versão do Wine/Proton usada no Lutris
- [ ] Exportar variáveis de ambiente do Lutris
- [ ] Comparar DLL overrides
- [ ] Verificar caminho do executável (absoluto vs relativo)

### ✅ Arquivos do Crack
- [ ] Todos os arquivos do crack estão presentes
- [ ] Usando o executável correto (mesmo do Lutris)
- [ ] DLLs do crack (steam_api64.dll, etc.) na pasta correta
- [ ] Permissões de execução configuradas

### ⚙️ Configuração do Wine
- [ ] Versão do Wine/Proton compatível
- [ ] WINEDLLOVERRIDES inclui `steam_api64=n,b`
- [ ] Variáveis de ambiente configuradas (DXVK_ASYNC, etc.)
- [ ] Prefix do Wine limpo ou copiado do Lutris
- [ ] Dependências instaladas (vcrun2019, vcrun2022, dxvk)

### 🎮 Configuração do Jogo
- [ ] Caminho absoluto para o executável
- [ ] use_goldberg_emu configurado corretamente
- [ ] app_id correto (1245620 para Elden Ring)
- [ ] Argumentos de lançamento testados

### 🖥️ Sistema
- [ ] Drivers gráficos atualizados
- [ ] Espaço em disco suficiente
- [ ] Gamescope e bwrap funcionando

---

## Logs e Depuração

Para obter mais informações sobre o erro:

1. **Verifique os logs do Linux-Coop**:
   ```bash
   cat ~/.local/share/linux-coop/logs/latest.log
   ```

2. **Execute com saída de debug do Wine**:
   ```json
   {
     "env_vars": {
       "WINEDEBUG": "+all",
       ...
     }
   }
   ```

3. **Monitore o output do Proton**:
   ```bash
   tail -f ~/.local/share/linux-coop/logs/instance_1_*.log
   ```

---

## Informações Adicionais

### Requisitos Mínimos do Sistema

- **CPU**: Intel Core i5-8400 / AMD Ryzen 3 3300X
- **RAM**: 12 GB
- **GPU**: NVIDIA GTX 1060 3GB / AMD RX 580 4GB
- **VRAM**: 3 GB
- **Storage**: 60 GB

### Links Úteis

- [ProtonDB - Elden Ring](https://www.protondb.com/app/1245620)
- [Steam Community - Elden Ring Linux](https://steamcommunity.com/app/1245620/discussions/)
- [GE-Proton Releases](https://github.com/GloriousEggroll/proton-ge-custom/releases)
- [Documentação do Wine](https://www.winehq.org/documentation)
- **[Guia: Comparar Configurações Lutris/Heroic](COMPARAR_LUTRIS_CONFIG.pt.md)** ⭐

---

## Ainda com Problemas?

Se nenhuma das soluções acima funcionou:

1. **Abra uma issue** no repositório do Linux-Coop com:
   - Output completo do erro
   - Versão do Proton/Wine
   - Distribuição Linux e versão do kernel
   - Conteúdo do arquivo de perfil
   - Logs relevantes

2. **Consulte a comunidade**:
   - [ProtonDB](https://www.protondb.com/app/1245620)
   - [Reddit r/linux_gaming](https://www.reddit.com/r/linux_gaming/)
   - [Discord do GE-Proton](https://discord.gg/6y3BdzC)

---

**Última atualização**: 2025-10-06
**Versões testadas**: Wine 10.16, Proton GE-Proton9-20+
