#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <thread>
#include <chrono>

#pragma comment(lib, "ws2_32.lib")

int main() {
    WSADATA wsa;
    WSAStartup(MAKEWORD(2, 2), &wsa);

    const char* ip = "127.0.0.1";

    while (true) {
        int port = 5000 + rand() % 5;

        SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);

        sockaddr_in server;
        server.sin_family = AF_INET;
        server.sin_port = htons(port);
        inet_pton(AF_INET, ip, &server.sin_addr);

        if (connect(sock, (sockaddr*)&server, sizeof(server)) == 0) {
            std::string msg = "EVENT:ATTACK";
            send(sock, msg.c_str(), msg.size(), 0);
            std::cout << "🔥 Attack → " << port << std::endl;
        }

        closesocket(sock);

        std::this_thread::sleep_for(std::chrono::milliseconds(800));
    }

    WSACleanup();
}