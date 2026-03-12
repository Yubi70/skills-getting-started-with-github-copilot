def test_get_activities_returns_expected_keys(client):
    # Arrange
    expected_activity_count = 9
    expected_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert len(data) == expected_activity_count
    assert "Chess Club" in data
    assert set(data["Chess Club"].keys()) == expected_fields


def test_get_activities_participants_is_list(client):
    # Arrange
    activity_name = "Programming Class"

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(data[activity_name]["participants"], list)
