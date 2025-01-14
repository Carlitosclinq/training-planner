import pytest
from unittest.mock import Mock, patch
from app.services.sync_service import SyncService
from app.models.activity import Activity

@pytest.fixture
def mock_intervals_client():
    client = Mock()
    client.get_activities.return_value = [
        {
            "id": "1",
            "type": "ride",
            "start_date": "2024-01-01T10:00:00Z",
            "distance": 50000,
            "duration": 7200,
            "power": {"normalized": 250, "average": 230}
        }
    ]
    return client

def test_sync_activities(db_session, mock_intervals_client):
    sync_service = SyncService(db_session, mock_intervals_client)
    
    # Premier sync
    new_activities = sync_service.sync_activities()
    assert len(new_activities) == 1
    
    # Vérifie que l'activité est en base
    activity = db_session.query(Activity).first()
    assert activity is not None
    assert activity.external_id == "1"
    
    # Deuxième sync (pas de nouvelles activités)
    new_activities = sync_service.sync_activities()
    assert len(new_activities) == 0

def test_sync_with_conflict(db_session, mock_intervals_client):
    sync_service = SyncService(db_session, mock_intervals_client)
    
    # Crée une activité existante avec le même ID externe
    existing_activity = Activity(
        external_id="1",
        type="ride",
        start_date=datetime(2024, 1, 1, 10, 0),
        distance=45000  # Différente distance
    )
    db_session.add(existing_activity)
    db_session.commit()
    
    # Sync devrait mettre à jour l'activité existante
    updated_activities = sync_service.sync_activities()
    assert len(updated_activities) == 1
    
    # Vérifie que l'activité a été mise à jour
    activity = db_session.query(Activity).first()
    assert activity.distance == 50000  # Nouvelle distance