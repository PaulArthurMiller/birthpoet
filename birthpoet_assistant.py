# The Assistant API call, with response actions

from openai import OpenAI
import os
import json
import time
from log_config import logging
from birthweather_script import get_birthweather

available_tools = []
tool1='get_weather_details'
tool2=None
tool3=None
assistant_id = 'asst_lGavt48cyFh2ir1hPmNlY2ik'
user_input = input("Let's make a great birthday message! Would you please tell me the first name of the person we're celebrating, their birthdate and their birth location? ")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
if "OPENAI_API_KEY" is not None:
    logging.info("Assistant: OpenAI API Key found!")
else:
    logging.error("Assistant: OpenAI API Key not found. Please set it as an environment variable.")

# def show_json(obj):
#     print(json.loads(obj.model_dump_json()))

def process_required_action(run, thread):
    tool_calls_info = []
    run_id = run.id
    tool_calls = run.required_action.submit_tool_outputs.tool_calls

    for tool_call in tool_calls:
        logging.info(dir(tool_call))
        tool_id = tool_call.id
        function_name = tool_call.function.name
        arguments = tool_call.function.arguments
        arguments_dict = json.loads(arguments)
        
        tool_calls_info.append({
            "tool_id": tool_id,
            "function_name": function_name,
            "arguments": arguments_dict
        })
    logging.info(tool_calls_info)

    for tool_call in tool_calls_info:
        logging.info(f"Processing tool call {tool_call['tool_id']} for function {tool_call['function_name']} with arguments {tool_call['arguments']}")
        if tool_call['function_name'] == tool1:
            std_birthdate = arguments_dict.get('birthdate')
            std_birthloc = arguments_dict.get('location')
            weather_details = get_birthweather(std_birthdate, std_birthloc)
            run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=[
                {
                    "tool_call_id": tool_id,
                    "output": f'{weather_details}',
                },
                ]
            )                
        elif tool_call['function_name'] == tool2:
            pass
        elif tool_call['function_name'] == tool3:
            pass
    return run

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(assistant_id, thread, user_input)
    return thread, run

def wait_on_run(run, thread):
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"Current run status: {run.status}")
        logging.info(f'Current run status: {run.status}')
        if run.status == "requires_action":
            process_required_action(run, thread)
            continue
        elif run.status in ["expired", "failed", "cancelled"]:
            print(f"Run encountered an error status: {run.status}")
            logging.error(f"Run encountered an error status: {run.status}")
            # Handle error status here (e.g., log the error, notify the user)
            break  # Exit the loop as the run cannot proceed to completion
        elif run.status == 'completed':
            print("Run completed successfully.")
            logging.info("Run completed successfully.")
            break
        time.sleep(0.5)
    return run

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()

thread, run = create_thread_and_run(user_input)
completed_run = wait_on_run(run, thread)
if completed_run:
    messages = get_response(thread)
    pretty_print(messages)
else:
    print("Error: Messages not available.")
    logging.info("Error: Messages not available.")

# Structure the response in an email. Send to entered email address.
