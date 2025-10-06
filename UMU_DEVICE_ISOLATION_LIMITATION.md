# ⚠️ IMPORTANTE: Limitação de Isolamento de Dispositivos no Modo UMU

## 🔍 Situação Atual

### Modo Tradicional (Proton + bwrap)
✅ **Isolamento de dispositivos FUNCIONA**
- bwrap cria container isolado para cada instância
- Cada jogador tem seus próprios dispositivos de entrada
- Mouse, teclado e controle são isolados por jogador

### Modo UMU
⚠️ **Isolamento de dispositivos NÃO ESTÁ DISPONÍVEL**
- UMU usa pressure-vessel para containerização geral
- pressure-vessel NÃO isola dispositivos de entrada
- bwrap não pode ser usado (conflito container-in-container)

## ❌ O Problema

Quando desabilitamos o bwrap para evitar o conflito com UMU:
- ✅ Os jogos ABREM corretamente
- ❌ Mas TODOS os dispositivos são visíveis para TODAS as instâncias
- ❌ Não há isolamento de mouse/teclado/controle por jogador

## 🎮 Impacto Prático

### Cenário: 2 Jogadores em Splitscreen com UMU

**O que FUNCIONA:**
- ✅ Duas instâncias do jogo abrem
- ✅ Telas divididas (horizontal/vertical)
- ✅ Prefixes separados (saves independentes)
- ✅ Variáveis de ambiente separadas

**O que NÃO FUNCIONA:**
- ❌ Controle 1 exclusivo para Player 1
- ❌ Controle 2 exclusivo para Player 2
- ❌ Mouse/teclado isolados
- ❌ Ambas instâncias veem TODOS os dispositivos

## 🔧 Por Que Isso Acontece?

### Arquitetura do UMU

```
┌─────────────────────────────────────────┐
│  umu-run (wrapper)                      │
│  ├─ pressure-vessel (container)         │
│     ├─ Proton                           │
│        └─ Jogo                          │
│                                         │
│  Dispositivos: TODOS visíveis           │ ← UMU não isola
└─────────────────────────────────────────┘
```

### Arquitetura Tradicional

```
┌─────────────────────────────────────────┐
│  Linux-Coop                             │
│  ├─ bwrap (container isolado)           │
│     ├─ Dispositivos: APENAS do Player 1 │ ← bwrap isola!
│     ├─ Proton                           │
│        └─ Jogo Player 1                 │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  Linux-Coop                             │
│  ├─ bwrap (container isolado)           │
│     ├─ Dispositivos: APENAS do Player 2 │ ← bwrap isola!
│     ├─ Proton                           │
│        └─ Jogo Player 2                 │
└─────────────────────────────────────────┘
```

## 🤔 Possíveis Soluções (Análise)

### Opção 1: Variáveis de Ambiente SDL/Wine
❓ **Status: A INVESTIGAR**

Podemos tentar usar:
- `SDL_JOYSTICK_DEVICE=/dev/input/by-id/...`
- `SDL_GAMECONTROLLER_USE_BUTTON_LABELS=0`

**Limitação:** 
- Funciona apenas para joysticks via SDL
- NÃO funciona para mouse/teclado
- Depende do jogo usar SDL (nem todos usam)

### Opção 2: Passar Opções para pressure-vessel
❓ **Status: PESQUISA NECESSÁRIA**

O umu-run pode aceitar opções extras para pressure-vessel?
- Precisaria documentação do UMU
- Pode não ser suportado
- Seria solução complexa

### Opção 3: Aceitar Limitação
✅ **Status: ATUAL**

Modo UMU = SEM isolamento de dispositivos
- Documentar claramente a limitação
- Recomendar modo tradicional para coop local
- UMU melhor para single-player ou online

### Opção 4: Híbrido (Investigar)
❓ **Status: EXPERIMENTAL**

Tentar injetar bwrap DEPOIS do pressure-vessel?
- Tecnicamente muito complexo
- Pode não funcionar
- Necessita pesquisa profunda

## 📋 Recomendações Atuais

### Para Coop Local com Dispositivos Isolados
**USE MODO TRADICIONAL (sem UMU)**
```json
{
  "use_umu": false,
  "proton_version": "GE-Proton10-4"
}
```
✅ Isolamento completo de dispositivos
✅ Funcionalidade testada e comprovada

### Para Jogos Epic/GOG (Single-player ou Online)
**USE MODO UMU**
```json
{
  "use_umu": true,
  "umu_store": "egs",
  "proton_version": "GE-Proton10-4"
}
```
✅ Melhor compatibilidade com lojas
✅ Protonfixes automáticos
⚠️ Sem isolamento de dispositivos

## 🎯 Casos de Uso

| Cenário | Modo Recomendado | Razão |
|---------|------------------|-------|
| Coop local splitscreen | **Tradicional** | Precisa isolamento |
| Jogo Epic single-player | **UMU** | Melhor compatibilidade |
| Jogo GOG single-player | **UMU** | Melhor compatibilidade |
| Steam coop local | **Tradicional** | Precisa isolamento |
| Online multiplayer | **Qualquer** | Sem necessidade de isolar |

## 💡 Workaround Temporário

### Se REALMENTE Precisa UMU + Isolamento

**Opção Manual:**
1. Configure os jogos para usar controles específicos dentro do jogo
2. Desabilite dispositivos manualmente no sistema antes de iniciar
3. Use ferramentas externas de mapeamento de controle

**Limitações:**
- Trabalhoso
- Não automático
- Requer configuração manual por jogo

## 🔮 Futuro

Possíveis melhorias a investigar:
1. Contribuir para o projeto UMU com suporte a device isolation
2. Pesquisar hooks no pressure-vessel
3. Desenvolver wrapper customizado
4. Testar variáveis de ambiente SDL/Wine

## ⚠️ CONCLUSÃO ATUAL

**MODO UMU = SEM ISOLAMENTO DE DISPOSITIVOS**

Isso é uma **limitação conhecida** da arquitetura UMU.

**Escolha baseada em necessidade:**
- Precisa isolar dispositivos? → **Use modo tradicional**
- Precisa compatibilidade Epic/GOG? → **Use UMU, aceite limitação**

---

**Status:** Limitação documentada
**Prioridade:** Investigar soluções futuras
**Recomendação:** Usar modo apropriado para cada caso de uso
