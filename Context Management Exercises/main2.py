from agents import Agent,Runner,RunContextWrapper,function_tool
from connection import config
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio,rich
load_dotenv()

class StudentProfile(BaseModel):
    student_id: str
    student_name: str
    current_semester: int
    total_courses: int

student = StudentProfile(
    student_id="STU-456",
    student_name="Hassan Ahmed",
    current_semester=4,
    total_courses=5
)


@function_tool
async def get_student_info(wrapper: RunContextWrapper[StudentProfile]):
    return f"this info of student {wrapper.context}"


personal_agent = Agent(
    name="Personal Agent",
    instructions="You are a helpful assistant, always call the tool to get user's information",
    tools=[get_student_info]
)

async def main():
    response = await Runner.run(
        personal_agent,
        "what is my name and student id",
        run_config=config,
        context = student
    )
    rich.print(response.final_output)

if __name__ == "__main__":
    asyncio.run(main())