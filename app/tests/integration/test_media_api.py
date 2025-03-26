import json
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
import pytest
from pytest_mock import MockerFixture
from starlette import status

from app.application.ai_model import AIModel
from app.application.genai_model import GenAIModel
from app.main import app
from app.application.ai_api_service import AIApiService
from app.tests.test_data_provider import TestDataProvider
from app.util.exceptions import NotFoundException


class TestAIModel(AIModel):
    def generate_content(self, title: str):
        return TestDataProvider.json_text_example()

class TestMadiaAPI:    
    @pytest.fixture
    def client(self):
        return TestClient(app)

        
    def test_content_suggestion_success(self, client, mocker: MockerFixture):
        text = TestDataProvider.json_text_example()
        expected_result = json.loads(TestDataProvider.json_text_example())
        mocker.patch(
            f"{GenAIModel.__module__}.{GenAIModel._create_model.__qualname__}",
            return_value=None,
        )
        mocker.patch(
            f"{AIApiService.__module__}.{AIApiService.get_content_suggestion.__qualname__}",
            return_value=json.loads(text),
        )
        
        response = client.get("/media/content-suggestions?title=Back to the future")
        
        data = response.json()     
        assert response.status_code == status.HTTP_200_OK
        assert data == expected_result


    @pytest.mark.parametrize(
        "return_value", 
        [
            "", 
            None
        ]
    )
    def test_content_suggestion_not_found(self, client, mocker: MockerFixture, return_value):
        title = "Back to the future"
        mocker.patch(
            f"{GenAIModel.__module__}.{GenAIModel._create_model.__qualname__}",
            return_value=None,
        )
        mocker.patch(
            f"{AIApiService.__module__}.{AIApiService.get_content_suggestion.__qualname__}",
            return_value=return_value,
        )
        
        response = client.get(f"/media/content-suggestions?title={title}")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json().get("detail") == f"This title cannot be found: {title}"
        
