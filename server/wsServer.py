# -*- coding: utf-8 -*-

import socket
import random
import time
import threading

# 서버 설정
host = '0.0.0.0'  # 모든 IP 주소에서 연결 허용
port = 8080       # 사용할 포트 번호

thread_num = 0              # 클라이언트 번호 초기값 설정
system_clock = 0            # 서버 0~600초 누적시간
time_ls = [0 ,0 ,0 ,0]      # 클라이언트 각각의 시간적립 리스트(스레드번호가 인덱스 번호이자 클라이언트 번호가 됨)

def random_question():
    first_num = random.randint(1, 100)
    second_num = random.randint(1, 100)
    third_num = random.randint(1, 100)
    operator1 = random.choice(['+', '-', '*', '/'])
    operator2 = random.choice(['+', '-', '*', '/'])

    question = "{} {} {} {} {}".format(first_num, operator1, second_num, operator2, third_num)

    answer = int(eval(question))

    question += " = ?"

    return question, answer


def client_handler(client_socket, thread_num):
    global system_clock

    print(f"Thread {thread_num} 시작")  # 스레드 번호 출력
    
    question, answer = random_question()
    

    while system_clock < 600:
         question += ',{}'.format(time_ls[thread_num]) # [3 + 4 + 5 = ?], [4]
         
         client_socket.send(question.encode('utf-8'))

         data = client_socket.recv(1024).decode('utf-8')
         print(f"Thread {thread_num}: 클라이언트로부터 받은 데이터: {data}")   # ex. data = [(time) 3, (ans) 5]
        
         client_time, client_ans  = map(int, data.split())
         time_ls[thread_num] = client_time
        
         if client_ans == answer :
            delay = random.randint(1, 5)
            time.sleep(delay)
            time_ls[thread_num] += delay
            question, answer = random_question()
         elif client_ans != answer :
             question = question.split(',')[0]
             continue
            

    print(f"Thread {thread_num} 종료")

# 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 소켓을 주소와 포트에 바인딩
server_socket.bind((host, port))

# 클라이언트로부터 연결 대기
server_socket.listen(4) # 4개의 연결을 동시에 처리
print("서버가 {}:{}에서 실행 중입니다.".format(host, port))

# 클라이언트와 연결 수락
while True:
    client_socket, client_address = server_socket.accept()
    print("{}에서 연결이 수락되었습니다.".format(client_address))
    client_thread = threading.Thread(target=client_handler, args=(client_socket, thread_num))
    client_thread.start()

    delay_time = client_socket.recv(1024).decode('utf-8')
    time_ls[thread_num] = delay_time
    
    thread_num += 1

client_socke.close()
server_socket.close()