#define _GNU_SOURCE
#include <dlfcn.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>
#include <stdlib.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/file.h>
#include <libgen.h>
#include <signal.h>

// Ponteiros para funções originais
static char* (*original_getcwd)(char*, size_t) = NULL;

// Variável para armazenar o diretório da biblioteca
static char library_dir[1024] = {0};
static int already_logged = 0;

// Função para obter o caminho do arquivo de log
char* get_log_path() {
    static char log_path[1024] = {0};
    if (log_path[0] == '\0') {
        // Se já descobrimos o diretório da biblioteca, use-o
        if (library_dir[0] != '\0') {
            snprintf(log_path, sizeof(log_path), "%s/game_workdir.log", library_dir);
        } else {
            // Fallback para o diretório atual
            strcpy(log_path, "game_workdir.log");
        }
    }
    return log_path;
}

void __attribute__((constructor)) init() {
    original_getcwd = dlsym(RTLD_NEXT, "getcwd");

    // Obtém o caminho desta biblioteca
    Dl_info info;
    if (dladdr((void*)init, &info)) {
        // Agora info.dli_fname contém o caminho para a biblioteca
        // Vamos extrair o diretório
        char* path_copy = strdup(info.dli_fname);
        if (path_copy) {
            char* dir = dirname(path_copy);
            if (dir) {
                strncpy(library_dir, dir, sizeof(library_dir) - 1);
                library_dir[sizeof(library_dir) - 1] = '\0';
            }
            free(path_copy);
        }
    }
}

// Intercept getcwd - apenas uma chamada é logada e depois encerra o processo
char* getcwd(char* buf, size_t size) {
    if (!original_getcwd) original_getcwd = dlsym(RTLD_NEXT, "getcwd");

    char* result = original_getcwd(buf, size);

    // Log apenas se for bem-sucedido e ainda não tivermos logado
    if (result && !already_logged) {
        char* log_path = get_log_path();
        int fd = open(log_path, O_CREAT | O_WRONLY | O_TRUNC, 0644);
        if (fd >= 0) {
            // Tentar obter lock exclusivo no arquivo
            if (flock(fd, LOCK_EX | LOCK_NB) == 0) {
                dprintf(fd, "GETCWD: %s\n", result);
                flock(fd, LOCK_UN);
            }
            close(fd);
        }

        already_logged = 1;

        // Encerra o processo imediatamente após escrever o log
        kill(getpid(), SIGKILL);
    }

    return result;
}
