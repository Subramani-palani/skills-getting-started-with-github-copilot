"""Pytest configuration and fixtures for the application tests."""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app


@pytest.fixture
def client():
    """Provide a TestClient instance for testing the FastAPI application."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test."""
    from app import activities
    
    # Store original state
    original_activities = {
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
            "description": "Join the school soccer team and compete in matches",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["alex@mergington.edu", "lucas@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Practice basketball skills and play friendly games",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["mia@mergington.edu", "noah@mergington.edu"]
        },
        "Drama Club": {
            "description": "Act, direct, and participate in school plays",
            "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["ava@mergington.edu", "liam@mergington.edu"]
        },
        "Art Workshop": {
            "description": "Explore painting, drawing, and other visual arts",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["ella@mergington.edu", "jack@mergington.edu"]
        },
        "Math Club": {
            "description": "Solve challenging math problems and prepare for competitions",
            "schedule": "Fridays, 4:00 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["grace@mergington.edu", "henry@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Participate in science events and experiments",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["chloe@mergington.edu", "ben@mergington.edu"]
        }
    }
    
    # Clear and reset
    activities.clear()
    activities.update(original_activities)
    yield
    
    # Reset after test
    activities.clear()
    activities.update(original_activities)