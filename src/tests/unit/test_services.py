import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.app.services.order_service import OrderService
from src.app.services.llm_service import LLMService

class TestOrderService:
    """Unit tests for OrderService"""

    @pytest.fixture
    def order_service(self, test_db):
        return OrderService(db=test_db)

    def test_create_session(self, order_service):
        """Test creating a drive-thru session"""
        session = order_service.create_drive_thru_session(
            vehicle_info="Blue Sedan",
            lane_number=1
        )

        assert session.id is not None
        assert session.vehicle_info == "Blue Sedan"
        assert session.lane_number == 1
        assert session.status == "active"

    def test_add_item_to_order(self, order_service, sample_order_data):
        """Test adding items to an order"""
        # First create a session
        session = order_service.create_drive_thru_session()

        # Create order
        order = order_service.create_order(
            session_id=session.id,
            items=sample_order_data["items"]
        )

        assert order.id is not None
        assert order.total_amount > 0
        assert len(order.items) == 1

    def test_order_summary(self, order_service, sample_order_data):
        """Test generating order summary"""
        session = order_service.create_drive_thru_session()
        order = order_service.create_order(session_id=session.id, items=sample_order_data["items"])

        summary = order_service.get_order_summary(order.id)

        assert summary["order_number"] == order.order_number
        assert "items" in summary
        assert len(summary["items"]) == 1

class TestLLMService:
    """Unit tests for LLMService"""

    @pytest.fixture
    def llm_service(self):
        return LLMService()

    @pytest.mark.asyncio
    async def test_generate_response(self, llm_service):
        """Test generating LLM response"""
        with patch('transformers.pipeline') as mock_pipeline:
            mock_pipeline.return_value = Mock(return_value=[{'generated_text': 'Test response'}])

            response = await llm_service.generate_response("Test message")

            assert response == "Test response"

    @pytest.mark.asyncio
    async def test_classify_intent(self, llm_service):
        """Test intent classification"""
        with patch('transformers.pipeline') as mock_pipeline:
            mock_pipeline.return_value = Mock(return_value={
                'labels': ['ordering'],
                'scores': [0.9]
            })

            intent, confidence = await llm_service.classify_intent("I want a burger")

            assert intent == "ordering"
            assert confidence == 0.9