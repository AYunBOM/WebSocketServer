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
result_sum = 0

def random_question():
    first_num = random.randint(1, 100)
    second_num = random.randint(1, 100)
    third_num = random.randint(1, 100)
    operator1 = random.choice(['+', '-', '*', '/'])
    operator2 = random.choice(['+', '-', '*', '/'])

    question = "{} {} {} {} {}".format(first_num, operator1, second_num, operator2, third_num)

    answer = int(eval(question))

    question += " = 정답을 입력해 주세요.\n"

    return question, answer


def client_handler(client_socket, thread_num):
    global system_clock, result_sum

    print("클라이언트{} 시작".format(thread_num))  # 스레드 번호 출력
    
    question, answer = random_question()
    
    system_clock = time_ls[thread_num]

    while system_clock < 600:
        question += ",{},{}".format(system_clock, thread_num) # [3 + 4 + 5 = ?], [4]
         
        client_socket.send(question.encode('utf-8'))

        data = client_socket.recv(1024).decode('utf-8')
        
        client_time, client_ans  = map(int, data.split())
        time_ls[thread_num] = client_time
         
        system_clock = time_ls[thread_num]
        print(system_clock)

        if client_ans == answer :
            delay = random.randint(1, 5)
            print("맞췄습니다. 다음 대기 시간은 {} 입니다".format(delay))
            time.sleep(delay)
            time_ls[thread_num] += delay
            system_clock = time_ls[thread_num]
            result_sum += client_ans
            question, answer = random_question()

        elif client_ans != answer :
            question = question.split(',')[0]
            print("틀렸습니다. 클라이언트{}에게 문제를 다시 보냅니다.".format(thread_num))
            continue
        
    print("'클라이언트{}'의 접속을 종료합니다.".format(thread_num))

# 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 소켓을 주소와 포트에 바인딩
server_socket.bind((host, port))

# 클라이언트로부터 연결 대기
server_socket.listen(4) # 4개의 연결을 동시에 처리
print("서버가 {}:{}에서 실행 중입니다.".format(host, port))

# 클라이언트와 연결 수락
while system_clock < 600:
    client_socket, client_address = server_socket.accept()
    print("'클라이언트{}'의 연결이 수락되었습니다.".format(client_address))
    client_thread = threading.Thread(
        target=client_handler, args=(client_socket, thread_num)
    )
    client_thread.start()

    delay_time = int(client_socket.recv(1024).decode("utf-8"))
    time_ls[thread_num] = delay_time

    thread_num += 1
    
print("최종 합계 : {}".format(result_sum))
client_socket.close()
server_socket.close()