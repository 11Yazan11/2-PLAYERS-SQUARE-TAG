import itertools
import ast


def choose_desired_map(map_number):
    map_number -= 1

    matrix_lines_len = 21779

    # Step 1: Count the total number of lines in the file
    with open('matrix_text.txt', 'r') as file:
        line_count = sum(1 for line in file)

    # Step 2: Calculate the number of matrices in the file
    map_count = line_count // matrix_lines_len

    # Step 3: Generate the line ranges for each matrix
    key_lines = []
    for i in range(map_count):
        start_line = matrix_lines_len * i + 1
        end_line = matrix_lines_len * (i + 1)
        key_lines.append((start_line, end_line))

    # Step 4: Select the desired matrix (e.g., the third matrix)
    map_index = map_number

    with open('matrix_text.txt', 'r') as reader:
        # Calculate the correct start and end lines to read
        start_line = key_lines[map_index][0] - 1
        end_line = key_lines[map_index][1]
    
    # Read the lines for the selected matrix
        lines = list(itertools.islice(reader, start_line, end_line))

    # Step 5: Combine the lines into a single string and parse the matrix
    content = ''.join(lines)
    # Skip the "matrix =" part and parse the remaining content
    matrix = ast.literal_eval(content.split('=', 1)[1].strip())

    return matrix
