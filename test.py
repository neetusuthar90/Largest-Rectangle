import requests

def input_matrix():
    rows = int(input()) # Enter the number of rows
    cols = int(input()) # Enter the number of columns
    matrix = []

    # Enter the elements row-wise
    for _ in range(rows):
        row = [int(x) for x in input().split()]
        if len(row) != cols:
            print("Error: Number of elements in each row must be equal to the number of columns.")
            return None
        matrix.append(row)
    return matrix

matrix = input_matrix()
# Test case 1 : According to given test case in assignment square is not consider a rectangle else answer will be 9
# 5
# 6
# 1 1 1 0 1 -9
# 1 1 1 1 2 -9
# 1 1 1 1 2 -9
# 1 0 0 0 5 -9
# 5 0 0 0 5 -9

# Test case 2
# 1
# 2
# 1 1

response = requests.post("http://localhost:8000/input/", json = matrix)
print(response.json())