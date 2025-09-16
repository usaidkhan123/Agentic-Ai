from agents import Agent,Runner,RunContextWrapper,function_tool
from connection import config
from pydantic import BaseModel
from dotenv import load_dotenv
import rich,asyncio
load_dotenv()

class BankAccount(BaseModel):
    account_number : str
    customer_name : str
    account_balance : int
    account_type : str



bank_account = BankAccount(
    account_number="ACC-789456",
    customer_name="Fatima Khan",
    account_balance=75500,
    account_type="savings")




@function_tool
async def get_customer_info(wrapper:RunContextWrapper[BankAccount]):
    return f"This is bank acc info of Fatima khan{wrapper.context}"



personal_agent = Agent(
    name="Personal Agent",
    instructions="You are a helpful assistant, always call the tool to get user's information",
    tools=[get_customer_info]

)

async def main():
    response = await Runner.run(
        personal_agent,
        "what is my customer name and also tell me account balance",
        run_config=config,
        context = bank_account
    )
    rich.print(response.final_output)

if __name__== "__main__":
    asyncio.run(main())

