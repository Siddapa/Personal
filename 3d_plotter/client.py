from connections import Client


if __name__ == '__main__':
    client = Client('192.168.68.128', 65432)
    client.send()
