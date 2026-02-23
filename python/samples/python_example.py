from localllmconnector import LocalLLMClient


def main() -> None:
    client = LocalLLMClient()
    response = client.generate(model="llama3.1", prompt="Say hello from Python in one sentence.")
    print(response)


if __name__ == "__main__":
    main()
