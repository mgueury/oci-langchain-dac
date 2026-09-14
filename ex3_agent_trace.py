"""ReAct weather clothing agent with its tool in a separate module."""

import os
import common
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_oci import ChatOCIGenAI

from tools import get_current_weather

load_dotenv()

# -- main -------------------------------------------------------------------

model = ChatOCIGenAI(
    auth_type=os.getenv("AUTH_TYPE", "API_KEY"),
    model_id=os.environ["GENAI_MODEL"],
    provider="generic",
    service_endpoint=f"https://inference.generativeai.{os.environ['REGION']}.oci.oraclecloud.com",
    compartment_id=os.environ["COMPARTMENT_OCID"],
    model_kwargs={"temperature": 0},
)
agent = create_agent(
    model,
    [get_current_weather],
    system_prompt=(
        "You recommend practical adult clothing. Ask for a city when absent. "
        "For weather-dependent advice, call get_current_weather first. Base weather "
        "facts only on its result, then recommend layers, outerwear, footwear, and "
        "rain or sun accessories when appropriate."
    ),
)

print("Agent with Tracing - Weather Clothing (type 'quit' to exit)")
conversation = []
while True:
    try:
        question = input("You: ").strip()
    except KeyboardInterrupt:
        print("\nGoodbye.")
        break
    if question.lower() in {"quit", "exit"}:
        break
    if question:
        conversation = common.trace_agent(
            agent,
            {"messages": [*conversation, HumanMessage(question)]},
            label="Weather agent",
        )["messages"]
        print(f"Agent: {conversation[-1].content}\n")
