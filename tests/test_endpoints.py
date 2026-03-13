"""
Test suite for High School Management System API endpoints.

Each test follows the Arrange-Act-Assert (AAA) pattern for clarity:
- Arrange: Set up test data and initial state
- Act: Execute the code being tested  
- Assert: Verify the results
"""

import pytest
from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_all_activities_returns_success(self):
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class", 
            "Gym Class",
            "Soccer Team",
            "Basketball Club",
            "Drama Club",
            "Art Workshop",
            "Math Club",
            "Science Olympiad"
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities_response = response.json()
        for activity_name in expected_activities:
            assert activity_name in activities_response

    def test_get_activities_returns_activity_details(self):
        # Arrange
        # Expected structure for each activity

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        # Verify each activity has required fields
        for activity_name, activity_data in activities.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_new_student_succeeds(self):
        # Arrange
        activity_name = "Chess Club"
        email = "new_student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json() == {
            "message": f"Signed up {email} for {activity_name}"
        }

    def test_signup_duplicate_student_fails(self):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity_fails(self):
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_adds_student_to_participants_list(self):
        # Arrange
        activity_name = "Math Club"
        email = "test_signup@mergington.edu"
        
        # Verify student is not already in the activity
        response_before = client.get("/activities")
        participants_before = response_before.json()[activity_name]["participants"]
        assert email not in participants_before

        # Act
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert signup_response.status_code == 200
        response_after = client.get("/activities")
        participants_after = response_after.json()[activity_name]["participants"]
        assert email in participants_after


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_registered_student_succeeds(self):
        # Arrange
        activity_name = "Soccer Team"
        email = "alex@mergington.edu"  # Already registered

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json() == {
            "message": f"Unregistered {email} from {activity_name}"
        }

    def test_unregister_not_registered_student_fails(self):
        # Arrange
        activity_name = "Basketball Club"
        email = "not_registered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]

    def test_unregister_nonexistent_activity_fails(self):
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_removes_student_from_participants_list(self):
        # Arrange
        activity_name = "Drama Club"
        email = "ava@mergington.edu"
        
        # Verify student is in the activity before unregistering
        response_before = client.get("/activities")
        participants_before = response_before.json()[activity_name]["participants"]
        assert email in participants_before

        # Act
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert unregister_response.status_code == 200
        response_after = client.get("/activities")
        participants_after = response_after.json()[activity_name]["participants"]
        assert email not in participants_after


class TestRootRedirect:
    """Tests for GET / endpoint"""

    def test_root_redirects_to_static_html(self):
        # Arrange
        # The root endpoint should redirect to /static/index.html

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "/static/index.html"