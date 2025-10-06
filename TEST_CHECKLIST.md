# ✅ Checklist de Testes - Integração UMU

## 🧪 Testes Automatizados

### Sintaxe Python
- [x] src/models/profile.py compila
- [x] src/services/umu.py compila
- [x] src/services/instance.py compila
- [x] src/cli/commands.py compila
- [x] src/gui/app.py compila

## 🖥️ Testes de GUI (Requer Ambiente Gráfico)

### Criar Novo Perfil
- [ ] Abrir GUI com sucesso
- [ ] Criar novo perfil
- [ ] Marcar "Use UMU Launcher"
- [ ] Verificar campos UMU aparecem
- [ ] Preencher campos UMU
- [ ] Salvar perfil
- [ ] Verificar JSON salvo corretamente

### Editar Perfil Existente
- [ ] Carregar perfil sem UMU
- [ ] Verificar campos UMU ocultos
- [ ] Marcar "Use UMU Launcher"
- [ ] Verificar campos aparecem
- [ ] Salvar modificações
- [ ] Recarregar perfil
- [ ] Verificar campos mantidos

### Toggle UMU
- [ ] Marcar/desmarcar checkbox
- [ ] Verificar campos aparecem/desaparecem
- [ ] Verificar Proton field esconde/aparece
- [ ] Verificar status bar atualiza

### Carregar Perfil com UMU
- [ ] Abrir ExampleUMU.json
- [ ] Verificar checkbox marcado
- [ ] Verificar campos UMU carregados
- [ ] Verificar valores corretos

## 🎮 Testes de Execução (Requer umu-run)

### Com UMU Instalado
- [ ] umu-run está instalado
- [ ] Criar perfil com UMU
- [ ] Lançar jogo
- [ ] Verificar comando umu-run usado
- [ ] Verificar variáveis de ambiente
- [ ] Verificar jogo executa

### Sem UMU Instalado
- [ ] Criar perfil com UMU
- [ ] Tentar lançar
- [ ] Verificar erro claro mostrado
- [ ] Verificar mensagem sobre instalar umu-run

## 📝 Testes de Dados

### Serialização
- [ ] Criar perfil com todos campos UMU
- [ ] Salvar
- [ ] Verificar JSON tem USE_UMU=true
- [ ] Verificar JSON tem UMU_ID
- [ ] Verificar JSON tem UMU_STORE
- [ ] Verificar JSON tem UMU_PROTON_PATH

### Deserialização
- [ ] Criar JSON manualmente com UMU
- [ ] Carregar na GUI
- [ ] Verificar todos campos carregam
- [ ] Verificar tipos corretos

### Valores Padrão
- [ ] Criar perfil com campos UMU vazios
- [ ] Salvar
- [ ] Verificar valores null/default
- [ ] Verificar execução usa defaults

## 🔄 Testes de Compatibilidade

### Perfis Antigos
- [ ] Carregar perfil sem campos UMU
- [ ] Verificar carrega sem erro
- [ ] Verificar UMU desmarcado
- [ ] Editar e salvar
- [ ] Verificar ainda funciona

### Modo Proton Tradicional
- [ ] Criar perfil sem UMU
- [ ] Verificar Proton version visível
- [ ] Lançar jogo
- [ ] Verificar usa Proton (não UMU)

## 📚 Testes de Documentação

### Links
- [ ] README.md links funcionam
- [ ] docs/UMU_USAGE.md existe
- [ ] docs/UMU_USAGE.pt.md existe
- [ ] Exemplos estão corretos

### Completude
- [ ] Instalação documentada
- [ ] Configuração documentada
- [ ] Exemplos fornecidos
- [ ] Troubleshooting incluído

## 🔧 Testes de Campos UMU

### UMU Game ID
- [ ] Aceita texto
- [ ] Aceita vazio (usa default)
- [ ] Placeholder mostra
- [ ] Tooltip mostra

### UMU Store
- [ ] ComboBox tem 6 opções
- [ ] Default é "none"
- [ ] Todas opções salvam
- [ ] Tooltip mostra

### UMU Proton Path
- [ ] Aceita "GE-Proton"
- [ ] Aceita path absoluto
- [ ] Aceita vazio (usa default)
- [ ] Placeholder mostra
- [ ] Tooltip mostra

## 🎯 Testes de Casos de Uso

### Epic Games Store
- [ ] Criar perfil para jogo EGS
- [ ] UMU_STORE = egs
- [ ] UMU_ID apropriado
- [ ] Executa corretamente

### GOG
- [ ] Criar perfil para jogo GOG
- [ ] UMU_STORE = gog
- [ ] Executa corretamente

### Steam (via UMU)
- [ ] Criar perfil para jogo Steam
- [ ] UMU_STORE = steam
- [ ] Executa corretamente

### Jogo Genérico
- [ ] Criar perfil sem UMU_ID
- [ ] UMU_STORE = none
- [ ] Executa com defaults

## ⚠️ Testes de Erro

### Validação
- [ ] UMU sem umu-run instalado
- [ ] Mensagem de erro clara
- [ ] Sugestão de instalação

### Campos Inválidos
- [ ] Store inválida (não deveria permitir)
- [ ] Path inválido (deveria avisar)

## 📊 Resumo de Status

Total de Testes: ~70
Testes Automatizados Passados: 5/5 ✅
Testes Manuais Pendentes: ~65

## 🚀 Para Executar Testes Manuais

1. Instalar dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Instalar umu-run (opcional, para testes completos):
   ```bash
   # Arch: pacman -S umu-launcher
   # Nobara: dnf install umu-launcher
   ```

3. Executar GUI:
   ```bash
   python linuxcoop.py
   ```

4. Seguir checklist acima

## ✅ Critérios de Sucesso

- [ ] Todos testes automatizados passam
- [ ] GUI abre sem erro
- [ ] Perfis salvam/carregam com UMU
- [ ] Campos aparecem/desaparecem corretamente
- [ ] Documentação está completa
- [ ] Exemplos funcionam
