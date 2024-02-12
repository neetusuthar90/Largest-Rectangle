from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import time

class matrix_model(BaseModel):
    matrix: list[list[int]]
    max_area: tuple
    execution_time: float

connection = sqlite3.connect("database.sqlite")
cursor = connection.cursor()

app = FastAPI()

@app.post("/input")
def largest_rectangle(matrix: list[list[int]]) -> tuple:
    start_time = time.time()

    if not matrix or not matrix[0]:
        return 0, 0
    
    rows, cols = len(matrix), len(matrix[0])
    max_area = 0
    max_num = None
    track = set()
    # Define a helper function to calculate the area of the rectangle
    def calculate_area(heights):
        stack = []
        max_area = 0
        i = 0
        while i <= len(heights):
            h = heights[i] if i < len(heights) else 0
            if not stack or h >= heights[stack[-1]]:
                stack.append(i)
                i += 1
            else:
                top = stack.pop()
                width = i if not stack else i - stack[-1] - 1
                if heights[top] != width:
                    max_area = max(max_area, heights[top] * width)
        return max_area
    
    # Iterate over each cell in the matrix
    for i in range(rows):
        for j in range(cols):
            # Initialize the heights array with 0s
            heights = [0] * cols
            if matrix[i][j] not in track:
                track.add(matrix[i][j])
                for k in range(i, rows):
                    # Update the heights array with the count of consecutive cells with the same number
                    for l in range(j, cols):
                        if matrix[k][l] == matrix[i][j]:
                            heights[l] += 1
                        else:
                            break
                    # Calculate the area of the rectangle with the current cell as the top-left corner
                    area = calculate_area(heights)
                    # Update the maximum area and number if necessary
                    if area > max_area:
                        max_area = area
                        max_num = matrix[i][j]
            else:
                continue
    end_time = time.time()
    execution_time = end_time - start_time
    response = tuple(max_num, max_area)
    data = matrix_model(matrix=matrix, max_area=response, execution_time=execution_time)
    
    return max_num, max_area
