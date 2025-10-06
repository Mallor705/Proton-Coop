# Solução de Problemas - Elden Ring

## Erro: Page Fault on Read Access (0x0000000000000000)

### Descrição do Erro

Ao executar o Elden Ring via Wine/Proton, você pode encontrar o seguinte erro:

```
Unhandled exception: page fault on read access to 0x0000000000000000 in 64-bit code
```

Este erro indica uma tentativa de acesso a memória nula (null pointer dereference), onde o jogo tenta ler dados de um endereço de memória inválido (0x0000000000000000).

### Análise Técnica

- **Instrução que falhou**: `movq (%rcx), %rax`
- **Registrador RCX**: Contém 0x0000000000000000 (ponteiro nulo)
- **Local do crash**: `eldenring+0x1e9f53b`
- **Ambiente**: Wine 10.16, Linux kernel 6.17.0-4-cachyos

O erro ocorre porque o código do jogo está tentando desreferenciar um ponteiro nulo, o que geralmente indica:
1. Módulo/componente não inicializado corretamente
2. DLL faltante ou incompatível
3. Problema com anti-cheat (EasyAntiCheat)
4. Incompatibilidade com a versão do Wine/Proton

---

## Soluções Possíveis

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

### 🔧 Solução 2: Configurar EasyAntiCheat

O Elden Ring usa EasyAntiCheat, que pode causar problemas no Linux.

**Opção A: Desabilitar EasyAntiCheat (para jogo offline)**

1. Navegue até a pasta do jogo:
   ```bash
   cd ~/.steam/steam/steamapps/common/ELDEN\ RING/Game/
   ```

2. Renomeie o executável do EAC:
   ```bash
   mv start_protected_game.exe start_protected_game.exe.bak
   ```

3. Execute diretamente o `eldenring.exe` no perfil:
   ```json
   {
     "exe_path": ".steam/steam/steamapps/common/ELDEN RING/Game/eldenring.exe",
     ...
   }
   ```

**Opção B: Usar EAC Bypass (incluído no Linux-Coop)**

O projeto já inclui DLLs do EAC Bypass em `src/utils/EAC Bypass/`.

1. Copie as DLLs para a pasta do jogo:
   ```bash
   cp src/utils/EAC\ Bypass/EasyAntiCheat_x64.dll \
      ~/.steam/steam/steamapps/common/ELDEN\ RING/Game/
   ```

2. Configure o WINEDLLOVERRIDES no perfil:
   ```json
   {
     "env_vars": {
       "WINEDLLOVERRIDES": "EasyAntiCheat_x64=n,b"
     },
     ...
   }
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

### 🔧 Solução 4: Reinstalar o Prefix do Wine

Às vezes o prefix do Wine pode ficar corrompido:

1. **Backup dos saves** (se houver):
   ```bash
   cp -r ~/Games/linux-coop/prefixes/Elden\ Ring/instance_1/pfx/drive_c/users/*/AppData/Roaming/EldenRing/ ~/backup_elden_saves/
   ```

2. **Remover o prefix existente**:
   ```bash
   rm -rf ~/Games/linux-coop/prefixes/Elden\ Ring/
   ```

3. **Executar o jogo novamente** para criar um prefix limpo

### 🔧 Solução 5: Instalar Dependências do Wine

Certifique-se de que as dependências necessárias estão instaladas:

```bash
# Via Winetricks (se disponível)
winetricks -q vcrun2019 vcrun2022 dotnet48 dxvk

# Ou via Protontricks (se estiver usando Steam)
protontricks 1245620 -q vcrun2019 vcrun2022
```

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

## Exemplo de Perfil Completo para Elden Ring

```json
{
  "game_name": "Elden Ring",
  "exe_path": ".steam/steam/steamapps/common/ELDEN RING/Game/eldenring.exe",
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
  "proton_version": "GE-Proton9-20",
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
  "game_args": "-dx12",
  "use_goldberg_emu": false,
  "env_vars": {
    "WINEDLLOVERRIDES": "EasyAntiCheat_x64=n,b",
    "PROTON_FORCE_LARGE_ADDRESS_AWARE": "1",
    "WINE_LARGE_ADDRESS_AWARE": "1",
    "DXVK_ASYNC": "1",
    "PROTON_NO_ESYNC": "0",
    "PROTON_NO_FSYNC": "0",
    "MANGOHUD": "0"
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

## Checklist de Diagnóstico

Execute estas verificações em ordem:

- [ ] Versão do Proton é compatível (GE-Proton9-20+)
- [ ] EasyAntiCheat configurado corretamente (bypass ou desabilitado)
- [ ] Arquivos do jogo verificados (via Steam)
- [ ] Drivers gráficos atualizados
- [ ] Variáveis de ambiente configuradas
- [ ] Prefix do Wine limpo/recriado
- [ ] Dependências do Wine instaladas (vcrun2019, vcrun2022)
- [ ] Argumentos de lançamento apropriados (-dx12 ou -dx11)

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
