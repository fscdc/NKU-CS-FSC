import socket
import time


def router_main():
    # 从用户那里获取延时和丢包率
    delay = int(input("Enter delay in ms: ")) / 1000  # 将毫秒转换为秒
    loss_rate = float(input("Enter packet loss rate (%): ")) / 100

    # router和server的IP和port
    router_ip, router_port = "127.0.0.1", 30000
    server_ip, server_port = "127.0.0.1", 40460

    # 创建套接字并bind，用的是UDP协议
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((router_ip, router_port))
    print(f"Router is running on {router_ip}:{router_port}")

    client_addr = None
    packet_count = 0  # 初始化包计数器
    loss_every_n_packets = (
        int(1 / loss_rate) if loss_rate > 0 else float("inf")
    )  # 每隔多少个包丢一个包

    while True:
        data, addr = sock.recvfrom(60000)

        # 来自server的包，直接转发给client
        if addr == (server_ip, server_port):
            if client_addr is not None:
                sock.sendto(data, client_addr)
            continue

        # 来自client的包，需要进行延时和丢包处理后转发给server
        client_addr = addr
        packet_count += 1  # 收到一个包，计数器加1

        # 模拟丢包处理
        if packet_count >= loss_every_n_packets:
            print("Simulating packet loss")
            packet_count = 0  # 重置计数器
            continue  # 丢弃当前包，不转发

        # 模拟延时处理
        if delay > 0:
            print(f"Simulating delay of {delay} seconds")
            time.sleep(delay)

        sock.sendto(data, (server_ip, server_port))


if __name__ == "__main__":
    router_main()
