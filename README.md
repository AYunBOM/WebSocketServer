# G9HW1

## 프로젝트명
서버-클라이언트간 Random 계산문제 맞추기 구현<br/>

## 조 이름
G9HW1<br/>

## 조원&역할
### 20213081 강수빈
외부 서버 생성 및 관리, 서버 코드 작성, 클라이언트 코드 작성, 로그 파일 작성, 전체적인 디버깅<br/>
### 20213100 복원빈
외부 서버와의 연결, 서버 코드 작성, 클라이언트 코드 작성, 영상촬영 및 제작, 전체적인 디버깅<br/>
### 20213126 장보미
서버 코드 작성, 클라이언트 코드 작성, 전체적인 디버깅, 영상촬영 및 제작, ReadMe 작성<br/>

## 프로그램 구성요소 설명
### server.py
#### 라이브러리&내장함수
socket    socket()  [소캣 객체를 생성하는 함수]  <br/>
          listen()  [소켓을 통해 들어오는 연결 요청을 수신하기 위한 대기 상태로 설정하는 함수, ()안에 4를 지정하여 클라이언트 소켓 4개를 연결]
random     randint()  [지정된 범위 내의 무작위 정수를 생성하는 함수] <br/>
threading  Thread() [멀티스레딩을 구현하고, 병렬로 실행될 작업 또는 함수를 지정하여 동시성 프로그래밍을 지원하는 스레드를 생성하는 함수] <br/>
#### 식별자
thread_num              int      [클라이언트 번호]
system_clock            int      [서버 누적 시간]
system_clock_formating  string   [system_clock을 문자열로 변환한 값]
question                string   [임의로 출제한 문제]
answer                  int      [임의로 풀제한 문제의 정답]
data                    string   [클라이언트에게 받은 메시지]
client_time             int      [클라이언트가 문제를 푸는데 걸린 임의의 시간]
client_ans              int      [클라이언트가 문제를 푼 답]
delay                   int      [클라이언트가 문제를 맞추었을 시, 새 문제를 출제하기 전 대기시간]
finish_line             string   [600초가 넘었을 때, 클라이언트에게 알리는 메시지]
result_sum              int      [클라이언트가 맞춘 정답의 총 합계]
#### 함수(function)
real_time()                      [system_clock을 `00:00` 형식의 문자열로 변환하는 함수]
random_question()                [임의의 문제를 출제하는 함수]
client_handler()                 [클라이언트에게 문제를 주고 답을 받는 함수)]

### client.py
#### 라이브러리&내장함수

#### 식별자
thread_num              int      [클라이언트 번호]
system_clock            int      [서버 누적 시간]
system_clock_formating  string   [system_clock을 문자열로 변환한 값]
question_q              string   [서버가 임의로 출제한 문제]
question_recv_time      int      [서버의 system_clock]
question_resolve_time   string   [클라이언트가 임의로 문제를 푼 시간]
question_ans_time       int      [question_recv_time과 question_resolve_time을 더한 누적 시간]
#### 함수(function)
real_time()                      [system_clock을 `00:00` 형식의 문자열로 변환하는 함수]
## 소스코드 컴파일방법
### #저희조는 visual stduio code를 사용하였습니다.
