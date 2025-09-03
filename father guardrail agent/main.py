from agents import Agent,Runner,input_guardrail,GuardrailFunctionOutput,InputGuardrailTripwireTriggered
import asyncio,rich
from connection import config 
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

class ChilderOutput(BaseModel):
    response : str
    isAcRunningAbove : bool


father_agent=Agent(
    name="father agent",
    instructions="You're a father agent and you have restrict childern run ac above 26C",
    output_type=ChilderOutput
)

@input_guardrail
async def father_guardrail(ctx,agent,input):
    result = await Runner.run(
        father_agent,
        input,
        run_config=config
    )
    rich.print(result.final_output)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=False
    )


childern_agent = Agent(
    name="childern agent",
    instructions="You're a child agent",
    input_guardrails=[father_guardrail]
)

async def main():
    try:
        result = await Runner.run(
             childern_agent,
            "you are running ac above 26C",
            run_config=config
        )
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("You're runnning ac above  26C")

if __name__ == "__main__":
    asyncio.run(main())