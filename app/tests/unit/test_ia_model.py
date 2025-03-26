import os
import sys
from unittest.mock import MagicMock

from app.application.ai_api_service import AIApiService
import pytest

from app.application.genai_model import GenAIModel
from app.tests.test_data_provider import TestDataProvider
from app.util.exceptions import ExternalServiceException


class TestAIAPIService:
    @pytest.fixture
    def mock_genai_model(self):
        mock_model = MagicMock()
        instance = GenAIModel(api_key="api-key", model="model")
        instance.model = mock_model
        return instance


    @pytest.mark.parametrize(
        "input_text, expected_result",
        [
            ("1234567test123", "test"),  #  test_format_text_success
            ("text", None),              #  test_format_text_less_than_ten_chars_returns_none
            ("1234567890", None),        #  test_format_text_has_ten_chars_returns_none
        ],
    )
    def test_format_text(self, mock_genai_model, input_text, expected_result):
        result = mock_genai_model._format_text(input_text)
        
        assert result == expected_result


    @pytest.mark.parametrize(
        "mock_response_text, expected_result",
        [
            # test_generate_content_success:
            (
                "json123"  + TestDataProvider.json_text_example() + "123", 
                TestDataProvider.json_text_example()
            ),
            # test_generate_content_less_than_ten_chars_returns_none:
            ("text", None), 
            # test_generate_content_has_ten_chars_returns_none:
            ("1234567890", None),
        ],
    )
    def test_generate_content(self, mock_genai_model, mock_response_text, expected_result):
        mock_genai_model.model.generate_content.return_value.text = mock_response_text

        result = mock_genai_model.generate_content("Back to the future")

        assert result == expected_result
        mock_genai_model.model.generate_content.assert_called_once()


    def test_generate_content_exception(self, mock_genai_model):        
        mock_genai_model.model.generate_content.side_effect = Exception("Spmething when wrotn")

        with pytest.raises(
            ExternalServiceException, 
            match="Cannot get the information for the title: back to the future"
        ):
            mock_genai_model.generate_content("back to the future")