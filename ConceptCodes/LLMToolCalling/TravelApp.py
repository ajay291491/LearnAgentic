# Importing required Python Modules

import os
import json
from  dotenv import load_dotenv
from openai import OpenAI, api_key
import gradio as gr
import requests

# Loading required variables
load_dotenv(override=True)
openai_key = os.getenv("OPENAI_API_KEY")
weather_key = os.getenv("OPEN_WEATHER_API_KEY")

# print(f"OpenAI Key       : {openai_key[:5]}")
# print(f"Open Weather key : {weather_key[:5]}")

# Initializing OpenAI SDK
openai=OpenAI()

# Defining function to call weather data from OpenWeather API
def get_weather_data(latitude, longitude):
    """
    :param latitude: Latitude, decimal (-90; 90). If you need the geocoder to automatic convert city names and zip-codes to geo coordinates and the other way around,
    :param longitude: Longitude, decimal (-180; 180). If you need the geocoder to automatic convert city names and zip-codes to geo coordinates and the other way around,
    :return: weather outlook
    """
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat" :round(float(latitude), 2),
        "lon" :round(float(longitude), 2),
        "appid" : weather_key,
        "units": "metric"
    }
    try:
        response = requests.get(weather_url, params=params)
        data = response.json()
        return data
    except Exception as error:
        print(f"Error : while connecting to OpenWeather API : {error}")

# Defining tool calling schema for LLM with function  get_weather_data

get_weather_data_tool = {
    "name": "get_weather_data",
    "description": "Use this tool to get weather data for a specific latitude and longitude",
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {
                "type": "number",
                "description": "Latitude, decimal (-90; 90)."
            },
            "longitude": {
                "type": "number",
                "description": "Longitude, decimal (-180; 180)."
            }
        },
        "required": ["latitude", "longitude"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": get_weather_data_tool }]

# Defining system prompt to control the behavior of LLM
system_prompt = """You are a travel agent named Aparna trying to guide your customer to visit places in a city and its weather forecast.
                    You will need to ask your customer the city they are planning to travel.
                    Then need to find the find latitude and longitude coordinates for that city and call the get_weather_data tool with those coordinates.
                    When you send response back to user, make sure you are sending the information of weather forecast in a user friendly way, and not the raw data from the tool response.
                    You must also include top 5 attractions they can visit to. 
                    Also best travel agent booking platforms available to book this trip which will save money for them
                    """

# Defining chat function
def chat(message, history):
    print('calling 1')
    messages = [{"role": "system", "content": system_prompt}] + history +  [{"role": "user", "content": message}]
    done = False

    while not done:
        print('calling 2')
        model_name = "gpt-4o-mini"
        response = openai.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=tools
        )
        print('calling 3')
        message_obj = response.choices[0].message
        finish_reason = response.choices[0].finish_reason
        print(f'calling 4 : {finish_reason}')
        if finish_reason=="tool_calls":
            print(f'calling 5 : {message_obj}')
            messages.append(message_obj)
            tool_calls = message_obj.tool_calls
            for tool_call in tool_calls:
                arguments = json.loads(tool_call.function.arguments)
                print('calling 6')
                results = get_weather_data(**arguments)
                print('calling 7')
                # Add tool response
                tool_response = {
                    "role": "tool",
                    "content": json.dumps(results),
                    "tool_call_id": tool_call.id
                }
                messages.append(tool_response)
        else:
            done = True
    return response.choices[0].message.content

# Initializing Chat function
gr.ChatInterface(chat).launch()
