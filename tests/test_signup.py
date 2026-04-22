"""
Tests for POST /activities/{activity_name}/signup endpoint following AAA pattern
"""


def test_signup_successful(client, reset_activities):
    """Test successful signup adds participant to activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]
    
    # Verify participant was added to activity
    activities_data = client.get("/activities").json()
    assert email in activities_data[activity_name]["participants"]


def test_signup_duplicate_registration(client, reset_activities):
    """Test signup fails when student already registered"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity(client, reset_activities):
    """Test signup fails for non-existent activity"""
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_multiple_activities(client, reset_activities):
    """Test a student can sign up for multiple activities"""
    # Arrange
    email = "multiactivity@mergington.edu"
    activities_to_join = ["Chess Club", "Programming Class", "Drama Club"]
    
    # Act
    for activity_name in activities_to_join:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Assert
    activities_data = client.get("/activities").json()
    for activity_name in activities_to_join:
        assert email in activities_data[activity_name]["participants"]
