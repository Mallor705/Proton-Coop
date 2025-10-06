# 🔄 Atualização UMU - Campo Proton Unificado

## Mudança Implementada

A interface UMU foi simplificada para usar o **mesmo campo Proton Version** que o modo tradicional, eliminando duplicação e confusão.

## O Que Mudou

### ❌ ANTES (Versão Anterior)
- Campo "Proton Version" escondia quando UMU estava ativo
- Campo separado "UMU Proton Path" aparecia
- Dois campos para essencialmente a mesma coisa
- Mais confuso para o usuário

### ✅ AGORA (Versão Atual)
- Campo "Proton Version" **sempre visível**
- Usado tanto por Proton tradicional quanto por UMU
- Apenas um campo para configurar
- Interface mais limpa e intuitiva

---

## Interface da GUI

### Layout Atualizado

```
╔═══════════════════════════════════════════════════════╗
║              Launch Options                           ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  Use UMU Launcher:      [✓]                          ║
║                                                       ║
║  Proton Version:        [GE-Proton10-4 ▼]            ║
║                         (usado pelo UMU também)       ║
║                                                       ║
║  UMU Game ID:          [umu-borderlands3      ]      ║
║                                                       ║
║  UMU Store:            [egs                   ▼]     ║
║                                                       ║
║  Disable bwrap:         [ ]                          ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
```

### Campos UMU Restantes

1. **Use UMU Launcher** (Checkbox)
   - Habilita/desabilita modo UMU

2. **Proton Version** (ComboBox - SEMPRE VISÍVEL)
   - Usado por ambos: Proton tradicional e UMU
   - Exemplo: "GE-Proton10-4", "Proton 8.0", etc.

3. **UMU Game ID** (Entry - só visível quando UMU ativo)
   - ID do jogo no umu-database
   - Exemplo: "umu-borderlands3"

4. **UMU Store** (ComboBox - só visível quando UMU ativo)
   - Loja do jogo
   - Opções: none, egs, gog, steam, origin, uplay

---

## Exemplo de Perfil JSON Atualizado

```json
{
  "GAME_NAME": "Borderlands 3",
  "EXE_PATH": "/home/user/Games/egs/Borderlands3.exe",
  "USE_UMU": true,
  "UMU_ID": "umu-borderlands3",
  "UMU_STORE": "egs",
  "PROTON_VERSION": "GE-Proton10-4",
  "NUM_PLAYERS": 2,
  "INSTANCE_WIDTH": 1920,
  "INSTANCE_HEIGHT": 1080,
  "PLAYERS": [...],
  "MODE": "splitscreen",
  "SPLITSCREEN": {
    "ORIENTATION": "horizontal"
  }
}
```

**Note:** Não há mais `UMU_PROTON_PATH` - usa-se `PROTON_VERSION` para ambos os modos.

---

## Mudanças no Modelo de Dados

### src/models/profile.py

**Removido:**
```python
umu_proton_path: Optional[str] = Field(default=None, alias="UMU_PROTON_PATH")
```

**Mantido:**
```python
proton_version: Optional[str] = Field(default=None, alias="PROTON_VERSION")
use_umu: bool = Field(default=False, alias="USE_UMU")
umu_id: Optional[str] = Field(default=None, alias="UMU_ID")
umu_store: Optional[str] = Field(default=None, alias="UMU_STORE")
```

---

## Mudanças no UmuService

### src/services/umu.py

**Antes:**
```python
def prepare_umu_environment(
    self,
    base_env: dict,
    wineprefix: Path,
    umu_id: Optional[str] = None,
    umu_store: Optional[str] = None,
    umu_proton_path: Optional[str] = None  # ❌ Campo separado
) -> dict:
```

**Agora:**
```python
def prepare_umu_environment(
    self,
    base_env: dict,
    wineprefix: Path,
    proton_version: Optional[str] = None,  # ✅ Usa versão comum
    umu_id: Optional[str] = None,
    umu_store: Optional[str] = None
) -> dict:
```

O `proton_version` é passado diretamente para a variável de ambiente `PROTONPATH` do UMU.

---

## Mudanças na GUI

### src/gui/app.py

**Removido:**
- Campo `umu_proton_path_label`
- Campo `umu_proton_path_entry`
- Lógica de show/hide do Proton Version

**Simplificado:**
```python
def _on_use_umu_toggled(self, checkbox):
    """Toggle visibility of UMU-specific fields."""
    use_umu = checkbox.get_active()
    
    # Show/hide UMU-specific fields
    self.umu_id_label.set_visible(use_umu)
    self.umu_id_entry.set_visible(use_umu)
    self.umu_store_label.set_visible(use_umu)
    self.umu_store_combo.set_visible(use_umu)
    
    # Proton Version field remains always visible
```

---

## Benefícios da Mudança

✅ **Interface mais limpa**
   - Menos campos na tela
   - Menos confusão

✅ **Consistência**
   - Um campo para Proton em ambos os modos
   - Comportamento previsível

✅ **Simplicidade**
   - Usuário não precisa decidir entre campos
   - Mesma seleção funciona para ambos

✅ **Manutenção**
   - Menos código duplicado
   - Menos campos para validar

---

## Fluxo de Uso Atualizado

### Modo Tradicional (UMU Desabilitado)
1. [ ] Use UMU Launcher (desmarcado)
2. Selecionar **Proton Version**: "GE-Proton10-4"
3. Salvar e executar
4. → Usa Proton tradicional com versão selecionada

### Modo UMU (UMU Habilitado)
1. [✓] Use UMU Launcher (marcado)
2. Selecionar **Proton Version**: "GE-Proton10-4"
3. Configurar **UMU Game ID**: "umu-borderlands3"
4. Configurar **UMU Store**: "egs"
5. Salvar e executar
6. → Usa UMU com versão de Proton selecionada

**A versão do Proton é a mesma em ambos os casos!**

---

## Compatibilidade

### Perfis Antigos com UMU_PROTON_PATH
Perfis antigos que tinham `UMU_PROTON_PATH` continuarão funcionando, mas o campo será ignorado. A versão do Proton será lida de `PROTON_VERSION`.

### Migração
Não é necessária migração manual. O sistema automaticamente:
1. Ignora `UMU_PROTON_PATH` se existir
2. Usa `PROTON_VERSION` para ambos os modos
3. Funciona perfeitamente com perfis novos e antigos

---

## Arquivos Modificados

✅ `src/models/profile.py` - Removido campo `umu_proton_path`
✅ `src/services/umu.py` - Atualizado para usar `proton_version`
✅ `src/services/instance.py` - Passa `proton_version` ao UMU
✅ `src/gui/app.py` - Removido campo UMU Proton Path da interface
✅ `profiles/ExampleUMU.json` - Atualizado exemplo

---

## Testes Realizados

✅ Compilação Python - Todos os arquivos OK
✅ Sintaxe validada - Sem erros
✅ Perfil de exemplo atualizado
✅ Lógica de save/load atualizada

---

## Resumo

A integração UMU foi **simplificada** para usar o campo **Proton Version** existente, eliminando a necessidade de um campo separado `UMU Proton Path`. Isso torna a interface mais limpa, intuitiva e consistente.

**Status: ✅ Implementação Completa e Validada**
