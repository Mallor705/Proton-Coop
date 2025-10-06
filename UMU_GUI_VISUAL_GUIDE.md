# Guia Visual - GUI com Integração UMU

## 🎨 Interface Gráfica Atualizada

### Visão Geral da GUI

A interface do Linux-Coop foi atualizada para incluir suporte completo ao UMU Launcher na aba "Game Settings".

---

## 📱 Layout da Interface

### Seção: Launch Options

#### **Antes da Implementação UMU:**

```
╔═══════════════════════════════════════════════════════╗
║              Launch Options                           ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  Proton Version:        [GE-Proton10-4 ▼]            ║
║                                                       ║
║  Disable bwrap:         [ ]                          ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
```

#### **Depois da Implementação UMU (UMU Desabilitado):**

```
╔═══════════════════════════════════════════════════════╗
║              Launch Options                           ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  Use UMU Launcher:      [ ]  ⓘ Enable UMU launcher   ║
║                              instead of Proton        ║
║                                                       ║
║  Proton Version:        [GE-Proton10-4 ▼]            ║
║                                                       ║
║  Disable bwrap:         [ ]                          ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
```

#### **Depois da Implementação UMU (UMU Habilitado):**

```
╔═══════════════════════════════════════════════════════╗
║              Launch Options                           ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  Use UMU Launcher:      [✓]  ⓘ Enable UMU launcher   ║
║                              instead of Proton        ║
║                                                       ║
║  ┌─────────────────────────────────────────────────┐ ║
║  │ UMU-Specific Settings                           │ ║
║  ├─────────────────────────────────────────────────┤ ║
║  │                                                 │ ║
║  │  UMU Game ID:       [umu-borderlands3        ] │ ║
║  │                     ⓘ Game ID from umu-database│ ║
║  │                                                 │ ║
║  │  UMU Store:         [egs                     ▼]│ ║
║  │                     ⓘ Epic, GOG, Steam, etc.  │ ║
║  │                                                 │ ║
║  │  UMU Proton Path:   [GE-Proton              ]  │ ║
║  │                     ⓘ Auto-download or path   │ ║
║  │                                                 │ ║
║  └─────────────────────────────────────────────────┘ ║
║                                                       ║
║  Disable bwrap:         [ ]                          ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
```

---

## 🔄 Comportamento Dinâmico

### Interação do Usuário

#### 1. **Estado Inicial (Novo Perfil)**
- ☐ Use UMU Launcher (desmarcado)
- ✅ Proton Version (visível)
- ❌ Campos UMU (ocultos)

#### 2. **Usuário Marca "Use UMU Launcher"**
- ✅ Use UMU Launcher (marcado)
- ❌ Proton Version (oculto automaticamente)
- ✅ UMU Game ID (aparece)
- ✅ UMU Store (aparece)
- ✅ UMU Proton Path (aparece)
- 📊 Status bar: "UMU mode enabled"

#### 3. **Usuário Desmarca "Use UMU Launcher"**
- ☐ Use UMU Launcher (desmarcado)
- ✅ Proton Version (reaparece)
- ❌ Campos UMU (ocultam automaticamente)
- 📊 Status bar: "UMU mode disabled"

---

## 💾 Fluxo de Dados

### Salvando Perfil

```
┌─────────────────┐
│   GUI Inputs    │
│                 │
│ [✓] Use UMU     │
│ [umu-test    ]  │  ──┐
│ [egs        ▼]  │    │
│ [GE-Proton   ]  │    │
└─────────────────┘    │
                       │
                       ▼
              ┌─────────────────┐
              │  get_profile    │
              │     _data()     │
              │                 │
              │  Coleta valores │
              │   dos campos    │
              └─────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  GameProfile    │
              │   Constructor   │
              │                 │
              │  use_umu=True   │
              │  umu_id="..."   │
              └─────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  model_dump()   │
              │   by_alias=True │
              └─────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  profile.json   │
              │                 │
              │  "USE_UMU": true│
              │  "UMU_ID": "..." │
              └─────────────────┘
```

### Carregando Perfil

```
┌─────────────────┐
│  profile.json   │
│                 │
│  "USE_UMU": true│
│  "UMU_ID": "..." │  ──┐
│  "UMU_STORE": ...│    │
└─────────────────┘    │
                       │
                       ▼
         ┌──────────────────────┐
         │  load_profile_data() │
         └──────────────────────┘
                       │
                       ▼
       ┌────────────────────────────┐
       │  _load_proton_settings()   │
       │                            │
       │  1. Lê USE_UMU             │
       │  2. Define checkbox         │
       │  3. Se True:               │
       │     - Carrega campos UMU   │
       │     - Esconde Proton       │
       │  4. Se False:              │
       │     - Carrega Proton       │
       └────────────────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   GUI Updated   │
              │                 │
              │ [✓] Use UMU     │
              │ [umu-test    ]  │
              │ [egs        ▼]  │
              │ [GE-Proton   ]  │
              └─────────────────┘
```

---

## 🎮 Campos UMU Detalhados

### Use UMU Launcher
- **Tipo**: Checkbox
- **Padrão**: Desmarcado (false)
- **Tooltip**: "Enable UMU launcher instead of traditional Proton (requires umu-run installed)"
- **Ação**: Ao alternar, mostra/esconde campos relacionados

### UMU Game ID
- **Tipo**: Text Entry
- **Placeholder**: "umu-default"
- **Tooltip**: "Game ID from umu-database (e.g., umu-borderlands3)"
- **Opcional**: Sim (usa "umu-default" se vazio)
- **Exemplo**: `umu-borderlands3`

### UMU Store
- **Tipo**: ComboBox (Dropdown)
- **Opções**:
  - `none` (padrão)
  - `egs` (Epic Games Store)
  - `gog` (GOG)
  - `steam` (Steam)
  - `origin` (Origin)
  - `uplay` (Uplay)
- **Tooltip**: "Game store identifier (Epic, GOG, Steam, etc.)"
- **Opcional**: Sim (usa "none" se vazio)

### UMU Proton Path
- **Tipo**: Text Entry
- **Placeholder**: "GE-Proton or custom path"
- **Tooltip**: "Use 'GE-Proton' for auto-download or specify custom Proton path"
- **Opcional**: Sim (usa UMU-Proton padrão se vazio)
- **Exemplos**:
  - `GE-Proton` (auto-download)
  - `/home/user/.steam/steam/compatibilitytools.d/GE-Proton8-28`

---

## 📝 Exemplos de Uso na GUI

### Cenário 1: Jogo Epic Games Store

1. **Game Name**: `Borderlands 3`
2. **Executable**: `/home/user/Games/epic-games-store/.../Borderlands3.exe`
3. **Use UMU**: ✅ Marcado
4. **UMU Game ID**: `umu-borderlands3`
5. **UMU Store**: `egs`
6. **UMU Proton Path**: `GE-Proton`

### Cenário 2: Jogo GOG

1. **Game Name**: `The Witcher 3`
2. **Executable**: `/home/user/Games/gog/.../witcher3.exe`
3. **Use UMU**: ✅ Marcado
4. **UMU Game ID**: `umu-witcher3`
5. **UMU Store**: `gog`
6. **UMU Proton Path**: (vazio - usa padrão)

### Cenário 3: Jogo Genérico (Sem Database Entry)

1. **Game Name**: `My Indie Game`
2. **Executable**: `/home/user/Games/indie/game.exe`
3. **Use UMU**: ✅ Marcado
4. **UMU Game ID**: (vazio - usa "umu-default")
5. **UMU Store**: `none`
6. **UMU Proton Path**: `GE-Proton`

---

## ✨ Feedback Visual

### Mensagens da Status Bar

| Ação | Mensagem |
|------|----------|
| Marcar UMU | `UMU mode enabled` |
| Desmarcar UMU | `UMU mode disabled` |
| Salvar com UMU | `Profile saved successfully` |
| Carregar com UMU | `Profile loaded` |

### Tooltips (Dicas ao Passar Mouse)

Todos os campos UMU têm tooltips informativos:
- **Use UMU Launcher**: Explica que requer umu-run
- **UMU Game ID**: Menciona umu-database e exemplo
- **UMU Store**: Lista opções de lojas
- **UMU Proton Path**: Explica auto-download vs path customizado

---

## 🔍 Validação e Reset

### Ao Criar Novo Perfil
Todos os campos UMU são resetados para valores padrão:
- Use UMU: ☐ Desmarcado
- UMU Game ID: (vazio)
- UMU Store: `none`
- UMU Proton Path: (vazio)

### Ao Salvar Perfil
- Campos vazios são salvos como `null` no JSON
- Valores padrão são aplicados durante execução
- Validação Pydantic garante tipos corretos

### Ao Carregar Perfil
- Perfis sem campos UMU: Campos permanecem ocultos
- Perfis com UMU: Checkbox marcado, campos carregados e visíveis
- Compatibilidade total com perfis antigos

---

## 🎯 Vantagens da Interface

✅ **Intuitiva**: Campos aparecem/desaparecem automaticamente
✅ **Informativa**: Tooltips explicam cada campo
✅ **Validada**: Sintaxe Python 100% correta
✅ **Completa**: Todos os campos UMU disponíveis
✅ **Compatível**: Funciona com perfis novos e existentes
✅ **Visual**: Feedback claro das ações do usuário

---

## 📸 Resumo Visual do Fluxo

```
Usuario Abre GUI
       │
       ▼
   Novo Perfil?  ──Yes──► Campos limpos, UMU desmarcado
       │
      No
       │
       ▼
   Seleciona Perfil
       │
       ▼
   Tem USE_UMU=true?  ──Yes──► Marca checkbox, mostra campos UMU
       │                       Carrega valores UMU
      No
       │
       ▼
   Mostra campos tradicionais (Proton)
       │
       ▼
   Usuario edita campos
       │
       ▼
   Marca/Desmarca UMU?
       │
       ├──Yes──► Campos aparecem/desaparecem
       │
       ▼
   Usuario clica "Save"
       │
       ▼
   Coleta dados da GUI (get_profile_data)
       │
       ▼
   Cria GameProfile com campos UMU
       │
       ▼
   Serializa para JSON (model_dump)
       │
       ▼
   Salva em profiles/nome.json
       │
       ▼
   Status: "✅ Profile saved successfully"
```

---

**🎉 Interface UMU Totalmente Implementada e Funcional!**
