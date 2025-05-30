import json
from pathlib import Path
from pydantic import BaseModel, Field, validator, ConfigDict
from typing import Optional, List
from ..core.exceptions import ProfileNotFoundError, ExecutableNotFoundError

class PlayerInstanceConfig(BaseModel):
    """Configurações específicas para uma instância de jogador."""
    account_name: Optional[str] = None
    language: Optional[str] = None
    listen_port: Optional[str] = None
    user_steam_id: Optional[str] = None

class GameProfile(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    """Modelo de perfil de jogo, contendo configurações e validações para execução multi-instância."""
    game_name: str = Field(..., alias="GAME_NAME")
    exe_path: Path = Field(..., alias="EXE_PATH")
    proton_version: Optional[str] = Field(default=None, alias="PROTON_VERSION")
    num_players: int = Field(..., alias="NUM_PLAYERS")
    instance_width: int = Field(..., alias="INSTANCE_WIDTH")
    instance_height: int = Field(..., alias="INSTANCE_HEIGHT")
    player_physical_device_ids: List[str] = Field(default_factory=list, alias="PLAYER_PHYSICAL_DEVICE_IDS")
    player_mouse_event_paths: List[str] = Field(default_factory=list, alias="PLAYER_MOUSE_EVENT_PATHS")
    player_keyboard_event_paths: List[str] = Field(default_factory=list, alias="PLAYER_KEYBOARD_EVENT_PATHS")
    app_id: Optional[str] = Field(default=None, alias="APP_ID")
    game_args: Optional[str] = Field(default=None, alias="GAME_ARGS")
    is_native: bool = False
    
    # Novo campo para configurações por jogador, usando alias "players" para o JSON
    player_configs: Optional[List[PlayerInstanceConfig]] = Field(default=None, alias="players")

    @validator('num_players')
    def validate_num_players(cls, v):
        """Valida se o número de jogadores é suportado (mínimo 2)."""
        if v < 2:
            raise ValueError("O número mínimo suportado é 2 jogadores")
        return v
    
    @validator('exe_path')
    def validate_exe_path(cls, v, values):
        """Valida se o caminho do executável existe."""
        # Se exe_path for uma string (vindo de JSON), converte para Path
        path_v = Path(v)
        if not path_v.exists():
            raise ExecutableNotFoundError(f"Game executable not found: {path_v}")
        return path_v

    @classmethod
    def load_from_file(cls, profile_path: Path) -> "GameProfile":
        """Carrega um perfil de jogo a partir de um arquivo (.profile ou .json)."""
        if not profile_path.exists():
            raise ProfileNotFoundError(f"Profile not found: {profile_path}")

        if profile_path.suffix == '.json':
            with open(profile_path, 'r') as f:
                data = json.load(f)
            
            # Pydantic pode lidar com a conversão de tipos e aliases diretamente do dicionário JSON
            # No entanto, precisamos garantir que os campos que são Path no modelo sejam convertidos se vierem como string do JSON.
            # O validador de exe_path já cuida disso.
            # Para outros campos Path (se houver no futuro), validadores semelhantes seriam necessários.
            
            # Detecção de 'is_native' para JSON
            exe_path_str = data.get('exe_path') # Usando o nome do campo Python, não o alias
            is_native = False
            if exe_path_str:
                if Path(exe_path_str).suffix.lower() != '.exe':
                    is_native = True
            data['is_native'] = is_native # Adiciona ao dict antes de passar para o Pydantic

            # Se 'num_players' não estiver no JSON mas 'players' estiver, infere num_players
            if 'num_players' not in data and 'players' in data and isinstance(data['players'], list):
                data['num_players'] = len(data['players'])
            
            # Pydantic vai usar os aliases definidos nos Fields se eles existirem no JSON,
            # caso contrário, usará os nomes dos campos.
            # Para o JSON que vimos, os nomes dos campos são snake_case, então não precisamos de alias no Field para JSON.
            # O alias nos Fields é mais para o formato .profile.
            # Para player_configs, o alias="players" está correto para o JSON.
            return cls(**data)
        
        elif profile_path.suffix == '.profile':
            profile_vars = {}
            array_key = None
            array_values = []
            raw_players_section = []
            capturing_players = False

            # Mapa de chaves do .profile para nomes de campo do modelo Pydantic
            key_map = {
                "GAME_NAME": "game_name",
                "EXE_PATH": "exe_path",
                "PROTON_VERSION": "proton_version",
                "NUM_PLAYERS": "num_players",
                "INSTANCE_WIDTH": "instance_width",
                "INSTANCE_HEIGHT": "instance_height",
                "PLAYER_PHYSICAL_DEVICE_IDS": "player_physical_device_ids",
                "PLAYER_MOUSE_EVENT_PATHS": "player_mouse_event_paths",
                "PLAYER_KEYBOARD_EVENT_PATHS": "player_keyboard_event_paths",
                "APP_ID": "app_id",
                "GAME_ARGS": "game_args"
                # Adicione outros mapeamentos se necessário
            }

            with open(profile_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    if line.upper().startswith('PLAYERS='): # Início da seção PLAYERS
                        capturing_players = True
                        # Remove 'PLAYERS=' e o que vier depois na mesma linha (ex: '{')
                        line_content_after_players_eq = line.split('=', 1)[1].strip()
                        if line_content_after_players_eq: # Se houver algo como '{' na mesma linha
                             if line_content_after_players_eq != "{": # Se for apenas "PLAYERS={"
                                raw_players_section.append(line_content_after_players_eq)
                        continue
                    
                    if capturing_players:
                        # Supondo que a seção PLAYERS termina com uma linha contendo apenas '}' ou no final do arquivo.
                        # Esta é uma heurística frágil. O formato no .profile para PLAYERS é problemático.
                        # Se a linha for apenas '}' e for o fim de um bloco, paramos.
                        # Por agora, vamos apenas capturar tudo até o fim ou até uma nova variável.
                        # O ideal seria que PLAYERS no .profile fosse um JSON string ou similar.
                        if '=' in line and not array_key: # Nova atribuição, então PLAYERS terminou
                            capturing_players = False
                            # Processar a linha atual normalmente
                        else:
                            raw_players_section.append(line)
                            continue # Não processa mais esta linha como uma var normal

                    if line.endswith('(') and '=' in line:
                        raw_array_key = line.split('=')[0].strip() # ex: PLAYER_PHYSICAL_DEVICE_IDS
                        array_key = key_map.get(raw_array_key, raw_array_key) # Converte para nome do campo Pydantic
                        array_values = []
                        continue
                    if array_key: # array_key já é o nome do campo Pydantic (snake_case)
                        if line.endswith(')'):
                            # array_key já está correto (ex: player_physical_device_ids)
                            profile_vars[array_key] = [str(val).strip().strip('\"\\\'') for val in array_values]
                            array_key = None
                            array_values = []
                            continue
                        value = line.split('#')[0].strip().strip('\"\\\'')
                        array_values.append(value)
                        continue
                    if '=' in line:
                        raw_key, value = line.split('=', 1)
                        raw_key = raw_key.strip()
                        value = value.strip().strip('\"\\\'')
                        
                        # Converte a chave para o nome do campo Pydantic (snake_case)
                        key = key_map.get(raw_key, raw_key) # Default para raw_key se não estiver no mapa
                        
                        if key == 'num_players':
                            profile_vars[key] = int(value)
                        elif key == 'instance_width':
                            profile_vars[key] = int(value)
                        elif key == 'instance_height':
                            profile_vars[key] = int(value)
                        elif key == 'exe_path':
                            profile_vars[key] = Path(value)
                        # Para outras chaves (game_name, proton_version, app_id, game_args),
                        # que já são strings, nenhuma conversão de tipo é necessária aqui.
                        # Elas já foram mapeadas para seus nomes de campo snake_case.
                        else:
                            profile_vars[key] = value # Armazena com a chave snake_case


            # Detecta se é nativo
            exe_p_val = profile_vars.get('exe_path') # Agora usa a chave snake_case
            is_native = False
            if exe_p_val and isinstance(Path(exe_p_val), Path) and Path(exe_p_val).suffix.lower() != '.exe':
                is_native = True
            profile_vars['is_native'] = is_native

            # Tentativa de parsear a seção PLAYERS se algo foi capturado
            # Esta parte é experimental devido ao formato irregular no .profile
            if raw_players_section:
                player_configs_data = []
                try:
                    # Tenta juntar e tratar como uma lista de JSONs, removendo vírgula final se houver
                    full_players_str = "".join(raw_players_section).strip()
                    if full_players_str.endswith(','):
                        full_players_str = full_players_str[:-1]
                    
                    # Adiciona colchetes se não for uma lista JSON completa
                    if not full_players_str.startswith('['):
                        full_players_str = '[' + full_players_str
                    if not full_players_str.endswith(']'):
                        full_players_str = full_players_str + ']'
                    
                    # Substitui aspas simples por aspas duplas para validade JSON (com cuidado)
                    # Isso é arriscado se aspas simples forem usadas dentro dos valores.
                    # Uma abordagem mais robusta seria usar uma biblioteca de parsing mais flexível ou ast.literal_eval
                    # full_players_str = full_players_str.replace(\"'\", '\"') # Comentado por ser arriscado

                    # Usando ast.literal_eval que é mais seguro para strings Python-like
                    import ast
                    parsed_players_list = ast.literal_eval(full_players_str)
                    
                    if isinstance(parsed_players_list, list):
                        for player_data_dict in parsed_players_list:
                            player_configs_data.append(PlayerInstanceConfig(**player_data_dict))
                        profile_vars['players'] = player_configs_data # Usa o alias 'players' para player_configs
                except Exception as e:
                    print(f"[AVISO] Não foi possível parsear a seção PLAYERS do arquivo .profile: {e}")
                    print(f"[AVISO] String PLAYERS capturada: '{''.join(raw_players_section)}'")
                    # player_configs permanecerá None ou default
            
            # Agora profile_vars contém chaves snake_case, e Pydantic usará populate_by_name=True.
            # Os aliases nos Fields não são mais usados para popular, mas ainda podem ser úteis para serialização
            # ou se quisermos que o schema JSON gerado use os aliases.
            return cls(**profile_vars)
        else:
            raise ValueError(f"Unsupported profile file extension: {profile_path.suffix}")

    # Adicionar getter para num_players para garantir consistência caso player_configs seja a fonte da verdade
    @property
    def effective_num_players(self) -> int:
        if self.player_configs:
            return len(self.player_configs)
        return self.num_players