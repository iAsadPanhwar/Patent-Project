import os
def write_to_file(content, directory='project', filename='output.txt'):
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, filename)

    # Ensure content is a string before writing
    if not isinstance(content, str):
        content = str(content)

    with open(file_path, 'w') as file:
        file.write(content)

    print(f"Content written to {file_path}")