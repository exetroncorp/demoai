import streamlit as st
import sqlite3
import cv2
import numpy as np
from fast_alpr import ALPR
from fast_alpr.default_detector import PlateDetectorModel
from fast_alpr.default_ocr import OcrModel
from PIL import Image
import io
import base64
from typing import get_args
import openai
import os

# Mistral API Configuration (using OpenAI client with Mistral endpoint)
MISTRAL_API_KEY = "****************************"
MISTRAL_BASE_URL = "https://codestral.mistral.ai/v1"

# Available models
DETECTOR_MODELS = [
    "yolo-v9-t-384-license-plate-end2end",
    "yolo-v9-s-384-license-plate-end2end",
    "yolo-v9-m-384-license-plate-end2end"
]

OCR_MODELS = [
    "global-plates-mobile-vit-v2-model",
    "argentina-plates-mobile-vit-v2-model",
    "europe-plates-mobile-vit-v2-model"
]

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'alpr' not in st.session_state:
    st.session_state.alpr = None

def init_alpr():
    """Initialize ALPR model"""
    if st.session_state.alpr is None:
        with st.spinner("Loading ALPR models..."):
            st.session_state.alpr = ALPR(
                detector_model="yolo-v9-t-384-license-plate-end2end",
                ocr_model="global-plates-mobile-vit-v2-model",
            )

def init_database():
    """Initialize the database with sample data"""
    conn = sqlite3.connect('license_plates.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS license_plates (
            plate_number TEXT PRIMARY KEY,
            owner_name TEXT,
            owner_phone TEXT,
            vehicle_make TEXT,
            vehicle_model TEXT,
            vehicle_color TEXT,
            registration_date TEXT,
            owner_address TEXT,
            owner_photo_url TEXT,
            vehicle_year INTEGER
        )
    ''')

    # Sample data with enhanced information
    sample_data = [
        ('ABC123', 'John Doe', '555-0101', 'Toyota', 'Camry', 'Silver', '2023-01-15', '123 Main St, Paris', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face', 2020),
        ('XYZ789', 'Jane Smith', '555-0102', 'Honda', 'Civic', 'Blue', '2023-02-20', '456 Oak Ave, Lyon', 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face', 2019),
        ('DEF456', 'Bob Johnson', '555-0103', 'Ford', 'F-150', 'Red', '2023-03-10', '789 Pine Rd, Marseille', 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face', 2021),
        ('GHI789', 'Alice Brown', '555-0104', 'BMW', 'X5', 'White', '2023-04-05', '321 Elm St, Nice', 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face', 2022),
        ('OAYG300', 'Zoubida Brown', '555-0104', 'Peugeot', '308', 'Black', '2023-04-05', '654 Cedar Blvd, Toulouse', 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face', 2022),
        ('2DCJ142', 'Yacine Robert', '06 58 40 12 11', 'Toyota', 'Corolla', 'Gray', '2024-04-05', '987 Maple Dr, Bordeaux', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face', 2023),
        ('34137B4', 'Olivier Ludovencia', '06 58 43 12 11', 'Tesla', 'Cyber Zdar', 'Gray','2024-04-05','987 Maple Dr, Bordeaux', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face', 2023),
        ('SKN3028', 'Nador Francis', '06 58 43 25 11', 'Mercedes', '190 Riffevo','Gray', '1989-04-05','987 Maple Dr, Bordeaux', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face', 2023)
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO license_plates
        (plate_number, owner_name, owner_phone, vehicle_make, vehicle_model, vehicle_color, registration_date, owner_address, owner_photo_url, vehicle_year)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_data)

    conn.commit()
    conn.close()

def get_owner_info(plate_number):
    """Get owner information from database"""
    conn = sqlite3.connect('license_plates.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT owner_name, owner_phone, vehicle_make, vehicle_model, registration_date,
               vehicle_color, owner_address, owner_photo_url, vehicle_year
        FROM license_plates WHERE plate_number = ?
    ''', (plate_number,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            'owner_name': result[0],
            'owner_phone': result[1],
            'vehicle_make': result[2],
            'vehicle_model': result[3],
            'registration_date': result[4],
            'photo': result[8]
        }
    return None

def extract_license_plate(image, detector_model="yolo-v9-t-384-license-plate-end2end", ocr_model="global-plates-mobile-vit-v2-model"):
    """Extract license plate from uploaded image using the working FastALPR approach"""
    try:
        # Convert PIL image to numpy array (RGB format)
        img_array = np.array(image.convert("RGB"))

        # Initialize ALPR with selected models
        alpr = ALPR(detector_model=detector_model, ocr_model=ocr_model)

        # Get predictions directly from numpy array
        results = alpr.predict(img_array)

        if results:
            plates = []
            for result in results:
                plate_info = {
                    'text': result.ocr.text if result.ocr else "N/A",
                    'confidence': result.ocr.confidence if result.ocr else 0.0,
                    # Note: bbox is not available in newer versions, we'll get it from drawing
                    'detection': result.detection
                }
                plates.append(plate_info)
            return plates, img_array, alpr
        else:
            return [], img_array, alpr

    except Exception as e:
        st.error(f"Error during license plate recognition: {str(e)}")
        return [], None, None

def add_to_chat(message, is_user=True):
    """Add message to chat history"""
    st.session_state.chat_history.append({
        'message': message,
        'is_user': is_user
    })



def extract_plate_from_query(query):
    """Extract license plate number from user query"""
    import re

    # Look for patterns like ABC123, OAYG300, etc.
    patterns = [
        r'\b[A-Z]{2,3}\d{3,4}\b',  # ABC123, OAYG300
        r'\b\d{3}[A-Z]{2,3}\b',    # 123ABC
        r'\b[A-Z]\d{3}[A-Z]{2}\b', # A123BC
        r'\b[A-Z]{3}\d{3}\b',      # ABC123
    ]

    query_upper = query.upper()
    for pattern in patterns:
        matches = re.findall(pattern, query_upper)
        if matches:
            return matches[0]

    # Also check for common plates mentioned
    words = query_upper.split()
    for word in words:
        # Remove non-alphanumeric characters
        clean_word = re.sub(r'[^A-Z0-9]', '', word)
        if len(clean_word) >= 4 and any(c.isdigit() for c in clean_word) and any(c.isalpha() for c in clean_word):
            return clean_word

    return None

def process_chat_query(query):
    """Process chat queries about license plates - PRIORITIZE AI TOOLS WHEN IMAGE UPLOADED"""

    # Check if there's an uploaded image - if so, let AI use tools first
    if 'last_uploaded_image' in st.session_state and st.session_state.last_uploaded_image is not None:
        st.write("🔧 DEBUG: Image detected - letting AI use tools first")
        return get_ai_response_with_tools(query)

    # If no image, try to extract a plate number from the query text
    extracted_plate = extract_plate_from_query(query)

    if extracted_plate:
        # FORCE real database lookup
        st.write(f"🔍 Extracted plate from query: {extracted_plate}")
        owner_info = get_owner_info(extracted_plate)

        if owner_info:
            return f"""✅ for plate {extracted_plate}:
👤 Owner: {owner_info['owner_name']}
📞 Phone: {owner_info['owner_phone']}
🚗 Vehicle: {owner_info['vehicle_make']} {owner_info['vehicle_model']}
👤 Photo: {owner_info['photo']}
📅 Registered: {owner_info['registration_date']}"""

        else:
            return f"❌ No information found in database for plate: {extracted_plate}"

    # If no specific plate mentioned and no image, check for general queries
    query_lower = query.lower()

    if any(phrase in query_lower for phrase in ['owner', 'who owns', 'car owner', 'vehicle owner']):
        # Get all available plates from database
        conn = sqlite3.connect('license_plates.db')
        cursor = conn.cursor()
        cursor.execute('SELECT plate_number FROM license_plates LIMIT 5')
        available_plates = [row[0] for row in cursor.fetchall()]
        conn.close()

        if available_plates:
            # Show the first available plate as example
            example_plate = available_plates[0]
            owner_info = get_owner_info(example_plate)

            response = f"""I can look up owner information for license plates. Here's an example from our database:

✅ REAL DATA FROM DATABASE for plate {example_plate}:
👤 Owner: {owner_info['owner_name']}
📞 Phone: {owner_info['owner_phone']}
🚗 Vehicle: {owner_info['vehicle_make']} {owner_info['vehicle_model']}
📅 Registered: {owner_info['registration_date']}

Available plates in database: {', '.join(available_plates)}

Ask me about a specific plate number!"""
            return response

    # For other queries, try AI with tools
    return get_ai_response_with_tools(query)

def get_ai_response_with_tools(query):
    """Get AI response with access to real tools"""
    try:
        client = openai.OpenAI(
            api_key=MISTRAL_API_KEY,
            base_url=MISTRAL_BASE_URL
        )

        # Define tools available to the AI
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_owner_info",
                    "description": "Look up owner information for a specific license plate number from the database",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "plate_number": {
                                "type": "string",
                                "description": "The license plate number to look up (e.g., 'ABC123', 'OAYG300')"
                            }
                        },
                        "required": ["plate_number"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "extract_license_plate",
                    "description": "Extract license plate numbers from the currently uploaded image using ALPR technology. Use this tool when the user asks about 'this car', 'this image', 'who owns this car', or mentions an uploaded image. This tool automatically accesses the most recently uploaded image.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "use_uploaded_image": {
                                "type": "boolean",
                                "description": "Always set to true to use the uploaded image"
                            }
                        },
                        "required": ["use_uploaded_image"]
                    }
                }
            }
        ]

        # Check if there's an uploaded image and add context
        image_context = ""
        if 'last_uploaded_image' in st.session_state and st.session_state.last_uploaded_image is not None:
            image_context = "\n\nIMPORTANT: The user has uploaded an image. When they ask about 'this car', 'this image', 'who owns this car', or similar questions referring to an uploaded image, you MUST use the extract_license_plate tool first to extract the plate number, then use get_owner_info to look up the owner."

        messages = [
            {
                "role": "system",
                "content": f"""You are a helpful assistant for a License Plate Recognition system.

                You have access to these tools:
                1. get_owner_info - Look up owner information for license plates in the database
                2. extract_license_plate - Extract license plate numbers from the currently uploaded image

                CRITICAL RULES:
                - When users ask about license plate information with a specific plate number, use get_owner_info
                - When users ask about "this car", "this image", "who owns this car", or refer to an uploaded image, use extract_license_plate FIRST, then get_owner_info
                - ALWAYS use tools when appropriate - do not provide generic responses when tools can give real data
                - NEVER make up or invent license plate data. Always use the tools to get real information.
                - If someone uploads an image and asks about ownership, you MUST use extract_license_plate first{image_context}"""
            },
            {
                "role": "user",
                "content": query
            }
        ]

        # Determine tool choice based on context
        tool_choice = "auto"

        # Force tool usage when image is uploaded and user asks about ownership
        if 'last_uploaded_image' in st.session_state and st.session_state.last_uploaded_image is not None:
            query_lower = query.lower()
            if any(phrase in query_lower for phrase in ['owner', 'who owns', 'this car', 'this image', 'car owner']):
                tool_choice = {"type": "function", "function": {"name": "extract_license_plate"}}
                st.write("🔧 DEBUG: Forcing extract_license_plate tool due to uploaded image + ownership query")

        # Try with tools first
        try:
            response = client.chat.completions.create(
                model="codestral-latest",
                messages=messages,
                tools=tools,
                tool_choice=tool_choice,
                max_tokens=300,
                temperature=0.7,
                parallel_tool_calls=False
            )

            # Check if tools were called
            message = response.choices[0].message

            if hasattr(message, 'tool_calls') and message.tool_calls:
                st.write("🔧 DEBUG: AI is using tools!")

                for tool_call in message.tool_calls:
                    import json
                    args = json.loads(tool_call.function.arguments)

                    if tool_call.function.name == "get_owner_info":
                        plate_number = args.get("plate_number", "").upper()
                        st.write(f"🔧 DEBUG: AI called get_owner_info with: {plate_number}")

                        # Call the actual function
                        owner_info = get_owner_info(plate_number)

                        if owner_info:
                            return f"""✅ (via AI tool) for plate {plate_number}:
👤 Owner: {owner_info['owner_name']}
📞 Phone: {owner_info['owner_phone']}
🚗 Vehicle: {owner_info['vehicle_make']} {owner_info['vehicle_model']}
📅 Registered: {owner_info['registration_date']}"""
                        else:
                            return f"❌ No information found in database for plate: {plate_number}"

                    elif tool_call.function.name == "extract_license_plate":
                        use_uploaded = args.get("use_uploaded_image", True)

                        st.write(f"🔧 DEBUG: AI called extract_license_plate (use_uploaded: {use_uploaded})")

                        # Check if there's an uploaded image in session state
                        if 'last_uploaded_image' in st.session_state:
                            image = st.session_state.last_uploaded_image

                            # Call the actual extraction function with default models
                            result = extract_license_plate(image, "yolo-v9-t-384-license-plate-end2end", "global-plates-mobile-vit-v2-model")

                            if isinstance(result, tuple) and len(result) == 3:
                                plates, _, _ = result
                            else:
                                plates = result if isinstance(result, list) else []

                            if plates:
                                extracted_plates = [plate['text'] for plate in plates]
                                st.write(f"🔧 DEBUG: Extracted plates: {extracted_plates}")

                                # Now look up owner info for the first plate
                                first_plate = extracted_plates[0]
                                owner_info = get_owner_info(first_plate)

                                if owner_info:
                                    return f"""✅ EXTRACTED PLATE: {first_plate}
✅ REAL OWNER DATA FROM DATABASE:
👤 Owner: {owner_info['owner_name']}
📞 Phone: {owner_info['owner_phone']}
🚗 Vehicle: {owner_info['vehicle_make']} {owner_info['vehicle_model']}
📸 Photo: {owner_info['photo']}
📅 Registered: {owner_info['registration_date']}"""
                                else:
                                    return f"✅ EXTRACTED PLATE: {first_plate}\n❌ No owner information found in database"
                            else:
                                return "❌ No license plates detected in the uploaded image"
                        else:
                            return "❌ No image has been uploaded yet. Please upload an image first."

            # If no tools called, return regular response
            return f"🤖 AI Response: {message.content}"

        except Exception as tool_error:
            st.write(f"🔧 DEBUG: Tool calling failed: {tool_error}")
            # Fallback to simple response
            return get_simple_ai_response(query)

    except Exception as e:
        return f"AI service temporarily unavailable. Error: {str(e)}"

def get_simple_ai_response(query):
    """Get AI response without tool calling - just for general questions"""
    try:
        client = openai.OpenAI(
            api_key=MISTRAL_API_KEY,
            base_url=MISTRAL_BASE_URL
        )

        messages = [
            {
                "role": "system",
                "content": """You are a helpful assistant for a License Plate Recognition system.
                You can help users with general questions about:
                1. How ALPR (Automatic License Plate Recognition) works
                2. The application features
                3. Technical questions about license plate detection

                DO NOT make up or invent license plate data. If asked about specific plates,
                tell users to provide a plate number so you can look it up in the database.

                Be helpful and informative about the technology and system."""
            },
            {
                "role": "user",
                "content": query
            }
        ]

        response = client.chat.completions.create(
            model="codestral-latest",
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI service temporarily unavailable. Error: {str(e)}"

# Streamlit App
def main():
    st.set_page_config(
        page_title="ALPR Chat Assistant",
        page_icon="🚗",
        layout="wide"
    )

    st.title("🚗 License Plate Recognition Chat Assistant")
    st.markdown("Upload an image to detect license plates or chat to query owner information!")

    # Initialize database
    init_database()

    # Create two columns
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📸 Image Upload & Recognition")

        # Model selection
        col_det, col_ocr = st.columns(2)
        with col_det:
            detector_model = st.selectbox("Detector Model", DETECTOR_MODELS, index=0)
        with col_ocr:
            ocr_model = st.selectbox("OCR Model", OCR_MODELS, index=0)

        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=['jpg', 'jpeg', 'png'],
            help="Upload an image containing a license plate"
        )

        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Store image in session state for AI tool access
            st.session_state.last_uploaded_image = image

            if st.button("🔍 Detect License Plates", type="primary"):
                with st.spinner("Processing..."):
                    result = extract_license_plate(image, detector_model, ocr_model)

                    # Handle the tuple return from extract_license_plate
                    if isinstance(result, tuple) and len(result) == 3:
                        plates, img_array, alpr = result
                    else:
                        plates = result if isinstance(result, list) else []
                        img_array = None
                        alpr = None

                if plates:
                    st.success(f"Found {len(plates)} license plate(s)!")

                    # Draw predictions on the image if we have the alpr object
                    if img_array is not None and alpr is not None:
                        try:
                            annotated_img_array = alpr.draw_predictions(img_array)
                            annotated_img = Image.fromarray(annotated_img_array)
                            st.image(annotated_img, caption="Annotated Image with OCR Results", use_container_width=True)
                        except Exception as e:
                            st.warning(f"Could not draw annotations: {e}")

                    # Display results
                    for i, plate in enumerate(plates):
                        st.subheader(f"Plate {i+1}")
                        st.write(f"**Text:** `{plate['text']}`")
                        st.write(f"**Confidence:** `{plate['confidence']:.2f}`")

                        # Auto-query owner info
                        owner_info = get_owner_info(plate['text'])
                        if owner_info:
                            st.info("Owner Information Found:")
                            st.write(f"👤 **Owner:** {owner_info['owner_name']}")
                            st.write(f"📞 **Phone:** {owner_info['owner_phone']}")
                            st.write(f"🚗 **Vehicle:** {owner_info['vehicle_make']} {owner_info['vehicle_model']}")
                            st.write(f"📅 **Registered:** {owner_info['registration_date']}")
                            st.write(f"📅 **Photo:** {owner_info['photo']}")

                            # Add to chat
                            add_to_chat(f"Detected plate: {plate['text']}", True)
                            add_to_chat(f"Found owner: {owner_info['owner_name']} - {owner_info['photo']} - {owner_info['vehicle_make']} {owner_info['vehicle_model']}", False)
                        else:
                            st.warning("No owner information found in database")
                            add_to_chat(f"Detected plate: {plate['text']}", True)
                            add_to_chat(f"No owner information found for {plate['text']}", False)
                else:
                    st.warning("No license plates detected in the image 😔")
                    add_to_chat("Uploaded image for analysis", True)
                    add_to_chat("No license plates detected in the image", False)

    with col2:
        st.header("💬 Chat Assistant")

        # Show image upload status
        if 'last_uploaded_image' in st.session_state and st.session_state.last_uploaded_image is not None:
            st.success("📸 Image uploaded! You can now ask: 'Who is the owner of this car?'")
        else:
            st.info("💡 Upload an image first, then ask about the car owner!")

        # Display chat history
        chat_container = st.container()
        with chat_container:
            for chat in st.session_state.chat_history:
                if chat['is_user']:
                    st.markdown(f"**You:** {chat['message']}")
                else:
                    st.markdown(f"**Assistant:** {chat['message']}")

        # Chat input
        user_input = st.text_input(
            "Ask about a license plate...",
            placeholder="e.g., 'What info do you have for plate ABC123?'",
            key="chat_input"
        )

        col_send, col_clear = st.columns([1, 1])

        with col_send:
            if st.button("Send", type="primary") and user_input:
                add_to_chat(user_input, True)
                response = process_chat_query(user_input)
                add_to_chat(response, False)
                st.rerun()

        with col_clear:
            if st.button("Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()

    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This application demonstrates:
        - **License Plate Recognition** using FastALPR
        - **Database Integration** for owner lookup
        - **Interactive Chat Interface**
        - **Real-time Image Processing**

        ### Sample Plates in Database:
        - ABC123 (John Doe)
        - XYZ789 (Jane Smith)
        - DEF456 (Bob Johnson)
        - GHI789 (Alice Brown)
        """)

        st.header("🛠️ Features")
        st.markdown("""
        - Upload images for plate detection
        - Chat-based queries
        - Owner information lookup
        - Confidence scoring
        - Real-time processing
        """)

        st.header("💡 Chat Examples")
        st.markdown("""
        Try these queries:
        - "What info do you have for plate ABC123?"
        - "Look up XYZ789"
        - "Who owns plate DEF456?"
        - "Tell me about GHI789"
        """)

if __name__ == "__main__":
    main()
