import socket

# 서버 정보 설정
server_host = '101.101.166.241'  # 서버의 IP 주소로 변경
server_port = 8080           # 서버에서 설정한 포트 번호로 변경

# 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결
client_socket.connect((server_host, server_port))

# 서버로 "Hello World!" 메시지 보내기
message = "Hello World!"
client_socket.send(message.encode('utf-8'))

# 서버로부터 데이터 받기
data = client_socket.recv(1024)  # 최대 1024바이트 데이터를 받음
print(f"서버로부터 받은 데이터: {data.decode('utf-8')}")

# 연결 종료
client_socket.close()