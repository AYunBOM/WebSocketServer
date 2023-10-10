# -*- coding: utf-8 -*-

import socket
import sys
import time
import random
from threading import Timer


# 서버 정보 설정
server_host = "101.101.208.213"  # 서버의 IP 주소로 변경
server_port = 8080  # 서버에서 설정한 포트 번호로 변경

# 시간을 리얼타임으로 변환
def real_time(time): 
    minute = "{}".format(time // 60)
    second = "{}".format(time % 60)
    result = "{}:{}".format(minute.zfill(2), second.zfill(2))
    # 예) 3초 => 00:03 / 100초 => 01:40
    return result

def question_timeout():
    print('Sorry, times up\n')

# 제한시간 10분
finish_time = real_time(600)

# 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결
client_socket.connect((server_host, server_port))
thread_num, system_clock = map(int, client_socket.recv(1024).decode("utf-8").split())

# 로그 파일 생성
client_file = open("client{}_log.txt".format(thread_num), 'w')

system_clock_formating = real_time(system_clock)

# 딜레이가 지난 후에 클라이언트 파일에 로그 작성
client_file.write("{} [client {}] 서버에 접속했습니다.\n".format(system_clock_formating, thread_num))

while True:
    elapsed_time = 0
    answer = 0
    timeout = 0
    # 서버로부터 문제 받기 (사칙연산 문제와 클라이언트 번호 포함)
    question = client_socket.recv(1024).decode("utf-8")

    # , 를 기준으로 분해한다.
    question_split = question.split(",")

    # 서버에게 문제와 시간을 받았을 때, 받은 문제를 적는다.
    question_q = question_split[0]
    
    # 서버에게 문제와 시간을 받았을 때, 받은 시간을 적는다.
    question_recv_time = int(question_split[1])
    
    if question_q == 'end' :
        time.sleep(question_recv_time)
        break
    
    print("{} [client {}] 서버에게 받은 문제: {}\n".format(system_clock_formating, thread_num, question_q))
    
    

    # 문제를 받은 시간을 로그 입력 형식에 맞게 변환시킨다.
    system_clock_formating = real_time(question_recv_time)
    client_file.write("{} [client {}] 서버로부터 문제를 받았습니다.\n".format(system_clock_formating, thread_num))
    
    # 문제를 해결한 임의의 시간을 구한다.
    question_resolve_time = random.randint(1, 5)    
    
    # 임의의 시간동안 입력받기
    try:
        # 임의의 시간동안 입력받기
        t = Timer(question_resolve_time, question_timeout)
        t.start()

        prompt = "You have {} seconds to choose the correct answer...\n".format(question_resolve_time)
        answer = input(prompt)
        t.cancel()

    except Exception as e:
        answer = 0
        # EOFError 예외 처리: 사용자가 입력을 종료할 때 예외 처리
        timeout = 1


    # 문제를 푼 시간(로그에 입력할 용도)은 문제를 받은 시간에서 문제를 해결하는데 걸린 시간을 더해주면 된다.
    question_ans_time = question_recv_time + question_resolve_time
    
    # 문제를 푸는 시간이 600초가 넘으면 서버와의 접속 끊기
    if question_ans_time >= 600:
        time.sleep(60-question_recv_time)
        break
    
    # 로그에 입력하는 형식에 맞게 변환시킨다.
    system_clock_formating = real_time(question_ans_time)
    time.sleep(question_resolve_time)

    # 문제에 대한 걸린 시간과 답 보내기

    # 문제를 해결하는데 걸린 시간과 답(공백제거)
    message = '{} {} {}'.format(question_resolve_time, answer, timeout)
    print(message)
    client_socket.send(message.encode('utf-8'))
    client_file.write("{} [client {}] 서버에게 '정답: {}'(를)을 보냈습니다.(문제 푸는데 걸린 시간 {}초)\n".format(system_clock_formating, thread_num, answer, question_resolve_time))


# 서버 종료될 때 로그를 적는다.
client_file.write("{} [client {}] 서버와의 접속을 종료하였습니다.\n".format(finish_time, thread_num))

# 연결 종료 (실제로는 이 부분이 실행되지 않을 것입니다)
client_socket.close()