import streamlit as st
import requests

def request_demo(name, phone_number, use_case, actor_id):
    # Grab the API key securely
    api_key = st.secrets["api_keys"]["bland_ai"]
    
    # Define the prompt
    prompt = f"""
    BACKGROUND INFO:
    Your name is Bittoo Aggarwal, and you're part of the Business Development team at Geekster. Your role involves calling and qualifying inbound leads shortly after they submit an inquiry on the Geekster website. If a lead seems surprised by the prompt response, you can explain that you're an AI phone agent designed to assist them by providing information and addressing their needs.
    ...
    * Their name is {name}
    * Their use case is {use_case}
    You: Would it be helpful if I sent you a brochure and more detailed information about our programs via WhatsApp?
    Them: "Some response"
    You: Thank you for your time. I'll send the details shortly, and feel free to reach out if you have any questions!
    """
    
    # Define the transfer phone number
    TRANSFER_PHONE_NUMBER = "+917982884305"
    
    # Create the data for the POST request
    data = {
        "phone_number": phone_number,
        "task": prompt,
        "voice_id": actor_id,
        "reduce_latency": True,
        "transfer_phone_number": TRANSFER_PHONE_NUMBER,
    }
    
    # Make the POST request to dispatch the phone call
    try:
        response = requests.post(
            "https://api.bland.ai/call",
            json=data,
            headers={
                "authorization": api_key,
                "Content-Type": "application/json",
            },
        )
        response_data = response.json()
        if response.status_code == 200 and response_data.get("status"):
            return {"message": "Phone call dispatched", "status": "success"}
        else:
            return {"message": "Error dispatching phone call", "status": "error"}
    except Exception as e:
        return {"message": f"Error: {e}", "status": "error"}

# Actor dictionary
actor_dict = {
    "Indian Male": "4ca175b7-3d84-45d2-83d3-c97f0839815c",
    "American Male": "2c01ebe7-45d4-4b58-9686-617fa283dd8e",
    "American Female": "13843c96-ab9e-4938-baf3-ad53fcee541d"
}

# Streamlit app layout
st.title("Receive a Phone Call from VirtualVoice")

name = st.text_input("What's your name?", "Saurabh")
phone_number = st.text_input("What's your phone number?", "+91 ")

actor = st.selectbox("Select voice agent you are expecting", list(actor_dict.keys()))
actor_id = actor_dict[actor]

if st.button("Talk to VirtualVoice"):
    response = request_demo(name, phone_number, "student", actor_id)
    st.write("API Response:")
    st.write(response)

# To run the Streamlit app, save this script and use the command: streamlit run script.py
