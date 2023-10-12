# -*- coding: utf-8 -*-

import socket
import random
import threading

# 서버 설정
host = "0.0.0.0"  # 모든 IP 주소에서 연결 허용
port = 8080  # 사용할 포트 번호

server_file = open("server_log.txt", "w")

thread_num = 0  # 클라이언트 번호 초기값 설정
system_clock = 0  # 서버 0~600초 누적시간
system_clock_formating = ""  # 누적시간 형태 변환할 문자열
result_sum = 0  # 정답 합계
count = 0

# 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 소켓을 주소와 포트에 바인딩
server_socket.bind((host, port))

# 클라이언트로부터 연결 대기
server_socket.listen(4)  # 4개의 연결을 동시에 처리
server_file.write("서버가 {}:{}에서 실행 중입니다.\n".format(host, port))


# 시간을 출력 형식에 맞게 변환
def real_time(time):
    minute = "{}".format(time // 60)
    second = "{}".format(time % 60)
    result = "{}:{}".format(minute.zfill(2), second.zfill(2))
    # 예) 3초 => 00:03 / 100초 => 01:40
    return result


# 랜덤으로 문제 출제&정답
def random_question():
    first_num = random.randint(1, 100)
    second_num = random.randint(1, 100)
    third_num = random.randint(1, 100)
    operator1 = random.choice(["+", "-", "*", "/"])
    operator2 = random.choice(["+", "-", "*", "/"])

    question = "{} {} {} {} {}".format(
        first_num, operator1, second_num, operator2, third_num
    )

    answer = int(eval(question))

    question += " = "

    return question, answer


# 클라이언트에게 문제 출제 & 정답 체크
def client_handler(client_socket, thread_num):
    global system_clock, result_sum, count

    client_socket.send(str(thread_num).encode("utf-8"))

    question, answer = random_question()

    system_clock_formating = real_time(system_clock)

    server_file.write(
        "{} [server] '클라이언트 {}' 연결 완료.\n".format(system_clock_formating, thread_num)
    )

    server_file.write(
        "{} [server] '클라이언트 {}' 에게 문제를 출제합니다.\n".format(
            system_clock_formating, thread_num
        )
    )

    while system_clock < 600:
        question += ",{}".format(system_clock)  # [3 + 4 + 5 = ?], [4]

        client_socket.send(question.encode("utf-8"))  # 문제 출제
        data = client_socket.recv(1024).decode("utf-8")  # 답 받기

        client_time, client_ans = map(int, data.split())
        system_clock += client_time

        system_clock_formating = real_time(system_clock)

        # 600초가 지나면 클라이언트에게 알림
        if system_clock >= 600:
            system_clock = 600
            system_clock_formating = real_time(system_clock)
            finish_line = "{},{}".format("time over", system_clock)
            client_socket.send(finish_line.encode("utf-8"))
            break

        print("시스템클락 : " + system_clock_formating)

        # 문제를 맞췄을 시, 임의의 시간동안 대기 후 새 문제 출제
        if client_ans == answer:
            delay = random.randint(1, 5)

            server_file.write(
                "{} [server] '클라이언트 {}' (이)가 답을 맞췄습니다. 정답:{}\n".format(
                    system_clock_formating, thread_num, answer
                )
            )
            server_file.write(
                "{} [server] '클라이언트 {}' 에게 {}초 뒤, 새 문제를 출제합니다.\n".format(
                    system_clock_formating, thread_num, delay
                )
            )

            system_clock += delay  # 시간 업데이트(대기 시간 추가)
            system_clock_formating = real_time(system_clock)  # 전체 시간 업데이트

            server_file.write(
                "{} [server] '클라이언트 {}' 에게 문제를 출제합니다.\n".format(
                    system_clock_formating, thread_num
                )
            )

            result_sum += client_ans  # 클라이언트가 푼 문제의 답 최종 합계

            question, answer = random_question()

        # 문제를 틀렸을 시, 같은 문제 재전송
        elif client_ans != answer:
            question = question.split(",")[0]
            server_file.write(
                "{} [server] '클라이언트 {}' 의 답이 틀렸습니다. 문제를 재전송합니다.\n".format(
                    system_clock_formating, thread_num
                )
            )

            continue

    server_file.write(
        "{} [server] '클라이언트 {}' 의 접속을 종료합니다.\n".format(
            system_clock_formating, thread_num
        )
    )

    count += 1

    # 클라이언트가 다 종료된 이후, 최종합계를 출력하고 서버를 종료한다.
    if count == 4:
        server_file.write(
            "{} [server] 최종 합계 : {}\n".format(system_clock_formating, result_sum)
        )

        server_file.write("서버를 종료합니다.\n")
    server_socket.close()


# 클라이언트와 연결 수락
while thread_num < 4:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(
        target=client_handler, args=(client_socket, thread_num)
    )
    client_thread.start()

    thread_num += 1
