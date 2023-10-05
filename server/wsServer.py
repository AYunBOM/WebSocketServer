# -*- coding: utf-8 -*-

import socket
import random
import time

# 서버 설정
host = '0.0.0.0'  # 모든 IP 주소에서 연결 허용
port = 8080       # 사용할 포트 번호

system_clock = 0

def random_question():
    first_num = random.randint(0, 100)
    second_num = random.randint(0, 100)
    third_num = random.randint(0, 100)
    operator1 = random.choice(['+', '-', '*', '/'])
    operator2 = random.choice(['+', '-', '*', '/'])

    question = "{} {} {} {} {}".format(first_num, operator1, second_num, operator2, third_num)

    answer = int(eval(question))

    question += " = ?"

    return question, answer


def client_handler():
    global system_clock

    while system_clock < 600:
        question, answer = random_question()

        client_socket.send(question.encode('utf-8'))

        data = client_socket.recv(1024).decode('utf-8')
        print("클라이언트로부터 받은 데이터: {}".format(data))
        
        time.sleep(1)
        system_clock += 1










# 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("0")
# 소켓을 주소와 포트에 바인딩
server_socket.bind((host, port))

# 클라이언트로부터 연결 대기
server_socket.listen(1)  # 1개의 연결을 동시에 처리

print("서버가 {}:{}에서 실행 중입니다.".format(host, port))

# 클라이언트와 연결 수락
client_socket, client_address = server_socket.accept()
print("{}에서 연결이 수락되었습니다.".format(client_address))

while True:
    # 클라이언트로부터 데이터 받기
    

    # 서버에서 메시지 생성
    server_message = "server: " + data

    # 클라이언트로 메시지 보내기
    client_socket.send(server_message.encode('utf-8'))

# 연결 종료 (실제로는 이 부분이 실행되지 않을 것입니다)
client_socket.close()
server_socket.close()
