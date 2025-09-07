from agents import Agent,Runner,RunContextWrapper
from connection import config
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio,rich

load_dotenv()

class Person(BaseModel):
    seat_preference : str
    travel_experience : str

personOne = Person(
       seat_preference="window",
       travel_experience="first_time"
)


async def airline_dynamic_instruction(ctx:RunContextWrapper[Person],agent:Agent):
       if ctx.context.seat_preference == "window" and ctx.context.travel_experience == "first_time":
              return "Explain window benefits, mention scenic views, reassure about flight experience"
       elif ctx.context.seat_preference == "aisle" and ctx.context.travel_experience == "occasional":
              return "Acknowledge the compromise, suggest strategies, offer alternatives"
       elif ctx.context.seat_preference ==  "any" and ctx.context.travel_experience  == "premium" :
              return "Highlight luxury options, upgrades, priority boarding"



airline_seat_agent = Agent(
    name="airline seat agent",
    instructions=airline_dynamic_instruction
)


async def main():
        response = await Runner.run(
            airline_seat_agent,
            "",
            run_config=config,
            context=personOne
        )
        print(response)
if __name__ == "__main__":
        asyncio.run(main())
