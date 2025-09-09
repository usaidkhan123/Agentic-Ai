from agents import Agent,Runner
from connection import config
from dotenv import load_dotenv
import asyncio,rich

load_dotenv()

translator_agent = Agent(
    name="Translator",
    instructions="You are a translator that translates text into different languages "
)

async def main():
    response = await Runner.run(
        translator_agent,
        "convert this sentence:hello how are you into urdu ",
        run_config=config
    )
    print(response.final_output)

if __name__ == "__main__":
    asyncio.run(main())