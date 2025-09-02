from agents import Agent,Runner
from connection import config
import asyncio
from dotenv import load_dotenv
load_dotenv()

lyricpoetry_agent = Agent(
    name="lyricpoetry agent",
    instructions="You're an lyric poetry agent and your task is to explain or describe lyric poetry "
)

narrativepoetry_agent = Agent(
    name="narrativepoetry agent",
    instructions="You're an narrative poetry agent and your task is to explain or describe narrative poetry"
)

dramaticpoetry = Agent(
    name="dramaticpoetry agent",
    instructions="You're an dramatic poetry agent and your task is to explain or describe dramatic poetry"
)


traige_agent = Agent(
    name="parent agent",
    instructions="""You're an parent agent and your task is to analyze poetry type
      and and delegate it to approriate agent.
      Delegate lyric poetry to lyricpoetry agent.
      Delegate narrative poetry to narrativepoetry agent.
      Delegate dramatic poetry to dramaticpoetry agent.
      Any query other than poetry keep it to 
        yourself and deny the user query""",
    handoffs=[lyricpoetry_agent,dramaticpoetry,narrativepoetry_agent]
)


async def main():
    response = await Runner.run(
        traige_agent,
        """He walked alone where shadows fell,
        Chasing a voice he once knew well.""",
        run_config=config
    )
    print(response.final_output)
    print("Agent Name ==>",response.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())