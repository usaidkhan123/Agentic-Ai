from agents import Agent,Runner
from connection import config
from dotenv import load_dotenv
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
load_dotenv()


diet_planner_agent = Agent(
    name = "Diet Planner Agent",
    instructions="""You are a diet planner agent, your task is to create personalized diet plans based on user preferences, dietary restrictions, and health goals.""" 
    )


workout_planner_agent = Agent(
    name="Workout Planner Agent",
    instructions="""You are a workout planner agent, your task is to design effective workout routines tailored to individual fitness levels, goals, and available equipment."""
)``

health_counselor_agent = Agent(
    name="Health Counselor Agent",
    instructions="""You are a health counselor agent, your task is to provide guidance on general health and wellness topics, including stress management, sleep hygiene, and preventive care."""    
    )

fitness_agent = Agent(
    name = " Fitness Coach",
    instructions=""" You are an parent fitness agent coach,your task is analyze prompt and delegate it to approriate.
     Delegate queries related to diet and nutrition to a diet planner agent.
     Delegate queries related to  exercise and workout plans to a workout planner agent. 
     Delegate queries related to  health and wellness to a health counselor agent.
     Also give one motivational quote at the end of each response.""",
    handoffs=[workout_planner_agent,diet_planner_agent,health_counselor_agent]
)

async def main():
    response =await Runner.run(
        fitness_agent,
        "I want to lose weight and build muscle. Can you help me with a diet plan and workout routine? my weight is 80kg and height is 5.9ft and also tell me workout plan i workout in gym for 5 days in a week,give me only workout plan",
        run_config=config
    )
    print(response.final_output)
    print("Agent Name ==>",response.last_agent.name)

    # async for event in response.stream_events():
    #     if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
    #         print(event.data.delta, end="",flush=True)

if __name__ == "__main__":
    asyncio.run(main())