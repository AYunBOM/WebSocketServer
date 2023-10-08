# -*- coding: utf-8 -*-

import socket
import sys
import time
import random

# 서버 정보 설정
server_host = "101.101.208.213"  # 서버의 IP 주소로 변경
server_port = 8080  # 서버에서 설정한 포트 번호로 변경
delay_time = random.randint(1, 5)

print("서버 접속 대기 시간: {}".format(delay_time))
time.sleep(delay_time)

# 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결
client_socket.connect((server_host, server_port))
client_socket.send(str(delay_time).encode("utf-8"))
print("서버에게 대기시간을 보냈습니다.")

while True:
    # 서버로부터 응답 받기
    question = client_socket.recv(1024).decode("utf-8")
    print("서버에게 받은 문제: {}".format(question))

    # 문제에 대한 걸린 시간과 답 보내기
    answer = sys.stdin.readline()
    client_socket.send(answer.encode('utf-8'))
    print("서버에게 임의의 정답을 보냈습니다.")

# 연결 종료 (실제로는 이 부분이 실행되지 않을 것입니다)
client_socket.close()

# 보미 : 

# 원빈 : 나 바보