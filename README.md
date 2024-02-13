# Largest Rectangle in a Matrix

This FastAPI application calculates the largest rectangle formed by similar numbers in the matrix and stores the result in a SQLite database.
A rectangle is defined by selecting a group of adjacent cells that contain the same number. The rectangle should have the maximum area among all rectangles formed by similar numbers.


## Assumptions
- The application handles missing values in the given test case appropriately.
- The largest possible area is considered to be 9, as a square is also a type of rectangle. If the requirement is for the maximum area to be 8, the function needs to ensure that the height and width are never the same. In such a case, a matrix of size 1x1 would be considered an invalid input for the function.
- **My code assumes that square is also a rectangle, hence the answer of sample test case is (1,9), not (1,8)**.

## Dependencies
- Python 3.6 or higher
- FastAPI
- uvicorn
- Pydantic
- SQLite3

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/neetusuthar90/Largest-Rectangle.git
   ```

2. Install the dependencies using pip:

   ```bash
   cd Largest-Rectangle
   pip install -r requirements.txt
   ```

## Usage

1. Start the FastAPI server:

    ```bash
    uvicorn main:app 
    ```

2. Send POST requests to the `/input` endpoint with a JSON body containing the matrix. The matrix should be a list of lists representing rows and columns.

3. The server will respond with a JSON array containing the dimensions of the largest rectangle found, including the maximum area and common integer in that rectangle.

Here's an example of making a POST request using `curl`.
```
➜  ~ curl -X POST \
  http://localhost:8000/input \
  -H 'Content-Type: application/json' \
  -d '[
    [1, 1, 1, 0, 1, -9],
    [1, 1, 1, 1, 2, -9],
    [1, 1, 1, 1, 2, -9],
    [1, 0, 0, 0, 5, -9],
    [5, 0, 0, 0, 5, -9]
  ]'
```
It prints the output as:
```
[1,9]
```

## Testing
This project includes tests using `pytest`. Run the tests with the following command:

```bash
pytest
```
The tests includes:

1. Unit tests for the largest_rectangle function. It takes metrics as an input and checks if output matches the expected output.
2. Integration tests for the FastAPI endpoint. It makes a POST request to the application and compares if output matches the expected output.

You can add more test cases in `test_matrices` list.


## Database

The results are stored in a SQLite database named `database.sqlite`. The database has a table named `results`, where each row represents a calculation result. The table schema is as follows:

```sql
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    matrix TEXT NOT NULL,
    max_area_num TEXT NOT NULL,
    execution_time REAL NOT NULL
)
```

- `matrix`: Stores the input matrix as a string.
- `max_area_num`: Records the maximum area and common number of the rectangle.
- `execution_time`: Records the time taken for the calculation.
