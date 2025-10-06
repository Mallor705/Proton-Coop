# Integração do UMU Launcher

O Linux-Coop agora suporta o uso do **UMU launcher** (Unified Launcher para jogos Windows no Linux) como alternativa à execução tradicional via Proton. Esta integração permite que você aproveite os recursos avançados do UMU, incluindo:

- Ambiente de runtime unificado similar ao Proton do Steam
- Acesso ao banco de dados umu-database para correções específicas de jogos
- Suporte para múltiplas lojas de jogos (Epic Games Store, GOG, etc.)
- Download e gerenciamento automático de versões do Proton
- Melhor compatibilidade com jogos não-Steam

## O que é o UMU?

O UMU (umu-launcher) é um launcher unificado para jogos Windows no Linux que replica o ambiente Proton do Steam fora do Steam. Ele fornece:

- Containerização do Steam Runtime Tools
- Aplicação automática de protonfixes
- Suporte a múltiplas lojas de jogos
- Nenhuma instalação do Steam necessária

Para mais informações, visite: https://github.com/Open-Wine-Components/umu-launcher

## Instalação

### Instalar o UMU Launcher

Antes de usar o UMU com o Linux-Coop, você precisa instalar o umu-launcher no seu sistema.

#### Arch Linux
```bash
pacman -S umu-launcher
```

#### Nobara
```bash
dnf install umu-launcher
```

#### Do Código Fonte
```bash
git clone https://github.com/Open-Wine-Components/umu-launcher.git
cd umu-launcher
./configure.sh --prefix=/usr
make
sudo make install
```

Para outras distribuições e métodos de instalação, veja o [guia de instalação do UMU](https://github.com/Open-Wine-Components/umu-launcher#installing).

## Configuração

Para habilitar o UMU launcher para um perfil de jogo, adicione os seguintes campos ao seu arquivo JSON de perfil:

### Configuração Básica do UMU

```json
{
  "game_name": "MeuJogo",
  "exe_path": ".steam/Steam/steamapps/common/MeuJogo/game.exe",
  "use_umu": true,
  "players": [
    {
      "account_name": "Jogador1",
      "language": "brazilian",
      "listen_port": "",
      "user_steam_id": "76561190000000001"
    },
    {
      "account_name": "Jogador2",
      "language": "brazilian",
      "listen_port": "",
      "user_steam_id": "76561190000000002"
    }
  ],
  "instance_width": 1920,
  "instance_height": 1080,
  "player_physical_device_ids": ["", ""],
  "player_mouse_event_paths": ["", ""],
  "player_keyboard_event_paths": ["", ""],
  "app_id": "12345678",
  "game_args": "",
  "env_vars": {
    "MANGOHUD": "1"
  },
  "mode": "splitscreen",
  "splitscreen": {
    "orientation": "horizontal",
    "instances": 2
  }
}
```

### Configuração Avançada do UMU

Para configuração avançada com IDs específicos de jogos e tipos de loja:

```json
{
  "game_name": "Jogo Epic Games",
  "exe_path": "/home/usuario/Games/epic-games-store/drive_c/Program Files/MeuJogo/game.exe",
  "use_umu": true,
  "umu_id": "umu-meujogo",
  "umu_store": "egs",
  "umu_proton_path": "GE-Proton",
  "players": [
    {
      "account_name": "Jogador1",
      "language": "brazilian",
      "listen_port": "",
      "user_steam_id": "76561190000000001"
    },
    {
      "account_name": "Jogador2",
      "language": "brazilian",
      "listen_port": "",
      "user_steam_id": "76561190000000002"
    }
  ],
  "instance_width": 1920,
  "instance_height": 1080,
  "player_physical_device_ids": ["", ""],
  "player_mouse_event_paths": ["", ""],
  "player_keyboard_event_paths": ["", ""],
  "app_id": "12345678",
  "game_args": "-algum-argumento",
  "env_vars": {
    "MANGOHUD": "1",
    "DXVK_ASYNC": "1"
  },
  "mode": "splitscreen",
  "splitscreen": {
    "orientation": "vertical",
    "instances": 2
  }
}
```

## Campos do Perfil UMU

### Campo Obrigatório

- **`use_umu`** (boolean): Defina como `true` para habilitar o UMU launcher em vez do Proton tradicional
  - Padrão: `false`

### Campos Opcionais

- **`umu_id`** (string): ID do jogo do [umu-database](https://umu.openwinecomponents.org/)
  - Usado para aplicar correções específicas do jogo
  - Padrão: `"umu-default"`
  - Exemplo: `"umu-borderlands3"`

- **`umu_store`** (string): Identificador da loja do jogo
  - Valores suportados: `"egs"` (Epic Games Store), `"gog"` (GOG), `"steam"`, `"none"`, etc.
  - Padrão: `"none"`
  - Usado em combinação com `umu_id` para encontrar correções apropriadas

- **`umu_proton_path`** (string): Versão específica do Proton ou caminho para usar
  - Use `"GE-Proton"` para baixar e usar automaticamente o GE-Proton mais recente
  - Ou especifique um caminho completo: `"/home/usuario/.steam/steam/compatibilitytools.d/GE-Proton8-28"`
  - Padrão: Usa UMU-Proton (Proton estável mais recente da Valve com compatibilidade UMU)

## Como o UMU Funciona com o Linux-Coop

Quando você habilita o UMU em um perfil:

1. **Verificação de Dependência**: Linux-Coop verifica se `umu-run` está instalado
2. **Configuração do Ambiente**: Variáveis de ambiente específicas do UMU são configuradas:
   - `WINEPREFIX`: Aponta para o prefixo Wine da instância do jogo
   - `GAMEID`: Definido a partir de `umu_id` ou padrão para `"umu-default"`
   - `STORE`: Definido a partir de `umu_store` ou padrão para `"none"`
   - `PROTONPATH`: Definido a partir de `umu_proton_path` se especificado
3. **Execução do Jogo**: Em vez de chamar o Proton diretamente, `umu-run` é usado
4. **Container Runtime**: UMU lida automaticamente com a configuração do container Steam Runtime
5. **Correções de Jogo**: UMU aplica protonfixes do umu-database se disponível

## Exemplos de Perfis

### Jogo da Epic Games Store

```json
{
  "game_name": "Borderlands 3",
  "exe_path": "/home/usuario/Games/epic-games-store/drive_c/Program Files/Epic Games/Borderlands 3/OakGame/Binaries/Win64/Borderlands3.exe",
  "use_umu": true,
  "umu_id": "umu-borderlands3",
  "umu_store": "egs",
  "umu_proton_path": "GE-Proton",
  "players": [
    {
      "account_name": "Jogador1",
      "user_steam_id": "76561190000000001"
    },
    {
      "account_name": "Jogador2",
      "user_steam_id": "76561190000000002"
    }
  ],
  "instance_width": 1920,
  "instance_height": 1080,
  "app_id": "530380",
  "mode": "splitscreen",
  "splitscreen": {
    "orientation": "horizontal",
    "instances": 2
  }
}
```

### Jogo GOG com Download Automático do GE-Proton Mais Recente

```json
{
  "game_name": "The Witcher 3",
  "exe_path": "/home/usuario/Games/gog/The Witcher 3/bin/x64/witcher3.exe",
  "use_umu": true,
  "umu_id": "umu-witcher3",
  "umu_store": "gog",
  "umu_proton_path": "GE-Proton",
  "players": [
    {
      "account_name": "Jogador1",
      "user_steam_id": "76561190000000001"
    },
    {
      "account_name": "Jogador2",
      "user_steam_id": "76561190000000002"
    }
  ],
  "instance_width": 1920,
  "instance_height": 1080,
  "app_id": "292030",
  "mode": "splitscreen",
  "splitscreen": {
    "orientation": "vertical",
    "instances": 2
  }
}
```

### Configuração UMU Simples (Configuração Mínima)

```json
{
  "game_name": "Meu Jogo",
  "exe_path": "/caminho/para/game.exe",
  "use_umu": true,
  "players": [
    {
      "account_name": "Jogador1",
      "user_steam_id": "76561190000000001"
    },
    {
      "account_name": "Jogador2",
      "user_steam_id": "76561190000000002"
    }
  ],
  "instance_width": 1920,
  "instance_height": 1080,
  "mode": "splitscreen",
  "splitscreen": {
    "orientation": "horizontal",
    "instances": 2
  }
}
```

## Comparando Proton vs UMU

### Modo Proton Tradicional
```json
{
  "use_umu": false,
  "proton_version": "GE-Proton10-4"
}
```

### Modo UMU
```json
{
  "use_umu": true,
  "umu_proton_path": "GE-Proton"
}
```

## Benefícios de Usar o UMU

1. **Steam Não Necessário**: Execute jogos sem ter o Steam instalado
2. **Correções Unificadas**: Acesso ao banco de dados centralizado de correções de jogos
3. **Suporte Multi-Loja**: Melhor suporte para Epic, GOG e outras lojas
4. **Atualizações Automáticas**: UMU pode baixar versões do Proton automaticamente
5. **Isolamento de Container**: Usa container Steam Runtime para melhor compatibilidade
6. **Integração Protonfixes**: Aplicação automática de ajustes específicos de jogos

## Solução de Problemas

### Erro de UMU não encontrado
```
DependencyError: umu-run is not installed
```
**Solução**: Instale o umu-launcher para sua distribuição (veja a seção Instalação)

### O jogo não inicia com o UMU
**Solução**: Verifique os logs em `~/.local/share/linux-coop/logs/` para mensagens de erro detalhadas

### Quer usar uma versão específica do Proton
**Solução**: Defina `umu_proton_path` para o caminho completo da sua instalação do Proton

### Precisa de correções específicas do jogo
**Solução**: Verifique o [umu-database](https://umu.openwinecomponents.org/) para os valores `umu_id` e `store` do seu jogo

## Recursos Adicionais

- [GitHub do UMU Launcher](https://github.com/Open-Wine-Components/umu-launcher)
- [Banco de Dados UMU](https://umu.openwinecomponents.org/)
- [Documentação do UMU](https://github.com/Open-Wine-Components/umu-launcher/blob/main/docs/umu.1.scd)
- [FAQ do UMU](https://github.com/Open-Wine-Components/umu-launcher/wiki/Frequently-asked-questions-(FAQ))

## Suporte

Se você encontrar problemas com a integração do UMU, por favor:

1. Verifique os logs em `~/.local/share/linux-coop/logs/`
2. Verifique se o UMU está instalado corretamente com `umu-run --help`
3. Teste o jogo com o UMU padrão antes de usá-lo com o Linux-Coop
4. Relate problemas no [GitHub do Linux-Coop](https://github.com/Mallor705/Linux-Coop/issues)
