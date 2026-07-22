from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act: attempt to sign up a participant who is already enrolled
    initial_signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert: signup is rejected because the student is already signed up
    assert initial_signup_response.status_code == 400
    assert initial_signup_response.json()["detail"] == "Student already signed up for this activity"

    # Act: remove the participant from the activity
    removal_response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert: removal succeeds
    assert removal_response.status_code == 200
    assert removal_response.json()["message"] == f"Removed {email} from {activity_name}"

    # Act: attempt to remove the same participant again
    second_removal_response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert: the second removal is rejected because the student is no longer in the activity
    assert second_removal_response.status_code == 404
    assert second_removal_response.json()["detail"] == "Student not found in this activity"
