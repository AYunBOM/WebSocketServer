import socket

# 서버 설정
host = '0.0.0.0'  # 모든 IP 주소에서 연결 허용
port = 8080     # 사용할 포트 번호

# 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 소켓을 주소와 포트에 바인딩
server_socket.bind((host, port))

# 클라이언트로부터 연결 대기
server_socket.listen(1)  # 1개의 연결을 동시에 처리

print(f"서버가 {host}:{port}에서 실행 중입니다.")

# 클라이언트와 연결 수락
client_socket, client_address = server_socket.accept()
print(f"{client_address}에서 연결이 수락되었습니다.")

# 클라이언트로부터 데이터 받기
data = client_socket.recv(1024)  # 최대 1024바이트 데이터를 받음
print(f"클라이언트로부터 받은 데이터: {data.decode('utf-8')}")

# 클라이언트로 "Hello World!" 메시지 보내기
message = "Hello World!"
client_socket.send(message.encode('utf-8'))

# 연결 종료
client_socket.close()
server_socket.close()