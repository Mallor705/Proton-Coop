#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <libevdev-1.0/libevdev/libevdev.h>
#include <linux/uinput.h>
#include <string.h>
#include <dirent.h>
#include <limits.h>

#ifndef PATH_MAX
#define PATH_MAX 4096 // Define a reasonable default value for PATH_MAX
#endif

// Nome do dispositivo virtual que será criado
#define VIRTUAL_DEVICE_NAME "InputPlumber Virtual Device"

// Função para criar e configurar o dispositivo virtual
int create_virtual_device()
{
    // Abre o dispositivo uinput com flags de escrita e sem bloqueio
    int uinput_fd = open("/dev/uinput", O_WRONLY | O_NONBLOCK);
    if (uinput_fd < 0)
    {
        perror("Erro ao abrir /dev/uinput");
        return -1;
    }

    // Configurar o dispositivo virtual: habilita a recepção de eventos de tecla (EV_KEY)
    ioctl(uinput_fd, UI_SET_EVBIT, EV_KEY);
    // Habilita todas as teclas possíveis
    for (int i = 0; i < 256; i++)
    {
        ioctl(uinput_fd, UI_SET_KEYBIT, i);
    }

    // Cria e inicializa a estrutura com informações do dispositivo
    struct uinput_user_dev uidev;
    memset(&uidev, 0, sizeof(uidev));
    snprintf(uidev.name, UINPUT_MAX_NAME_SIZE, VIRTUAL_DEVICE_NAME);
    uidev.id.bustype = BUS_USB;
    uidev.id.vendor = 0x1234;  // ID do fornecedor
    uidev.id.product = 0x5678; // ID do produto
    uidev.id.version = 1;      // Versão do dispositivo

    // Escreve a configuração no dispositivo virtual
    if (write(uinput_fd, &uidev, sizeof(uidev)) < 0)
    {
        perror("Erro ao configurar dispositivo virtual");
        close(uinput_fd);
        return -1;
    }

    // Cria efetivamente o dispositivo virtual
    if (ioctl(uinput_fd, UI_DEV_CREATE) < 0)
    {
        perror("Erro ao criar dispositivo virtual");
        close(uinput_fd);
        return -1;
    }

    // Informar sucesso na criação do dispositivo virtual
    printf("Dispositivo virtual criado com sucesso: %s\n", VIRTUAL_DEVICE_NAME);
    return uinput_fd;
}

// Função que lida com o dispositivo físico: abertura, leitura de eventos e repasse para o dispositivo virtual
void handle_physical_device(const char *device_path, int virtual_fd)
{
    // Abre o dispositivo físico para leitura não bloqueante
    int fd = open(device_path, O_RDONLY | O_NONBLOCK);
    if (fd < 0)
    {
        perror("Erro ao abrir dispositivo físico");
        return;
    }

    // Inicializa a estrutura libevdev para manipular os eventos do dispositivo físico
    struct libevdev *dev = NULL;
    if (libevdev_new_from_fd(fd, &dev) < 0)
    {
        perror("Erro ao inicializar libevdev");
        close(fd);
        return;
    }

    // Exibe o nome do dispositivo físico monitorado
    printf("Monitorando dispositivo físico: %s\n", libevdev_get_name(dev));

    // Loop para leitura dos eventos do dispositivo físico
    struct input_event ev;
    while (1)
    {
        int rc = libevdev_next_event(dev, LIBEVDEV_READ_FLAG_NORMAL, &ev);
        if (rc == LIBEVDEV_READ_STATUS_SUCCESS)
        {
            // Envia o evento capturado para o dispositivo virtual
            if (write(virtual_fd, &ev, sizeof(ev)) < 0)
            {
                perror("Erro ao enviar evento para dispositivo virtual");
                break;
            }
            // Adiciona evento de sincronização
            ev.type = EV_SYN;
            ev.code = SYN_REPORT;
            ev.value = 0;
            if (write(virtual_fd, &ev, sizeof(ev)) < 0)
            {
                perror("Erro ao enviar evento de sincronia para dispositivo virtual");
                break;
            }
        }
        else if (rc != -EAGAIN)
        {
            // Sai do laço se ocorrer um erro diferente de -EAGAIN
            break;
        }
    }

    // Libera recursos alocados pelo libevdev e fecha o dispositivo físico
    libevdev_free(dev);
    close(fd);
}

// Função principal que seleciona o dispositivo físico (joystick) e inicializa os dispositivos
int main(int argc, char *argv[])
{
    char device_path[PATH_MAX];

    // Se nenhum argumento for fornecido, busca automaticamente o joystick na pasta /dev/input/by-id
    if (argc < 2)
    {
        DIR *dir = opendir("/dev/input/by-id");
        if (!dir)
        {
            perror("Erro ao abrir /dev/input/by-id");
            return 1;
        }
        struct dirent *entry;
        int found = 0;
        // Percorre os arquivos do diretório procurando por "joystick" no nome
        while ((entry = readdir(dir)) != NULL)
        {
            if (strstr(entry->d_name, "joystick") != NULL)
            {
                snprintf(device_path, sizeof(device_path), "/dev/input/by-id/%s", entry->d_name);
                found = 1;
                break;
            }
        }
        closedir(dir);
        if (!found)
        {
            fprintf(stderr, "Nenhum joystick encontrado em /dev/input/by-id\n");
            return 1;
        }
        // Exibe o caminho do joystick encontrado
        printf("Joystick encontrado: %s\n", device_path);
    }
    else
    {
        // Utiliza o caminho informado com terminação nula garantida
        strncpy(device_path, argv[1], sizeof(device_path) - 1);
        device_path[sizeof(device_path) - 1] = '\0';
    }

    // Cria o dispositivo virtual e verifica se ocorreu algum erro
    int virtual_fd = create_virtual_device();
    if (virtual_fd < 0)
    {
        return 1;
    }

    // Inicia o tratamento do dispositivo físico monitorado
    handle_physical_device(device_path, virtual_fd);

    // Destrói o dispositivo virtual e limpa recursos
    ioctl(virtual_fd, UI_DEV_DESTROY);
    close(virtual_fd);
    return 0;
}