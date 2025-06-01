# Guia de Teste - Interface Zenity

## Instalação do Zenity

### Ubuntu/Debian:
```bash
sudo apt install zenity
```

### Fedora/RHEL:
```bash
sudo dnf install zenity
```

### Arch Linux:
```bash
sudo pacman -S zenity
```

## Testando a Interface Zenity

### Teste Manual do Zenity
Para verificar se o zenity está funcionando corretamente:

```bash
zenity --password --title="Teste" --text="Digite uma senha qualquer:"
```

### Comportamento Esperado no Linux-Coop

1. **Com zenity instalado:**
   - Uma janela gráfica aparece solicitando a senha sudo
   - Título: "Linux-Coop"
   - Texto: "Digite sua senha para continuar:"
   - Campo de senha oculto (pontos/asteriscos)

2. **Sem zenity instalado:**
   - Fallback automático para prompt de terminal
   - Mensagem no log: "zenity not found, falling back to terminal prompt"

3. **Se usuário cancelar a janela:**
   - Aplicação encerra com mensagem: "Password dialog cancelled by user"

4. **Se senha estiver incorreta:**
   - Aplicação encerra com mensagem: "Invalid sudo password provided"

5. **Se sudo já estiver válido:**
   - Não solicita senha, continua execução
   - Mensagem no log: "Sudo credentials already valid."

## Cenários de Teste

### Teste 1: Zenity Disponível
```bash
# Certifique-se que zenity está instalado
which zenity

# Execute o Linux-Coop
python ./linuxcoop.py Palworld
```

### Teste 2: Sem Zenity
```bash
# Temporariamente remova zenity do PATH
PATH="/usr/bin:/bin" python ./linuxcoop.py Palworld
```

### Teste 3: Sudo Já Válido
```bash
# Execute sudo primeiro
sudo -v

# Execute imediatamente o Linux-Coop
python ./linuxcoop.py Palworld
```

## Troubleshooting

### Zenity não aparece:
- Verifique se está em ambiente gráfico (X11/Wayland)
- Teste: `echo $DISPLAY`
- Verifique permissões do zenity

### Erro "No protocol specified":
- Execute: `xhost +local:`
- Ou execute como usuário gráfico, não root

### Senha não aceita:
- Verifique se a senha está correta no terminal: `sudo -v`
- Certifique-se que o usuário está no grupo sudo/wheel