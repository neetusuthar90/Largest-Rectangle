from collections import defaultdict
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import time

# Define the BaseModel for the database storage
class MatrixModel(BaseModel):
    matrix: list[list[int]]
    max_area_num: tuple
    execution_time: float

# Define a class to handle database operations
class Database:
    def __init__(self, db_name):
        # Establish connection and cursor
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        # SQL query to create the table
        query = """
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matrix TEXT NOT NULL,
            max_area_num TEXT NOT NULL,
            execution_time REAL NOT NULL
        )
        """
        self.cursor.execute(query)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Commit changes and close connection when exiting the context
        self.connection.commit()
        self.connection.close()

    def save_result(self, matrix, max_area_num, execution_time):
        # SQL query to insert a result into the table
        query = "INSERT INTO results (matrix, max_area_num, execution_time) VALUES (?, ?, ?)"
        # Execute the query with the provided parameters
        self.cursor.execute(query, (str(matrix), str(max_area_num), execution_time))


app = FastAPI()

# Helper function to find the largest rectangle area
def largest_rectangle_area(histogram):
    stack = []
    max_area = 0
    n = len(histogram)
    for i in range(n + 1):
        while stack and (i == n or histogram[stack[-1]] >= histogram[i]):
            height = histogram[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, width * height)
        stack.append(i)
    return max_area

# Helper function to find the maximum sub-rectangle area in a matrix
def max_sub_rectangle_area(matrix, n, m):
    max_area = 0
    height = [0] * m
    for i in range(n):
        for j in range(m):
            if matrix[i][j] == 1:
                height[j] += 1
            else:
                height[j] = 0
        area = largest_rectangle_area(height)
        max_area = max(max_area, area)
    return max_area

# Define the endpoint for receiving matrix input
@app.post("/input")
def largest_rectangle(matrix: list[list[int]]) -> tuple:
    # Start measuring execution time
    start_time = time.time()
    
    rows, cols = len(matrix), len(matrix[0])
    visited = [[0] * cols for _ in range(rows)]
    
    # Initialize a defaultdict to store elements of the same type
    mp = defaultdict(list)

    # Initialize variables for the maximum area and the number associated with it
    max_area = 0
    num = -1
    
    # Depth-first search function to traverse connected elements
    def dfs(i, j, elem, nr, nc):
        if i < 0 or i >= rows or j < 0 or j >= cols or visited[i][j] or matrix[i][j] != elem:
            return nr, nc
        visited[i][j] = 1
        mp[matrix[i][j]].append((i, j))
        nr = max(nr, i)
        nc = max(nc, j)
        dx = [1, 0, -1, 0]
        dy = [0, -1, 0, 1]
        for k in range(4):
            newx = i + dx[k]
            newy = j + dy[k]
            nr, nc = dfs(newx, newy, elem, nr, nc)
        return nr, nc
    
    # Iterate over each element in the matrix
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j]:
                mp[matrix[i][j]] = []
                nr, nc = dfs(i, j, matrix[i][j], 0, 0)
                sub_mat = [[0] * (nc + 1) for _ in range(nr + 1)]
                for x, y in mp[matrix[i][j]]:
                    sub_mat[x][y] = 1
                area = max_sub_rectangle_area(sub_mat, nr + 1, nc + 1)
                if area > max_area:
                    max_area = area
                    num = matrix[i][j]
                    
    # Stop measuring execution time
    end_time = time.time()
    execution_time = end_time - start_time
    
     # Save the result to the database
    with Database("database.sqlite") as db:
        db.save_result(matrix, (num, max_area), execution_time)
        
    # Return the number associated with the maximum area and the maximum area itself
    return num,max_area

