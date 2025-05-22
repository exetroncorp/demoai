# Autonomous Agent for License Plate Recognition and Owner Lookup

## Introduction to Agentic Programming

Agentic programming involves creating systems that autonomously make decisions and perform actions based on user input. By integrating large language models (LLMs) with external tools, these systems can handle complex tasks that combine natural language understanding with specific functionalities, such as image processing or database queries.

In this project, we use [Mistral AI's Codestral](https://mistral.ai/), a powerful LLM optimized for code generation and tool use, to build an autonomous agent. The agent interprets a user’s request to identify the owner of a car based on an image of its license plate. It achieves this by extracting the license plate number using Optical Character Recognition (OCR) and querying a SQLite database to retrieve the owner’s information.

## Overview of the Project

The goal is to create an agent that can:
1. Accept a user query, e.g., "Find the owner of the car in this image: car.jpg."
2. Use the LLM to understand the query and decide to extract the license plate number.
3. Call an OCR tool to process the image and extract the license plate number.
4. Query a SQLite database with the license plate number to retrieve the owner’s name.
5. Return the owner’s name to the user.

This demonstrates how LLMs can orchestrate external tools to perform tasks requiring both language comprehension and computational capabilities.

## Components and Their Roles

The system comprises several components, each with a specific role:

1. **LLM (Codestral)**  
   - **Role**: Acts as the decision-making core, interpreting the user’s natural language query and determining which tools to call. Codestral processes the query, generates tool calls, and synthesizes the final response based on tool outputs.

2. **Agent**  
   - **Role**: Orchestrates the workflow by receiving the user’s query, interacting with the LLM, executing tool calls, and managing the flow of information until the final answer is provided.

3. **Tools**  
   - **OCR Tool**: Uses [OpenCV](https://opencv.org/) and [Pytesseract](https://pypi.org/project/pytesseract/) to process an image and extract the license plate number through image processing and text recognition.  
   - **Database Query Tool**: Queries a SQLite database to retrieve the owner’s name based on the license plate number, handling database connections and SQL queries.

4. **SQLite Database**  
   - **Role**: Stores mappings between license plate numbers and owner names in a lightweight, file-based database.

5. **Mistral AI Python Client**  
   - **Role**: Facilitates communication between the agent and Codestral via [Mistral AI’s API](https://docs.mistral.ai/), handling requests and responses.

## Diagram of Component Interactions

The following text-based diagram illustrates how the components interact:

```
User Query
  |
  v
Agent
  |
  v
LLM (Codestral)
  |
  +--> Decides to call OCR Tool
  |      |
  |      v
  |    OCR Tool --> Extracts License Plate Number
  |
  +--> Decides to call Database Query Tool
         |
         v
       Database Query Tool --> Retrieves Owner's Name
         |
         v
Final Answer
```

**Explanation**:
- The user submits a query to the agent.
- The agent passes the query to the LLM (Codestral).
- The LLM decides to call the OCR tool to extract the license plate number.
- The OCR tool processes the image and returns the license plate number.
- The LLM then calls the database query tool with the license plate number.
- The database query tool retrieves the owner’s name.
- The agent collects the results and delivers the final answer to the user.

To create a visual diagram, you can use a tool like [Draw.io](https://www.draw.io) to represent this flow with boxes and arrows.

## 1. Setup Instructions

Install the required Python libraries:

```python
!pip install opencv-python pytesseract mistralai
```

Install Tesseract OCR:
- **Ubuntu**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`
- **Windows**: Download from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) and add to your system’s PATH.

Obtain a Mistral AI API key from [Mistral AI’s console](https://console.mistral.ai/) and set it as an environment variable:
```bash
export MISTRAL_API_KEY='your_key_here'
```

Place a sample image (`car.jpg`) with a visible license plate in your working directory.

## 2. Create the SQLite Database

Create a SQLite database to store license plate numbers and owner names.

```python
import sqlite3

# Connect to the database (creates a new file if it doesn't exist)
conn = sqlite3.connect('license_plates.db')
cursor = conn.cursor()

# Create the table
cursor.execute('''
CREATE TABLE IF NOT EXISTS license_plates (
    license_plate TEXT PRIMARY KEY,
    owner_name TEXT
)
''')

# Insert sample data
sample_data = [
    ('ABC123', 'John Doe'),
    ('XYZ789', 'Jane Smith'),
    ('123ABC', 'Alice Johnson')
]
cursor.executemany('INSERT OR IGNORE INTO license_plates VALUES (?, ?)', sample_data)
conn.commit()
conn.close()
```

This creates `license_plates.db` with a table mapping license plates to owners.

## 3. Implement the OCR Function

The OCR function uses OpenCV and Pytesseract to extract the license plate number from an image.

```python
import cv2
import pytesseract
from matplotlib import pyplot as plt

def extract_license_plate(image_path):
    try:
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            return "Error: Could not load image"

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # Sort contours by area and keep the largest one
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

        if not contours:
            return "No license plate found"

        # Extract the license plate region
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            plate_region = gray[y:y+h, x:x+w]

            # Apply OCR
            text = pytesseract.image_to_string(plate_region, config='--psm 8')

            # Clean the text
            text = ''.join(e for e in text if e.isalnum()).strip()

            if text:
                return text
            return "No license plate found"

    except Exception as e:
        return f"Error during OCR: {str(e)}"

# Test the function
image_path = 'car.jpg'
plate_number = extract_license_plate(image_path)
print(f"Extracted license plate: {plate_number}")
```

**Note**: This is a basic implementation. For better accuracy, consider advanced preprocessing or libraries like [OpenALPR](https://github.com/openalpr/openalpr).

## 4. Implement the Database Query Function

This function retrieves the owner’s name from the database using the license plate number.

```python
def get_owner_info(license_plate):
    try:
        conn = sqlite3.connect('license_plates.db')
        cursor = conn.cursor()
        cursor.execute('SELECT owner_name FROM license_plates WHERE license_plate = ?', (license_plate,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        return "Owner not found"
    except Exception as e:
        return f"Error querying database: {str(e)}"

# Test the function
print(get_owner_info('ABC123'))  # Should return 'John Doe'
print(get_owner_info('Unknown'))  # Should return 'Owner not found'
```

## 5. Define the Tools

Define the OCR and database query functions as tools using OpenAI-style JSON schemas.

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "extract_license_plate",
            "description": "Extract the license plate number from an image",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the image file"
                    }
                },
                "required": ["image_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_owner_info",
            "description": "Get the owner's information from the license plate number",
            "parameters": {
                "type": "object",
                "properties": {
                    "license_plate": {
                        "type": "string",
                        "description": "The license plate number"
                    }
                },
                "required": ["license_plate"]
            }
        }
    }
]
```

## 6. Set Up the Mistral Client

Initialize the Mistral AI client with your API key.

```python
import os
from mistralai import Mistral
import json

# Initialize the Mistral client
api_key = os.environ.get("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY environment variable not set")
client = Mistral(api_key=api_key)
```

## 7. Build the Autonomous Agent

The agent processes the user’s query, calls tools as needed, and returns the final answer.

```python
# Initial user message
messages = [
    {"role": "user", "content": "Find the owner of the car in this image: car.jpg"}
]

# Map function names to actual functions
names_to_functions = {
    "extract_license_plate": extract_license_plate,
    "get_owner_info": get_owner_info
}

# Process tool calls
while True:
    response = client.chat.complete(
        model="codestral-latest",
        messages=messages,
        tools=tools,
        tool_choice="any",
        parallel_tool_calls=False
    )

    # Check for tool calls
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        # Execute the function
        if function_name in names_to_functions:
            result = names_to_functions[function_name](**function_args)
            messages.append({
                "role": "tool",
                "name": function_name,
                "content": str(result)
            })
        else:
            messages.append({
                "role": "tool",
                "name": function_name,
                "content": "Error: Function not implemented"
            })
    else:
        # No more tool calls; get the final answer
        final_answer = response.choices[0].message.content
        print("Final Answer:", final_answer)
        break
```

## 8. Example Workflow

For the query “Find the owner of the car in this image: car.jpg”:
1. The agent sends the query to Codestral.
2. Codestral calls `extract_license_plate({"image_path": "car.jpg"})`, which might return “ABC123”.
3. The agent appends the result and Codestral calls `get_owner_info({"license_plate": "ABC123"})`, returning “John Doe”.
4. The agent outputs: “The owner of the car is John Doe.”

## 9. Considerations and Improvements

- **OCR Accuracy**: The OCR function may struggle with low-quality images. Consider advanced preprocessing or [OpenALPR](https://github.com/openalpr/openalpr).
- **Error Handling**: Add checks for image file existence and valid license plate formats.
- **Extensions**: Support multiple images, add a web interface, or include more database fields.

## 10. Sample Database Table

| License Plate | Owner Name     |
|---------------|----------------|
| ABC123        | John Doe       |
| XYZ789        | Jane Smith     |
| 123ABC        | Alice Johnson  |

## 11. Conclusion

This notebook demonstrates how to build an autonomous agent using Codestral and external tools. It showcases the power of agentic programming for tasks requiring both language understanding and computational actions. You can extend this by improving OCR accuracy or integrating with real-world systems.