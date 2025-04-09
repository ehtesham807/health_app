import requests
import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
# import requests
import speech_recognition as sr

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq()

# Streamlit App
st.title("Health Expert 👩🏻‍⚕️")
st.info("This is a robot who is an expert in health-related things. Ask any question related to health.")

# Health Expert Role
robot_role_message = (
    "You are a health expert who can suggest diet, medicine, causes, "
    "provide exercises with video links, and answer all health-related queries."
)

# User Input Section
user_query = st.text_input("Ask anything related to your health")

# Submit Button for Health Queries
if st.button("Submit") and user_query:
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": robot_role_message},
            {"role": "user", "content": user_query},
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        max_completion_tokens=300,
        top_p=1,
        stop=", 6",
        stream=False,
    )

    health_output = chat_completion.choices[0].message.content
    st.text_area("Expert Output", health_output)


# # -------------------------- Voice Input Section --------------------------
st.subheader("Voice Input for Health Queries")
recognizer = sr.Recognizer()
if st.button("Start Listening"):
    with sr.Microphone() as source:
        st.write("Listening... Please speak now.")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.write(f"You said: {text}")

            # Sending voice input to Groq for response
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": robot_role_message},
                    {"role": "user", "content": text},
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_completion_tokens=300,
                top_p=1,
                stop=", 6",
                stream=False,
            )

            health_output = chat_completion.choices[0].message.content
            st.text_area("Expert Output", health_output)

        except sr.UnknownValueError: # type: ignore
            st.write("Sorry, I could not understand you.")
        except sr.RequestError: # type: ignore
            st.write("Sorry, there's an issue with the speech recognition service.")




# -------------------------- Personalized Health Recommendations Section --------------------------

# Function to create personalized health plans
def create_health_plan(age, weight, health_goal):
    exercise_routine = ""
    diet_plan = ""

    if health_goal == "Weight Loss":
        exercise_routine = "Cardio: 30-40 minutes of jogging, cycling, or brisk walking.\nStrength Training: 2-3 days/week."
        diet_plan = "Low-calorie, high-protein meals. Focus on vegetables, lean proteins, and whole grains."
    elif health_goal == "Muscle Gain":
        exercise_routine = "Strength Training: Focus on compound lifts like squats, deadlifts, and bench press.\nCardio: Moderate, 2-3 times a week."
        diet_plan = "Higher protein intake. Include lean meats, legumes, and protein shakes."
    elif health_goal == "General Fitness":
        exercise_routine = "A mix of cardio and strength training, 3-4 times a week."
        diet_plan = "Balanced meals with a mix of carbs, proteins, and healthy fats."

    return exercise_routine, diet_plan

# Function to get dietary suggestions
def get_diet_suggestions(diet_preference, health_goal):
    if diet_preference == "Vegan":
        if health_goal == "Weight Loss":
            return "High-fiber vegetables, legumes, tofu, and quinoa. Avoid processed foods and oils."
        elif health_goal == "Muscle Gain":
            return "High-protein plant-based foods such as lentils, chickpeas, tofu, and tempeh. Include healthy fats like avocados."
        elif health_goal == "General Fitness":
            return "A balanced mix of whole grains, legumes, vegetables, and healthy fats. Ensure adequate protein intake."
    
    elif diet_preference == "Keto":
        if health_goal == "Weight Loss":
            return "Focus on high-fat, low-carb foods like avocados, olive oil, and fatty fish. Avoid carbs."
        elif health_goal == "Muscle Gain":
            return "Eat high-protein, high-fat meals, such as eggs, meat, fish, and low-carb vegetables."
        elif health_goal == "General Fitness":
            return "A moderate amount of protein, high healthy fats, and very low carbs. Avoid starchy vegetables and grains."

    elif diet_preference == "Gluten-Free":
        if health_goal == "Weight Loss":
            return "Avoid gluten-containing grains like wheat. Focus on lean proteins, vegetables, and gluten-free grains like quinoa."
        elif health_goal == "Muscle Gain":
            return "Include gluten-free sources of protein like quinoa, rice, legumes, and lean meats. Avoid processed gluten-free products."
        elif health_goal == "General Fitness":
            return "Eat balanced gluten-free meals with vegetables, fruits, lean proteins, and gluten-free grains."

    else:
        return "Please select a valid dietary preference."

# Streamlit app interface for health plan and diet suggestions
st.subheader("Personalized Health Assistant")

# User input for health plan
age = st.number_input("Enter your age:", min_value=18, max_value=120)
weight = st.number_input("Enter your weight (kg):", min_value=30, max_value=200)
health_goal = st.selectbox("Select your health goal:", ["Weight Loss", "Muscle Gain", "General Fitness"])

# Generate health plan
if st.button("Generate Health Plan"):
    exercise_routine, diet_plan = create_health_plan(age, weight, health_goal)
    st.write(f"### Your Personalized Exercise Routine:")
    st.write(exercise_routine)
    st.write(f"### Your Personalized Diet Plan:")
    st.write(diet_plan)

# User input for dietary suggestions
diet_preference = st.selectbox("Select your dietary preference:", ["Vegan", "Keto", "Gluten-Free"])
health_goal_diet = st.selectbox("Select your health goal for diet:", ["Weight Loss", "Muscle Gain", "General Fitness"])

# Generate dietary suggestions
if st.button("Get Dietary Suggestions"):
    diet_suggestions = get_diet_suggestions(diet_preference, health_goal_diet)
    st.write(f"### Dietary Suggestions for {diet_preference} diet and {health_goal_diet} goal:")
    st.write(diet_suggestions)



## --------------------Emergency Contact-------------------------
if st.button("Emergency Contacts"):
    st.write("""
        📞 **Emergency Numbers:**  
        - **Local Emergency:** 911  
        - **Poison Control:** 1-800-222-1222  
        - **Emergency Services (Global):** 112  
        - **Fire Department:** 101 (India), 999 (UK), 911 (USA)  
    """)


