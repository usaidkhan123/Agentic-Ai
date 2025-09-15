from agents import Agent,Runner,OutputGuardrailTripwireTriggered
from connection import config 
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio,rich

class MessageOutput(BaseModel):
    response : str


eigth_grade_std = Agent(
    name="Eight grade student",
    instructions="""
        1. You are an teacher agent that answer query to a eight standard student. Keep your vocabulary simple and easy. 
""",
    output_type=MessageOutput    
)

async def main():
    query="What are trees? Explain using the most complex scientific terminology possible"
    try:
        response = await Runner.run(
            eigth_grade_std,
            query,
            run_config=config  
          )
        print(response.final_output)
    except  OutputGuardrailTripwireTriggered:
        print('Agent output is not according to the expectations')

if __name__ == "__main__":
    asyncio.run(main())