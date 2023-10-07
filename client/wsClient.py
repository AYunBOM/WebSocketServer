# -*- coding: utf-8 -*-

import socket
import sys
import time
import random

# 서버 정보 설정
server_host = "101.101.208.213"  # 서버의 IP 주소로 변경
server_port = 8080  # 서버에서 설정한 포트 번호로 변경
num = random.randint(1, 5)
print("서버 접속에 걸리는 시간: {}".format(num))
#print(num)
time.sleep(num)

# 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결
client_socket.connect((server_host, server_port))

client_socket.send(str(num).encode("utf-8"))
print("서버에게 메시지 보냄.")

while True:
    #message = sys.stdin.readline()

    # 서버로 메시지 보내기
    #client_socket.send(message.encode("utf-8"))
    
    # 서버로부터 응답 받기
    response = client_socket.recv(1024).decode("utf-8")
    print("서버 응답: {}".format(response))

    # 문제에 대한 걸린 시간과 답 보내기
    ans = sys.stdin.readline()
    client_socket.send(ans.encode('utf-8'))
    print("서버에게 메시지 보냄.")

# 연결 종료 (실제로는 이 부분이 실행되지 않을 것입니다)
client_socket.close()
