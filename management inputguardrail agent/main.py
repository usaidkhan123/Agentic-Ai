from agents import Agent,Runner,input_guardrail,GuardrailFunctionOutput,InputGuardrailTripwireTriggered
import asyncio,rich
from connection import config
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

class StudentOutput(BaseModel):
    response : str
    relevantQuerry : bool



management_agent = Agent(
    name="management agent",
    instructions="You're management agent you have deal with student querries releated to class timming , etc.",
    output_type=StudentOutput
)

@input_guardrail
async def security_guardrail(ctx,agent,input):
    result = await Runner.run(
        management_agent,
        input,
        run_config = config
    )
    rich.print(result.final_output)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=False
    )


student_agent = Agent(
    name = "student agent",
    instructions="You're a student agent",
    input_guardrails=[security_guardrail]
)

async def main():
    try:
        response = await Runner.run(
             student_agent,
            "i want to change my class timming",
            run_config=config
            )
        print(response)
    except InputGuardrailTripwireTriggered:
        print("irrelevant querry")



if __name__ == "__main__":
    asyncio.run(main())