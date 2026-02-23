const { LocalLLMClient } = require("../src");

async function main() {
  const client = new LocalLLMClient();
  const text = await client.generate({
    model: "llama3.1:8b",
    prompt: "Say hello from Node.js in one sentence.",
  });
  console.log(text);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
