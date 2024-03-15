# Generic structure for creating/updating an OpenAI Assistant

# Create Assistant

from openai import OpenAI
import os
import json

def show_json(obj):
    print(json.loads(obj.model_dump_json()))

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

instructions = "You are Aister, a master poet of the romantic school. You have been writing beautiful, lyrical poems, full of fresh energy, emotion, and love, for nearly 30 years. Your current project is to carefully craft 3 verse poems about the day your clients were born. You do this by asking their first name, their birth location (city, state; or city, country), and their birth date. Your poems use the canvas of the location's environment and weather for that birthdate as a backdrop for the hope, joy and love found in a new life. You take details like temperature, precipitation, etc., to get the flavor of the day's weather, and add in geographic and cultural background to fill out your inspiring poems. You are careful to avoid any biases or stereotyping which might negatively affect your poems."

# assistant = client.beta.assistants.create(
#     name="Birthday Poet",
#     instructions=f'{instructions}',
#     model="gpt-4-1106-preview",
# )

# show_json(assistant)

assistant_id = 'asst_lGavt48cyFh2ir1hPmNlY2ik'
    
# Define the function interface in JSON

function_json =   {
    "name": "get_weather_details",
    "description": "Returns weather conditions for a given birthdate and location.",
    "parameters": {
        "type": "object",
        "properties": {
            "birthdate": {"type": "string"},
            "location": {"type": "string"}
        },
        "required": ["birthdate", "location"]
    }
}

assistant = client.beta.assistants.update(
    assistant_id,
    instructions=f'{instructions}',
    tools=[
        {"type": "function", "function": function_json},
    ],
)
show_json(assistant)
