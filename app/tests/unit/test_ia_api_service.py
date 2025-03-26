from unittest.mock import AsyncMock, MagicMock

from app.application.ai_api_service import AIApiService
import pytest

from app.application.ai_model import AIModel
from app.application.genai_model import GenAIModel
from app.tests import test_data_provider
from app.util.exceptions import ExternalServiceException


class TestAIAPIService:
    @pytest.fixture
    def mock_ai_model(self):
        mock_model = MagicMock()
        return mock_model
    
    @pytest.fixture
    def ai_api_service(self, mock_ai_model):
        return AIApiService(model=mock_ai_model)
        
    def test_crate_json_success(self, ai_api_service):
        text = '''
        [
        {"title": "title test 1", "synopsis": "synopsis 1", "genres": ["genre1", "genre2"]},
        {"title": "title test 2", "synopsis": "synopsis 2", "genres": ["genrea", "genreb"]}
        ]
        '''
        expected_result = [
            {"title": "title test 1", "synopsis": "synopsis 1", "genres": ["genre1", "genre2"]},
            {"title": "title test 2", "synopsis": "synopsis 2", "genres": ["genrea", "genreb"]}
        ]
    
        result = ai_api_service._create_json(text)   
    
        assert result == expected_result    

        
    @pytest.mark.parametrize(
        "input_text",
        [
            "invalid json",
            "",
            '{"title": "title test 1", "synopsis": "synopsis 1'
        ]
     )
    def test_create_json_invalid_json_raises_exception(self, ai_api_service, input_text):
        with pytest.raises(ExternalServiceException, match="There is a problem processing the information"):
            ai_api_service._create_json(input_text)
           
            
    def test_create_json_with_none_text_raise_exception(self, ai_api_service):
        text = None

        with pytest.raises(Exception):
            ai_api_service._create_json(text)

    @pytest.mark.asyncio
    async def test_get_content_success(self, ai_api_service, mock_ai_model):
        title = "title"
        text = test_data_provider.TestDataProvider.json_text_example()
        mock_ai_model.generate_content = AsyncMock(return_value=text)
        
        result = await ai_api_service.get_content_suggestion(title)
        
        assert result == ai_api_service._create_json(text)
        mock_ai_model.generate_content.assert_called_once_with(title)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "mock_return_value", 
        [
            "", 
            None
        ]
    )
    async def test_get_content(
        self,
        ai_api_service, 
        mock_ai_model, 
        mock_return_value
    ):
        title = "title"
        mock_ai_model.generate_content = AsyncMock(return_value=mock_return_value)

        result = await ai_api_service.get_content_suggestion(title)
        
        assert result is None
        mock_ai_model.generate_content.assert_called_once_with(title)        
