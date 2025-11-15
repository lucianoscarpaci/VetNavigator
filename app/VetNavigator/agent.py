import datetime
import os
from zoneinfo import ZoneInfo

import google.auth
from dotenv import load_dotenv
from google.adk.agents import Agent

load_dotenv()

# Set the credentials environment variable BEFORE calling google.auth.default()
credentials_path = os.getenv("SERVICE_ACCOUNT_KEY_FILE")
if credentials_path:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
else:
    print("Warning: SERVICE_ACCOUNT_KEY_FILE not found in .env file.")

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")


def get_weather(query: str) -> str:
    """Simulates a web search. Use it get information on weather.

    Args:
        query: A string containing the location to get weather information for.

    Returns:
        A string with the simulated weather information for the queried location.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city.

    Args:
        city: The name of the city to get the current time for.

    Returns:
        A string with the current time information.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        tz_identifier = "America/Los_Angeles"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"


def translate_military_experience(mos: str, rank: str, experience_years: int) -> str:
    """Translates a veteran's Military Occupational Specialty (MOS), rank, and experience into civilian job suggestions.

    Args:
        mos: The veteran's MOS code (e.g., '11B', '91B', '25U').
        rank: The veteran's rank (e.g., 'Sergeant', 'Captain').
        experience_years: The number of years of experience in the MOS.

    Returns:
        A string containing a list of suggested civilian job roles and sectors.
    """
    mos_to_civilian = {
        "11B": "Infantryman -> Law Enforcement, Security Management, Project Management",
        "91B": "Wheeled Vehicle Mechanic -> Automotive Technician, Diesel Mechanic, Fleet Manager",
        "25U": "Signal Support Systems Specialist -> IT Support Specialist, Network Administrator, Telecommunications Technician",
        "35F": "Intelligence Analyst -> Data Analyst, Business Intelligence Analyst, Market Research Analyst",
        "68W": "Combat Medic -> Emergency Medical Technical (EMT), Paramedic, Licensed Practical Nurse (LPN), Medical Assistant",
    }

    translation = mos_to_civilian.get(
        mos.upper(),
        f"I do not have specific information for MOS {mos}, but general skills include leadership, discipline, and teamwork.",
    )

    return f"Based on your experience as a {rank} with {experience_years} years as a {mos}, here are some potential civilian career paths: {translation}."


root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    instruction="You are VetNavigator, a helpful AI assistant for veterans. Your primary function is to translate military experience (MOS, rank, years of experience) into civilian job roles. You can also provide weather and time information.",
    tools=[get_weather, get_current_time, translate_military_experience],
)
