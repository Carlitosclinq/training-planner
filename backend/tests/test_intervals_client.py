import pytest
from unittest.mock import Mock, patch
from app.services.intervals_client import IntervalsClient

def test_intervals_client_init():
    client = IntervalsClient("test_key", "12345")
    assert client.api_key == "test_key"
    assert client.athlete_id == "12345"

@patch('app.services.intervals_client.requests.get')
def test_get_activities(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "activities": [
            {"id": "1", "type": "ride", "distance": 50000}
        ]
    }
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    client = IntervalsClient("test_key", "12345")
    activities = client.get_activities()

    assert len(activities) == 1
    assert activities[0]["id"] == "1"
    assert activities[0]["type"] == "ride"