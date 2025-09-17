from agents import Agent,Runner,RunContextWrapper
from dotenv import load_dotenv
from connection import config
import asyncio,rich
from pydantic import BaseModel
load_dotenv()

class TravelerType(BaseModel):
    traveler_profile: str
    trip_type : str


traveler = TravelerType(
    traveler_profile ="Solo",
    trip_type = "Adventure"
)

async def get_traveler_info(ctx:RunContextWrapper[TravelerType] , agent: Agent):
    if ctx.context.traveler_profile == "solo" or ctx.context.trip_type == "Adventure":
        return " Suggest exciting activities, focus on safety tips, recommend social hostels and group tours for meeting people"
    elif ctx.context.traveler_profile == "Family" or ctx.context.trip_type == "Cultural":
        return "Focus on educational attractions, kid-friendly museums, interactive experiences, family accommodations"
    elif ctx.context.traveler_profile == "Executive" or ctx.context.trip_type == "Business ":
        return "Emphasize efficiency, airport proximity, business centers, reliable wifi, premium lounges. medical_student/doctor"



travel_planning_agent = Agent(
    name = "Travel Planning Agent",
    instructions=get_traveler_info
)

async def main():
    response = await Runner.run(
        travel_planning_agent,
        "i am a solo travel and i want to go adventures place in america . You can suggest me any kind of adventures place in america.You can suggest me Nature/Outdoors adventure",
        run_config=config,
        context = traveler
    )
    rich.print(response.final_output)

if __name__ == "__main__":
    asyncio.run(main())