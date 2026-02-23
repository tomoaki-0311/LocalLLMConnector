const path = require("path");
const { LocalLLMClient } = require("../src");

async function main() {
  const defaultImage = path.resolve(__dirname, "..", "..", "samples", "assets", "sample64.jpg");
  const imagePath = process.env.LLM_IMAGE_PATH || defaultImage;

  const client = new LocalLLMClient();
  const text = await client.generateWithImages({
    model: "qwen2.5vl:7b",
    prompt: "Describe this image in one sentence.",
    imagePaths: [imagePath],
  });
  console.log(text);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
