#include <iostream>
#include <stdio.h>
#include <WinSock2.h>
#include <WS2tcpip.h>
#include <time.h>
#include <unistd.h>
#include <vector>
#include <random>
#include <string>

int main(){
    int port = 12345;
    BOOL yes = 1;
    WSADATA wsa_data;
    //INIT
    if(WSAStartup(MAKEWORD(2,0),&wsa_data) != 0){
        std::cerr << "Winsock初期化失敗" << std::endl;
    }

    int src_socket;
    struct sockaddr_in src_addr;
    memset(&src_addr,0,sizeof(src_addr));
    src_addr.sin_port = htons(port);
    src_addr.sin_family = AF_INET;
    // src_addr.sin_addr.s_addr = INADDR_ANY;
    src_addr.sin_addr.s_addr = inet_addr("255.255.255.255");
    
    //ipv4,UDP
    src_socket = socket(AF_INET,SOCK_DGRAM,0);
    setsockopt(src_socket,SOL_SOCKET,SO_BROADCAST,(char*)&yes,sizeof(yes));
    //socketをipアドレスとポートに紐づけ
    bind(src_socket,(struct sockaddr*)&src_addr,sizeof(src_addr));


    //buff
    std::string buf = "sPAn:0";
    std::cout << "waiting" << std::endl;
    std::mt19937 mt{std::random_device{}()};
    std::uniform_int_distribution<int> dist(1,3);
    while(1){
        sendto(src_socket,buf.c_str(),sizeof(char)*buf.length(),0,(struct sockaddr*)&src_addr,sizeof(src_addr));
        sleep(1);
        std::cout << (double)clock() << ":" << buf.c_str() << std::endl;
        buf = "pPAn:" + std::to_string(dist(mt));
    }
    closesocket(src_socket);
    WSACleanup();
    return 0;

}