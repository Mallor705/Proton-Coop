#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <libevdev/libevdev.h>
#include <linux/uinput.h>
#include <string.h>
#include <dirent.h>
#include <limits.h>

#define VIRTUAL_DEVICE_NAME "InputPlumber Virtual Device"

int create_virtual_device()
{
    int uinput_fd = open("/dev/uinput", O_WRONLY | O_NONBLOCK);
    if (uinput_fd < 0)
    {
        perror("Erro ao abrir /dev/uinput");
        return -1;
    }

    // Configurar o dispositivo virtual
    ioctl(uinput_fd, UI_SET_EVBIT, EV_KEY);
    for (int i = 0; i < 256; i++)
    {
        ioctl(uinput_fd, UI_SET_KEYBIT, i);
    }

    struct uinput_user_dev uidev;
    memset(&uidev, 0, sizeof(uidev));
    snprintf(uidev.name, UINPUT_MAX_NAME_SIZE, VIRTUAL_DEVICE_NAME);
    uidev.id.bustype = BUS_USB;
    uidev.id.vendor = 0x1234;
    uidev.id.product = 0x5678;
    uidev.id.version = 1;

    if (write(uinput_fd, &uidev, sizeof(uidev)) < 0)
    {
        perror("Erro ao configurar dispositivo virtual");
        close(uinput_fd);
        return -1;
    }

    if (ioctl(uinput_fd, UI_DEV_CREATE) < 0)
    {
        perror("Erro ao criar dispositivo virtual");
        close(uinput_fd);
        return -1;
    }

    printf("Dispositivo virtual criado com sucesso: %s\n", VIRTUAL_DEVICE_NAME);
    return uinput_fd;
}

void handle_physical_device(const char *device_path, int virtual_fd)
{
    int fd = open(device_path, O_RDONLY | O_NONBLOCK);
    if (fd < 0)
    {
        perror("Erro ao abrir dispositivo físico");
        return;
    }

    struct libevdev *dev = NULL;
    if (libevdev_new_from_fd(fd, &dev) < 0)
    {
        perror("Erro ao inicializar libevdev");
        close(fd);
        return;
    }

    printf("Monitorando dispositivo físico: %s\n", libevdev_get_name(dev));

    struct input_event ev;
    while (1)
    {
        int rc = libevdev_next_event(dev, LIBEVDEV_READ_FLAG_NORMAL, &ev);
        if (rc == 0)
        {
            // Repassar evento para o dispositivo virtual
            if (write(virtual_fd, &ev, sizeof(ev)) < 0)
            {
                perror("Erro ao enviar evento para dispositivo virtual");
                break;
            }
        }
        else if (rc != -EAGAIN)
        {
            break;
        }
    }

    libevdev_free(dev);
    close(fd);
}

int main(int argc, char *argv[])
{
    char device_path[PATH_MAX];

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
        printf("Joystick encontrado: %s\n", device_path);
    }
    else
    {
        strncpy(device_path, argv[1], sizeof(device_path));
    }

    int virtual_fd = create_virtual_device();
    if (virtual_fd < 0)
    {
        return 1;
    }

    handle_physical_device(device_path, virtual_fd);

    // Remover dispositivo virtual
    ioctl(virtual_fd, UI_DEV_DESTROY);
    close(virtual_fd);
    return 0;
}