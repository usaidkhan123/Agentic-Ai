from agents import Agent,Runner,RunContextWrapper
from connection import config
from dotenv import load_dotenv
import asyncio,rich
from pydantic import BaseModel

load_dotenv()

class Person(BaseModel):
    name : str
    profession : str

personOne = Person(
    name =   "usaid",
    profession= "Doctor"
)

async def dynamic_medical_instructions(ctx : RunContextWrapper[Person] , agent : Agent):
    if ctx.context.profession == "Patient":
        return "Use simple, non-technical language. Explain medical terms in everyday words. Be empathetic and reassuring"
    elif ctx.context.profession == "Medical Student":
        return "Use moderate medical terminology with explanations. Include learning opportunities"
    elif ctx.context.profession == "Doctor":
        return "Use full medical terminology, abbreviations, and clinical language. Be concise and professional"



medical_consulation_agent = Agent(
    name="medical consulation agent",
    instructions=dynamic_medical_instructions
)

async def main():
    response = await Runner.run(
        medical_consulation_agent,
        "what are causes of fever",
        run_config=config,
        context=personOne
    )
    rich.print(response.final_output)

if __name__ == "__main__":
    asyncio.run(main())