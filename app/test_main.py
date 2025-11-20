"""test"""
from unittest.mock import patch
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

@patch("app.services.s3_service")
def test_read_main(mock_boto):
    """test"""
    mock_boto.upload_file.return_value = "s3://test/test"

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
