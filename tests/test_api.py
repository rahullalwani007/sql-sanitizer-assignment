import pytest
import json
from app import create_app

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config['TESTING'] = True

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client 

# Test Cases 

def test_sanitized_input(test_client):
    """Test with a clean, sanitized input string."""
    response = test_client.post('/v1/sanitized/input/',
                                json={"input": "This is a clean input"})
    assert response.status_code == 200
    assert response.json == {"result": "sanitized"}

def test_unsanitized_input_single_quote(test_client):
    """Test with input containing a single quote."""
    response = test_client.post('/v1/sanitized/input/',
                                json={"input": "This ' is not clean"})
    assert response.status_code == 200
    assert response.json == {"result": "unsanitized"}

def test_unsanitized_input_semicolon(test_client):
    """Test with input containing a semicolon."""
    response = test_client.post('/v1/sanitized/input/',
                                json={"input": "This ; is not clean"})
    assert response.status_code == 200
    assert response.json == {"result": "unsanitized"}

def test_unsanitized_input_double_hyphen(test_client):
    """Test with input containing SQL comment '--'."""
    response = test_client.post('/v1/sanitized/input/',
                                json={"input": "This -- is not clean"})
    assert response.status_code == 200
    assert response.json == {"result": "unsanitized"}

def test_unsanitized_input_sql_keyword(test_client):
    """Test with input containing a SQL keyword (case-insensitive)."""
    response = test_client.post('/v1/sanitized/input/',
                                json={"input": "This contains UNION select"})
    assert response.status_code == 200
    assert response.json == {"result": "unsanitized"}

def test_unsanitized_input_complex(test_client):
    """Test with a more complex potentially malicious input."""
    response = test_client.post('/v1/sanitized/input/',
                                json={"input": "1' OR '1'='1; -- "})
    assert response.status_code == 200
    assert response.json == {"result": "unsanitized"}

def test_missing_input_key(test_client):
    """Test request with missing 'input' key."""
    response = test_client.post('/v1/sanitized/input/',
                                json={"other_key": "some value"})
    assert response.status_code == 400
    assert "error" in response.json
    assert "Missing 'input' key" in response.json["error"]

def test_non_json_request(test_client):
    """Test request with incorrect Content-Type."""
    response = test_client.post('/v1/sanitized/input/',
                                data="this is not json",
                                content_type="text/plain")
    assert response.status_code == 415 # Unsupported Media Type
    assert "error" in response.json
    assert "Request must be JSON" in response.json["error"]

def test_invalid_json_request(test_client):
    """Test request with invalid JSON."""
    response = test_client.post('/v1/sanitized/input/',
                                data='{"input": "test",}', 
                                content_type="application/json")
    assert response.status_code == 400
    assert "error" in response.json
    assert "Invalid JSON received" in response.json["error"]

def test_input_not_string(test_client):
    """Test request where 'input' value is not a string."""
    response = test_client.post('/v1/sanitized/input/',
                                json={"input": 12345})
    assert response.status_code == 400
    assert "error" in response.json
    assert "'input' value must be a string" in response.json["error"]


def test_get_request_not_allowed(test_client):
    """Test that GET requests to the endpoint are not allowed."""
    response = test_client.get('/v1/sanitized/input/')
    assert response.status_code == 405 # Method Not Allowed