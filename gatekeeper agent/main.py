from agents import Agent,Runner,input_guardrail,GuardrailFunctionOutput,InputGuardrailTripwireTriggered
from connection import config
import asyncio,rich
from dotenv  import load_dotenv
from pydantic import BaseModel

class StudentOutput(BaseModel):
    response : str
    isStudentIsOfOurSchool : bool

gatekeepe_agent = Agent(
    name = "gatekeeper",
    instructions="You're an gatekeeper agent . You're task is to stop the student of other school to not enter in our school.Our school name is The Smart School  ",
    output_type=StudentOutput
    )

@input_guardrail
async def gatekeeper_guardrail(ctx,agent,input):
    result = await Runner.run(
        gatekeepe_agent,
        input,
        run_config = config
    )
    rich.print(result.final_output)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=True
    )


student_agent = Agent(
    name =" student agent",
    instructions="You're an student agent ",
    input_guardrails=[gatekeeper_guardrail]
)

async def main():
    try:
        result = await Runner.run(
            student_agent,
            "I am student of the city school",
            run_config=config
        )
    except InputGuardrailTripwireTriggered:
        print("You're student of other school")


if __name__ == "__main__":
    asyncio.run(main())
