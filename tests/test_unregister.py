"""
Tests for DELETE /activities/{activity_name}/unregister endpoint following AAA pattern
"""


def test_unregister_successful(client, reset_activities):
    """Test successful unregister removes participant from activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]
    
    # Verify participant was removed from activity
    activities_data = client.get("/activities").json()
    assert email not in activities_data[activity_name]["participants"]


def test_unregister_not_registered(client, reset_activities):
    """Test unregister fails when participant not registered"""
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_unregister_nonexistent_activity(client, reset_activities):
    """Test unregister fails for non-existent activity"""
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_unregister_then_signup_again(client, reset_activities):
    """Test student can unregister and sign up again for same activity"""
    # Arrange
    activity_name = "Programming Class"
    email = "changeable@mergington.edu"
    
    # Act - Sign up
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert signup_response.status_code == 200
    
    # Act - Unregister
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    assert unregister_response.status_code == 200
    
    # Assert - Participant removed
    activities_data = client.get("/activities").json()
    assert email not in activities_data[activity_name]["participants"]
    
    # Act - Sign up again
    signup_again_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert signup_again_response.status_code == 200
    
    # Assert - Participant re-added
    activities_data = client.get("/activities").json()
    assert email in activities_data[activity_name]["participants"]
