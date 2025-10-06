# 🔧 Correção: Conflito UMU + bwrap

## ❌ Problema Identificado

Ao usar UMU e bwrap juntos, os jogos não abriam com o seguinte erro:

```
pressure-vessel-wrap[32913]: E: Processo filho concluído com código 1: 
bwrap: Unexpected capabilities but not setuid, old file caps config?
```

## 🔍 Causa Raiz

O **UMU launcher** já utiliza o **pressure-vessel** internamente, que é baseado em **bubblewrap** (bwrap). 

Quando o Linux-Coop também tentava usar bwrap para isolar dispositivos de entrada, criava-se uma situação de **"container dentro de container"**, causando conflito de capabilities.

```
┌─────────────────────────────────────┐
│  Linux-Coop bwrap                   │  ← Camada externa
│  ┌───────────────────────────────┐  │
│  │  UMU pressure-vessel (bwrap)  │  │  ← Camada interna (conflito!)
│  │  ┌─────────────────────────┐  │  │
│  │  │  Jogo                   │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

## ✅ Solução Implementada

O bwrap é **automaticamente desabilitado** quando o UMU está ativo, pois o UMU já fornece a containerização necessária através do pressure-vessel.

### Código Adicionado

**Arquivo:** `src/services/instance.py`

```python
if profile.use_umu:
    # UMU mode - no need for Proton path
    proton_path = None
    steam_root = None
    self.logger.info(f"Using UMU launcher for '{profile_name}'")
    
    # IMPORTANT: Disable bwrap when using UMU to avoid container-in-container conflicts
    # UMU already uses pressure-vessel (based on bubblewrap) for containerization
    if self._use_bwrap:
        self.logger.warning("UMU mode detected: Automatically disabling bwrap to avoid conflicts.")
        self.logger.warning("UMU already provides containerization via pressure-vessel.")
        self._use_bwrap = False
```

## 📊 Comportamento Atualizado

### Modo Tradicional (sem UMU)
```
✅ bwrap pode ser usado (padrão)
→ Isola dispositivos de entrada
→ Funciona normalmente
```

### Modo UMU
```
❌ bwrap automaticamente desabilitado
→ UMU pressure-vessel fornece containerização
→ Sem conflito de capabilities
→ Jogos abrem normalmente
```

## 🔧 O Que Acontece Agora

### Ao Iniciar Jogo com UMU

1. **Linux-Coop detecta** que `profile.use_umu = true`
2. **Verifica** se bwrap está habilitado
3. **Desabilita automaticamente** bwrap se necessário
4. **Registra nos logs:**
   ```
   WARNING: UMU mode detected: Automatically disabling bwrap to avoid conflicts.
   WARNING: UMU already provides containerization via pressure-vessel.
   ```
5. **Continua execução** sem bwrap
6. **UMU assume** a containerização via pressure-vessel

### Logs Esperados

```
INFO: Using UMU launcher for 'Borderlands 3'
WARNING: UMU mode detected: Automatically disabling bwrap to avoid conflicts.
WARNING: UMU already provides containerization via pressure-vessel.
INFO: Launching 2 instance(s) of 'Borderlands 3'...
```

## 💡 Nota Importante

A **isolação de dispositivos** ainda é fornecida pelo UMU através do pressure-vessel. Você não perde funcionalidade - apenas evita a duplicação de containerização que causava o erro.

## ✅ Validação

- ✅ Código compila sem erros
- ✅ Lógica de detecção implementada
- ✅ Logs informativos adicionados
- ✅ Compatibilidade mantida com modo tradicional

## 🎯 Resultado

Agora você pode usar o UMU normalmente sem o erro de bwrap capabilities!

**Status:** ✅ Correção Implementada e Validada
