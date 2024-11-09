import json
import pyodbc
import os

def insert_data_into_db(json_file, connection_string):
    """
    Inserts data from a JSON file into the accommodations table in the SQL Server database.
    
    Parameters:
    - json_file: Path to the JSON file to be inserted.
    - connection_string: The connection string to connect to the SQL Server database.
    """
    # Print the current working directory for debugging
    print(f"Current Working Directory: {os.getcwd()}")

    # Step 1: Read the JSON data from the file
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            accommodations = json.load(file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please make sure the JSON file path is correct.")
        return

    # Step 2: Establish a connection to the SQL Server
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Step 3: Insert each accommodation into the accommodations table
    for accommodation in accommodations:
        title = accommodation.get('title', '')
        location = accommodation.get('location', '')
        description = accommodation.get('description', '')
        link = accommodation.get('link', '')

        # Execute the insert command
        cursor.execute("""
            INSERT INTO accommodations (title, location, description, link)
            VALUES (?, ?, ?, ?)
        """, title, location, description, link)

    # Step 4: Commit the transaction and close the connection
    conn.commit()
    cursor.close()
    conn.close()
    print("Data successfully inserted into the accommodations database.")

# Define the connection string for your SQL Server
connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-9UFQHR5\\WOOFYASERVER;"  # Make sure this is the correct server name
    "Database=Accommodation;"                   # Correct database name
    "Trusted_Connection=yes;"                   # Use Windows Authentication
)


# Use the absolute path for the cleaned JSON file
current_directory = os.path.dirname(os.path.abspath(__file__))  # Get the script's current directory
json_file = os.path.join(current_directory, "combined_data.json")  # Update to the correct file path

# Run the script to insert data
insert_data_into_db(json_file, connection_string)
