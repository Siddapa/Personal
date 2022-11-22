from connections import Client


if __name__ == '__main__':
    client = Client('127.0.0.1', 65432)
    client.send()