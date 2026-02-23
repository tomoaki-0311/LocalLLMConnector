import os
from localllmconnector import LocalLLMClient


def main() -> None:
    here = os.path.dirname(__file__)
    default_image = os.path.abspath(os.path.join(here, "..", "..", "samples", "assets", "sample64.jpg"))
    image_path = os.environ.get("LLM_IMAGE_PATH", default_image)

    client = LocalLLMClient()
    response = client.generate_with_images(
        model="qwen2.5vl:7b",
        prompt="Describe this image in one sentence.",
        image_paths=[image_path],
    )
    print(response)


if __name__ == "__main__":
    main()
