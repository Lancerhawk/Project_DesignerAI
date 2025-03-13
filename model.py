import streamlit as st
import google.generativeai as genai
import requests
import time

api_key = "Gemini_API_Key"
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 2048,  
    "response_mime_type": "text/plain",
}

def generate_design_idea(style, size, rooms):
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )

    context = f"""
    Create a custom home design plan with the following details:
    Style: {style}
    Size: {size}
    Rooms: {rooms}

    Provide:
    1️⃣ A detailed **home design description** including concept, materials, and key features.
    2️⃣ A **room layout** explaining space distribution.
    3️⃣ A simple **ASCII flowchart** representing the design process.
    """

    chat_session = model.start_chat(history=[{"role": "user", "parts": [context]}])
    response = chat_session.send_message(context)

    if response and response.candidates:
        text = response.candidates[0].content if isinstance(response.candidates[0].content, str) else response.candidates[0].content.parts[0].text
        
        print("\n🏠 AI-Generated Home Design Idea:\n")
        print(text)  

        return text

    return "⚠️ Failed to generate design idea."

def fetch_image_from_lexica(style):
    lexica_url = f"https://lexica.art/search?q={style}"
    
    try:
        response = requests.get(lexica_url)

        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code} from Lexica API")
            return None

        data = response.json()
        
        if 'images' in data and isinstance(data['images'], list) and len(data['images']) > 0:
            image_url = data['images'][0].get('src')
            print(f"Fetched Image URL: {image_url}")  
            return image_url
        else:
            print("No images found in Lexica response.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except requests.exceptions.JSONDecodeError:
        print("Error: Could not parse JSON from Lexica API")
        return None

st.set_page_config(page_title="AI Room Designer", page_icon="🏡", layout="centered")

st.title("🏡 AI Home Design Generator")

st.markdown("Generate home design ideas and find inspiration instantly!")

st.sidebar.header("Enter Design Details")
style = st.sidebar.text_input("Home Style (e.g., Modern, Rustic)", placeholder="Enter home style")
size = st.sidebar.text_input("Home Size (e.g., 2000 sq ft)", placeholder="Enter size")
rooms = st.sidebar.text_input("Number of Rooms", placeholder="Enter number of rooms")

if st.sidebar.button("Generate Design"):
    if style and size and rooms:
        with st.spinner("🤖 AI is generating your design idea..."):
            time.sleep(2) 
            design_idea = generate_design_idea(style, size, rooms)

        # st.subheader("🏠Your AI-Generated Home Design Idea")
        st.markdown(design_idea) 

        with st.spinner("🔍 Searching for inspiration images..."):
            image_url = fetch_image_from_lexica(style)

        if image_url:
            st.image(image_url, caption="Design Inspiration from Lexica.art", use_column_width=True)
        else:
            st.warning("⚠️ No relevant images found on Lexica.art.")
    else:
        st.error("🚨 Please fill in all fields before generating!")

st.markdown("---")
st.markdown("💡 **AI Home Design Generator** - Powered by Google Gemini & Lexica")
