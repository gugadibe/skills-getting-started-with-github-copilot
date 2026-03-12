"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Dados simulados de atividades
activities = {
    "Robotics": {
        "description": "Build and program robots for competitions.",
        "schedule": "Wednesdays 16:00-18:00",
        "max_participants": 10,
        "participants": []
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays.",
        "schedule": "Fridays 15:00-17:00",
        "max_participants": 15,
        "participants": []
    },
    "Chess": {
        "description": "Learn and play chess competitively.",
        "schedule": "Mondays 17:00-19:00",
        "max_participants": 12,
        "participants": []
    }
}

# Endpoint para listar atividades
@app.get("/activities")
def get_activities():
    return activities

# Endpoint para inscrever aluno
@app.post("/activities/{activity}/signup")
def signup(activity: str, email: str):
    if activity not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    act = activities[activity]
    if email in act["participants"]:
        raise HTTPException(status_code=400, detail="Already signed up")
    if len(act["participants"]) >= act["max_participants"]:
        raise HTTPException(status_code=400, detail="No spots left")
    act["participants"].append(email)
    return {"message": f"Signed up for {activity}!"}

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Competitive soccer team for inter-school matches",
        "schedule": "Practice: Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Pickup games and skill development for basketball enthusiasts",
        "schedule": "Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 16,
        "participants": []
    },
    "Art Club": {
        "description": "Explore drawing, painting, and mixed media projects",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["ava@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting, stage production, and playwriting workshops",
        "schedule": "Thursdays, 3:30 PM - 5:30 PM",
        "max_participants": 25,
        "participants": []
    },
    "Science Club": {
        "description": "Hands-on experiments and science fair preparation",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["noah@mergington.edu"]
    },
    "Debate Team": {
        "description": "Structured debate lessons and inter-school competitions",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": []
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Normalize and validate email
    normalized_email = email.strip().lower()

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if normalized_email in [p.strip().lower() for p in activity.get("participants", [])]:
        raise HTTPException(status_code=400, detail="Student is already signed up")

    # Add student
    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}


@app.post("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    normalized_email = email.strip().lower()
    activity = activities[activity_name]

    participants = activity.get("participants", [])
    normalized_participants = [p.strip().lower() for p in participants]

    if normalized_email not in normalized_participants:
        raise HTTPException(status_code=400, detail="Student not signed up for this activity")

    # Remove participant
    activity["participants"] = [p for p in participants if p.strip().lower() != normalized_email]

    return {"message": f"Unregistered {normalized_email} from {activity_name}"}