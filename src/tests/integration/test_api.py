import pytest
from fastapi.testclient import TestClient

class TestDriveThruAPI:
    """Integration tests for Drive-Thru API"""

    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "drive-thru-ordering" in data["service"]

    def test_chat_endpoint(self, client):
        """Test chat endpoint"""
        response = client.post(
            "/api/v1/chat",
            json={"message": "I want to order a cheeseburger"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["status"] == "success"

    def test_create_session(self, client):
        """Test session creation"""
        response = client.post(
            "/api/v1/sessions",
            json={"vehicle_info": "Test Vehicle", "lane_number": 1}
        )

        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert "session_uuid" in data

    def test_order_flow(self, client):
        """Test complete order flow"""
        # Create session
        session_response = client.post("/api/v1/sessions", json={})
        session_data = session_response.json()

        # Create order
        order_response = client.post(
            f"/api/v1/sessions/{session_data['session_id']}/orders",
            json={
                "items": [
                    {
                        "menu_item_id": 1,
                        "quantity": 1,
                        "unit_price": 5.99,
                        "selected_modifiers": {},
                        "special_instructions": ""
                    }
                ]
            }
        )

        assert order_response.status_code == 200
        order_data = order_response.json()
        assert "order_id" in order_data

    def test_invalid_message(self, client):
        """Test chat endpoint with invalid data"""
        response = client.post("/api/v1/chat", json={})

        assert response.status_code == 422  # Validation error

class TestDatabaseIntegration:
    """Database integration tests"""

    def test_database_connection(self, test_db):
        """Test database connection and basic operations"""
        # Test connection by creating a session
        from src.app.models.database import DriveThruSession

        session = DriveThruSession(vehicle_info="Test Car", lane_number=1)
        test_db.add(session)
        test_db.commit()

        # Verify session was created
        saved_session = test_db.query(DriveThruSession).filter_by(vehicle_info="Test Car").first()
        assert saved_session is not None
        assert saved_session.lane_number == 1