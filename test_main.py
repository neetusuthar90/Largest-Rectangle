import pytest
from fastapi.testclient import TestClient
from main import app, largest_rectangle

test_matrices = [
    {
        "matrix": [
        [1, 1, 1, 0, 1, -9],
        [1, 1, 1, 1, 2, -9],
        [1, 1, 1, 1, 2, -9],
        [1, 0, 0, 0, 5, -9],
        [5, 0, 0, 0, 5, -9],
        ],
        "result": (1, 9),
    },
    {
        "matrix": [
            [1],
        ],
        "result": (1, 1),
    },
    {
        "matrix": [
            [0,1,1,0],
            [1,1,1,1],
            [1,1,1,1],
            [0,1,1,0]
        ],
        "result": (1, 8),
    }
]


def test_largest_rectangle():
    for item in test_matrices:
        result = largest_rectangle(item['matrix'])
        assert result == item['result']    



def test_fastapi_endpoint():
    client = TestClient(app)
    
    for item in test_matrices:
        response = client.post("/input", json=item['matrix'])
        assert response.status_code == 200
        assert response.json() == list(item['result'])
        
 
