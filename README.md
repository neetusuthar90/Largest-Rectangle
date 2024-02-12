## Largest Rectangle in a Matrix

This FastAPI application calculates the largest rectangle of 1s in a binary matrix and stores the result in a SQLite database.

## Assumptions
- The application handles missing values in the given test case appropriately.
- The largest possible area is considered to be 9, as a square is also a type of rectangle. If the requirement is for the maximum area to be 8, the function needs to ensure that the height and width are never the same. In such a case, a matrix of size 1x1 would be considered an invalid input for the function.

## Dependencies
- Python 3.6 or higher
- FastAPI
- Pydantic
- SQLite3

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/your-repo.git
   ```

2. Install the dependencies using pip:

   ```bash
   pip install fastapi uvicorn
   ```

## Usage

1. Start the FastAPI server:

    ```bash
    uvicorn main:app 
    ```

2. Send POST requests to the /input endpoint with a JSON body containing the histogram matrix. The matrix should be a list of lists representing rows and columns.

3. The server will respond with a JSON array containing the dimensions of the largest rectangle found, including the maximum area and common integer in that rectangle.

## Testing
This project includes tests using `pytest`. Run the tests with the following command:

```bash
pytest
```
The tests include:

1. Unit tests for the largest_rectangle function.
2. Integration tests for the FastAPI endpoint.


## Database

The results are stored in a SQLite database named `database.sqlite`. The database has a table named `results`, where each row represents a calculation result. The table schema is as follows:

```sql
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    matrix TEXT NOT NULL,
    max_area TEXT NOT NULL,
    execution_time REAL NOT NULL
)
```

- `matrix`: Stores the input matrix as a string.
- `max_area`: Records the maximum area of the rectangle.
- `execution_time`: Records the time taken for the calculation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
