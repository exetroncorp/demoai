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
import numpy as np
import re
from matplotlib import pyplot as plt

def extract_license_plate(image_path):
    """
    Enhanced license plate extraction with multiple detection strategies
    """
    try:
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            return "Error: Could not load image"

        # Try multiple detection strategies
        strategies = [
            _strategy_contour_detection,
            _strategy_direct_ocr,
            _strategy_morphological,
            _strategy_adaptive_threshold
        ]

        for strategy in strategies:
            result = strategy(image)
            if result and _is_valid_license_plate(result):
                return result

        return "No license plate found"

    except Exception as e:
        return f"Error during OCR: {str(e)}"

def _strategy_contour_detection(image):
    """Strategy 1: Improved contour-based detection"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply bilateral filter to reduce noise while preserving edges
    filtered = cv2.bilateralFilter(gray, 11, 17, 17)

    # Edge detection with multiple thresholds
    edges = cv2.Canny(filtered, 30, 200)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours by license plate characteristics
    plate_candidates = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 1000:  # Too small
            continue

        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h

        # License plates typically have aspect ratio between 2:1 and 5:1
        if 2.0 <= aspect_ratio <= 5.0 and area > 1000:
            plate_candidates.append((contour, area, x, y, w, h))

    # Sort by area and try the largest candidates
    plate_candidates.sort(key=lambda x: x[1], reverse=True)

    for candidate in plate_candidates[:3]:  # Try top 3 candidates
        _, _, x, y, w, h = candidate
        plate_region = gray[y:y+h, x:x+w]

        # Enhance the plate region
        enhanced_plate = _enhance_plate_region(plate_region)

        # Try OCR with different configurations
        for config in ['--psm 8', '--psm 7', '--psm 6']:
            text = pytesseract.image_to_string(enhanced_plate, config=config)
            cleaned_text = _clean_license_plate_text(text)
            if cleaned_text and len(cleaned_text) >= 4:
                return cleaned_text

    return None

def _strategy_direct_ocr(image):
    """Strategy 2: Direct OCR on the whole image"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Enhance the entire image
    enhanced = _enhance_plate_region(gray)

    # Try OCR on the whole image
    text = pytesseract.image_to_string(enhanced, config='--psm 6')

    # Extract potential license plate patterns
    patterns = re.findall(r'\b[A-Z0-9]{4,8}\b', text.upper())
    for pattern in patterns:
        if _is_valid_license_plate(pattern):
            return pattern

    return None

def _strategy_morphological(image):
    """Strategy 3: Morphological operations to find rectangular regions"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Blackhat operation to highlight dark regions
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)

    # Gradient to find edges
    grad = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)

    # Combine blackhat and gradient
    combined = cv2.add(blackhat, grad)

    # Threshold
    _, thresh = cv2.threshold(combined, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h
        area = cv2.contourArea(contour)

        if 2.0 <= aspect_ratio <= 5.0 and area > 1000:
            plate_region = gray[y:y+h, x:x+w]
            enhanced_plate = _enhance_plate_region(plate_region)

            text = pytesseract.image_to_string(enhanced_plate, config='--psm 8')
            cleaned_text = _clean_license_plate_text(text)
            if cleaned_text and len(cleaned_text) >= 4:
                return cleaned_text

    return None

def _strategy_adaptive_threshold(image):
    """Strategy 4: Adaptive thresholding approach"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive threshold
    adaptive_thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # Find contours
    contours, _ = cv2.findContours(adaptive_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h
        area = cv2.contourArea(contour)

        if 2.0 <= aspect_ratio <= 5.0 and area > 1000:
            plate_region = gray[y:y+h, x:x+w]
            enhanced_plate = _enhance_plate_region(plate_region)

            text = pytesseract.image_to_string(enhanced_plate, config='--psm 8')
            cleaned_text = _clean_license_plate_text(text)
            if cleaned_text and len(cleaned_text) >= 4:
                return cleaned_text

    return None

def _enhance_plate_region(plate_region):
    """Enhance the license plate region for better OCR"""
    # Resize if too small
    if plate_region.shape[1] < 200:
        scale_factor = 200 / plate_region.shape[1]
        new_width = int(plate_region.shape[1] * scale_factor)
        new_height = int(plate_region.shape[0] * scale_factor)
        plate_region = cv2.resize(plate_region, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(plate_region)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)

    # Apply sharpening kernel
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(blurred, -1, kernel)

    return sharpened

def _clean_license_plate_text(text):
    """Clean and validate extracted text"""
    # Remove non-alphanumeric characters
    cleaned = re.sub(r'[^A-Z0-9]', '', text.upper())

    # Remove common OCR mistakes
    replacements = {
        'O': '0', 'I': '1', 'S': '5', 'Z': '2', 'B': '8'
    }

    for old, new in replacements.items():
        # Only replace if it makes sense in context
        if len(cleaned) > 4 and old in cleaned:
            # Simple heuristic: if more numbers than letters, likely a number
            if sum(c.isdigit() for c in cleaned) > sum(c.isalpha() for c in cleaned):
                cleaned = cleaned.replace(old, new)

    return cleaned.strip()

def _is_valid_license_plate(text):
    """Validate if text looks like a license plate"""
    if not text or len(text) < 4 or len(text) > 8:
        return False

    # Check if it contains both letters and numbers (common pattern)
    has_letter = any(c.isalpha() for c in text)
    has_number = any(c.isdigit() for c in text)

    # Most license plates have both letters and numbers
    return has_letter and has_number

# Test the function
image_path = 'car.jpg'
plate_number = extract_license_plate(image_path)
print(f"Extracted license plate: {plate_number}")
```

**Note**: This enhanced implementation uses multiple strategies for better accuracy. For even better results, consider these alternatives:

### Alternative Libraries for License Plate Recognition

1. **EasyOCR** - More accurate than Tesseract for license plates:
```python
# Install: pip install easyocr
import easyocr

def extract_license_plate_easyocr(image_path):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path)

    for (bbox, text, confidence) in results:
        if confidence > 0.5 and _is_valid_license_plate(text):
            return text.upper().replace(' ', '')

    return "No license plate found"
```

2. **OpenALPR** - Professional-grade license plate recognition:
```python
# Install: pip install openalpr
from openalpr import Alpr

def extract_license_plate_openalpr(image_path):
    alpr = Alpr("us", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
    if not alpr.is_loaded():
        return "Error: OpenALPR not loaded"

    results = alpr.recognize_file(image_path)
    alpr.unload()

    if results['results']:
        return results['results'][0]['plate']

    return "No license plate found"
```

3. **PaddleOCR** - High accuracy OCR from Baidu:
```python
# Install: pip install paddlepaddle paddleocr
from paddleocr import PaddleOCR

def extract_license_plate_paddle(image_path):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    results = ocr.ocr(image_path, cls=True)

    for line in results:
        for word_info in line:
            text = word_info[1][0]
            confidence = word_info[1][1]
            if confidence > 0.5 and _is_valid_license_plate(text):
                return text.upper().replace(' ', '')

    return "No license plate found"
```

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

# Process tool calls sequentially until we have all results
tool_results = []
max_iterations = 3  # Prevent infinite loops

for iteration in range(max_iterations):
    response = client.chat.complete(
        model="codestral-latest",
        messages=messages,
        tools=tools,
        tool_choice="any",
        parallel_tool_calls=False  # Sequential calls since they depend on each other
    )

    # Check for tool calls
    if response.choices[0].message.tool_calls:
        # Execute all tool calls in this iteration
        for tool_call in response.choices[0].message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            # Execute the function
            if function_name in names_to_functions:
                result = names_to_functions[function_name](**function_args)
                tool_results.append({
                    "function": function_name,
                    "arguments": function_args,
                    "result": result
                })

                # Add result as user message instead of tool role
                messages.append({
                    "role": "user",
                    "content": f"Result of {function_name}({function_args}): {result}"
                })
            else:
                tool_results.append({
                    "function": function_name,
                    "arguments": function_args,
                    "result": "Error: Function not implemented"
                })

                messages.append({
                    "role": "user",
                    "content": f"Error: {function_name} not implemented"
                })
    else:
        # No more tool calls, we're done
        break

# Create a summary of all tool results and request table format
if tool_results:
    results_summary = "All tool execution results:\n"
    for i, tool_result in enumerate(tool_results, 1):
        results_summary += f"{i}. {tool_result['function']}({tool_result['arguments']}) -> {tool_result['result']}\n"

    # Add the results summary and request table format
    messages.append({
        "role": "user",
        "content": f"{results_summary}\nPlease format your final response as a table showing the results clearly."
    })

    # Get the final formatted response without tools
    final_response = client.chat.complete(
        model="codestral-latest",
        messages=messages,
        tools=None  # Disable tools to prevent further tool calls
    )

    final_answer = final_response.choices[0].message.content
    print("Final Answer:", final_answer)
else:
    # No tool calls were made
    final_answer = response.choices[0].message.content
    print("Final Answer:", final_answer)
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
