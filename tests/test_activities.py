"""
Tests for GET /activities endpoint following AAA (Arrange-Act-Assert) pattern
"""


def test_get_all_activities(client):
    """Test GET /activities returns all activities with correct structure"""
    # Arrange - client fixture provides TestClient
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    
    # Verify activity structure
    activity = data["Chess Club"]
    assert "participants" in activity
    assert "max_participants" in activity
    assert "schedule" in activity
    assert "description" in activity
    assert isinstance(activity["participants"], list)
    assert isinstance(activity["max_participants"], int)


def test_get_activities_contains_participants(client):
    """Test GET /activities includes existing participants"""
    # Arrange - client fixture provides TestClient
    
    # Act
    response = client.get("/activities")
    
    # Assert
    data = response.json()
    chess_club = data["Chess Club"]
    
    # Verify known participants are in the list
    assert len(chess_club["participants"]) > 0
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]
