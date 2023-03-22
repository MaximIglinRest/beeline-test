from clients import get_client

if __name__ == "__main__":
    client = get_client(client="pg")
    client.check()
