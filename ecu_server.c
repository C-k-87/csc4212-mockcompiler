#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include "ecu_proc.tab.h"

double get_ecu_data(char *input);

int main() {
    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    char buffer[1024] = {0};

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(8080);

    printf("Running ECU server on port 8080...\n");
    bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr));
    
    listen(server_fd, 3);
    while (1)
    {

        socklen_t addrlen = sizeof(client_addr);
        client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &addrlen);

        read(client_fd, buffer, sizeof(buffer)-1);
        buffer[sizeof(buffer)-1] = '\0';  // ensure null-terminated

        // Find "end;" and cut the string there
        char *end_pos = strstr(buffer, "end;");
        if (end_pos) {
            end_pos[4] = '\0';  // keep "end;" and terminate string
        }
        printf("Message from client: %s\n", buffer);

        double data = get_ecu_data(buffer);
        char response[256];
        snprintf(response, sizeof(response), "%.5f", data);

        printf("Sending data: %s\n", response);
        send(client_fd, response, strlen(response), 0);

        memset(buffer, 0, sizeof(buffer));  // Clear buffer for next message
    }
    

    close(client_fd);
    close(server_fd);
    return 0;
}