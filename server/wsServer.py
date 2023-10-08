# -*- coding: utf-8 -*-

import socket
import random
import time
import threading

# 서버 설정
host = '0.0.0.0'  # 모든 IP 주소에서 연결 허용
port = 8080       # 사용할 포트 번호

server_file = open("server_log.txt", 'w')

thread_num = 0              # 클라이언트 번호 초기값 설정
system_clock = ""           # 서버 0~600초 누적시간
time_ls = [0 ,0 ,0 ,0]      # 클라이언트 각각의 시간적립 리스트(스레드번호가 인덱스 번호이자 클라이언트 번호가 됨)
result_sum = 0

# 시간을 리얼타임으로 변환
def real_time(time): 
    minute = "{}".format(time // 60)
    second = "{}".format(time % 60)
    result = "{}:{}".format(minute.zfill(2), second.zfill(2))
    # 예) 3초 => 00:03 / 100초 => 01:40
    return result
    

# 임의의 문제 출제&정답
def random_question():
    first_num = random.randint(1, 100)
    second_num = random.randint(1, 100)
    third_num = random.randint(1, 100)
    operator1 = random.choice(['+', '-', '*', '/'])
    operator2 = random.choice(['+', '-', '*', '/'])

    question = "{} {} {} {} {}".format(first_num, operator1, second_num, operator2, third_num)

    answer = int(eval(question))
    
    question += " = "

    return question, answer

# 클라이언트에게 문제 출제&정답체크
def client_handler(client_socket, thread_num):
    global system_clock, result_sum

    question, answer = random_question()
    
    system_clock = real_time(time_ls[thread_num])

    while time_ls[thread_num] < 600:
        question += ",{}".format(time_ls[thread_num]) # [3 + 4 + 5 = ?], [4]
        server_file.write("{} > 클라이언트 {}에게 문제를 출제합니다.".format(system_clock, thread_num))

        client_socket.send(question.encode("utf-8"))
        data = client_socket.recv(1024).decode("utf-8")
        
        client_time, client_ans  = map(int, data.split())
        time_ls[thread_num] = client_time
         
        system_clock = real_time(time_ls[thread_num])
        print(system_clock)

        # 문제를 맞췄을 시, 임의의 시간동안 대기 후 새 문제 출제
        if client_ans == answer :
            delay = random.randint(1, 5)

            server_file.write("{} > '클라이언트{}'가 답을 맞췄습니다. 정답:{}".format(system_clock, thread_num, answer))
            server_file.write("{} > {}초 뒤 '클라이언트{}'에게 새 문제를 출제합니다.".format(system_clock, delay, thread_num))

            time.sleep(delay) # 임의로 지정한 대기 시간
            time_ls[thread_num] += delay # 시간 업데이트(대기 시간 추가)
            system_clock = real_time(time_ls[thread_num]) # 전체 시간 업데이트

            result_sum += client_ans # 클라이언트가 푼 문제의 답 최종 합계
            
            question, answer = random_question()
        
        # 문제를 틀렸을 시, 같은 문제 재전송
        elif client_ans != answer :
            question = question.split(',')[0]

            server_file.write("{} > '클라이언트{}'의 답이 틀렸습니다. 문제를 재전송합니다.".format(system_clock, thread_num))

            continue   
         
    server_file.write("{} > '클라이언트{}'의 접속을 종료합니다.".format(system_clock, thread_num))

# 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 소켓을 주소와 포트에 바인딩
server_socket.bind((host, port))

# 클라이언트로부터 연결 대기
server_socket.listen(4) # 4개의 연결을 동시에 처리
server_file.write("서버가 {}:{}에서 실행 중입니다.".format(host, port))

# 클라이언트와 연결 수락
while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(
        target=client_handler, args=(client_socket, thread_num)
    )
    client_thread.start()

    client_socket.send(str(thread_num).encode("utf-8"))

    delay_time = int(client_socket.recv(1024).decode("utf-8"))
    time_ls[thread_num] = delay_time
    system_clock = real_time(time_ls[thread_num])
        
    server_file.write("{} > '클라이언트 {}' 연결 완료.\n".format(system_clock, thread_num))
    
    thread_num += 1

server_file.write("최종 합계 : {}".format(result_sum))

server_file.close()
client_socket.close()
server_socket.close()
