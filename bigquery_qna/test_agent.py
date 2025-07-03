import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from bigquery_qna.agent import root_agent
from google.genai import types as genai_types


async def main():
    """Runs the agent with a sample query."""
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="bigquery_qna", user_id="test_user", session_id="test_session"
    )
    runner = Runner(
        agent=root_agent, app_name="bigquery_qna", session_service=session_service
    )
    query = "I'd like to query the `bigquery-public-data.wikipedia` dataset. What are the most popular articles?"
    async for event in runner.run_async(
        user_id="test_user",
        session_id="test_session",
        new_message=genai_types.Content(
            role="user", 
            parts=[genai_types.Part.from_text(text=query)]
        ),
    ):
        if event.is_final_response() and event.content and event.content.parts:
            print(event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
