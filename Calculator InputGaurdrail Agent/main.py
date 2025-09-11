from agents import Agent,Runner,input_guardrail,GuardrailFunctionOutput,InputGuardrailTripwireTriggered
from connection import config
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio,rich
load_dotenv()


class CalculatorOutput(BaseModel):
    result:str
    isPromptRejected:bool


calculator_guardrail_agent = Agent(
    name="Calculator Guardrail Agent",
    instructions="""You are a strict math input guardrail agent. 
Your only job is to check whether the user input is a valid math problem 
(e.g., addition, subtraction, multiplication, division, fractions, or simple word problems). 
- If the input is a valid math problem, approve it. 
- If the input is not math-related, politely reject it and explain that only math problems are allowed. """,
    output_type=CalculatorOutput
)


@input_guardrail
async def calculator_guardrail(ctx,agent,input):
    response = await Runner.run(
        calculator_guardrail_agent,
        input,
        run_config = config
    )
    rich.print(response.final_output)
    return GuardrailFunctionOutput(
        output_info=response.final_output.result,
        tripwire_triggered=response.final_output.isPromptRejected
    )



calculator_agent = Agent(
    name="Calculator Agent",
    instructions="You are a calculator agent and your task is to solve mathematical problems",
    input_guardrails=[calculator_guardrail]
)

async def main():
    try:
        response = await Runner.run(
                    calculator_agent,
                    "Write an eassay on global warming",
                    run_config = config
                    )
        print(response)
    except InputGuardrailTripwireTriggered:
        print("Input was rejected by the guardrail.")

if __name__ == "__main__":
    asyncio.run(main())