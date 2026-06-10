# PPTX-generator-demo
LLM Generation of Powerpoint slides. with agent skills.md functioning as the template guide.


# How to start

start the server first

cd renderer
npx tsx src/server.ts

then run the pipeline

python main.py "Create a 10-slide capability deck about ERNI's digital transformation services"

Or use the renderer standalone (no LLM, just JSON → PPTX):
cd renderer
npx tsx src/cli.ts render --input test-spec.json --output ../output/deck.pptx

Validate an existing .pptx:
cd renderer
npx tsx src/cli.ts validate ../output/test.pptx