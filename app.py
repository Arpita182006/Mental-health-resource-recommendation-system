import streamlit as st
import pandas as pd

# Define resource map
resource_map = {
    'mild': ['Mental Health Tips', 'Exercise & Diet Plan'],
    'moderate': ['Online Counseling', 'Stress Management App'],
    'severe': ['Therapy Session', 'Emergency Helpline']
}

# Define the rule-based recommendation function
def recommend_resources(row):
    severity = row['Severity']
    stress = row['Stress_Level']
    consult = row['Consultation_History']
    work_hours = row['Work_Hours']
    sleep_hours = row['Sleep_Hours']
    activity_hours = row['Physical_Activity_Hours']
    condition = row['Mental_Health_Condition']
    medication = row.get('Medication_Usage', 'No')

    # All Okay Condition
    if (severity == 'mild' and stress == 'low' and consult == 'No' and 
        medication == 'No' and activity_hours >= 1 and sleep_hours >= 7 and work_hours <= 8):
        return [
            'You seem to be doing well! 🎉',
            'Keep up with your self-care routine.',
            'Explore meditation or wellness apps to maintain mental clarity.'
        ]

    if severity == 'mild' and stress in ['low', 1] and activity_hours >= 1:
        return resource_map['mild']

    elif severity == 'moderate' or stress in ['moderate', 2] or (work_hours > 8 and sleep_hours < 6):
        return resource_map['moderate'] + ['Consider reducing your work stress.', 'Improve your sleep schedule.']

    elif severity == 'severe' or "anxiety" in condition.lower() or activity_hours == 0:
        return resource_map['severe'] + ['Seek professional help immediately.']

    else:
        return resource_map['moderate']

# Streamlit UI
st.title("🧠 Mental Health Resource Recommender")

st.markdown("Fill in the details to get personalized mental health resource recommendations.")

severity = st.selectbox("Severity", ['mild', 'moderate', 'severe'])
stress = st.selectbox("Stress Level", ['low', 'moderate', 'high'])
consult = st.selectbox("Have you consulted a professional?", ['Yes', 'No'])
medication = st.selectbox("Are you on any medication?", ['Yes', 'No'])
condition = st.text_input("Describe your mental health condition(calm,anxiety etc)", "")
activity_hours = st.slider("Physical Activity Hours per day", 0, 5, 1)
sleep_hours = st.slider("Sleep Hours per day", 0, 12, 7)
work_hours = st.slider("Work Hours per day", 0, 16, 8)

# Predict button
if st.button("Get Recommendations"):
    user_data = {
        'Severity': severity,
        'Stress_Level': stress,
        'Consultation_History': consult,
        'Medication_Usage': medication,
        'Mental_Health_Condition': condition,
        'Physical_Activity_Hours': activity_hours,
        'Sleep_Hours': sleep_hours,
        'Work_Hours': work_hours
    }

    recommendation = recommend_resources(user_data)
    
    st.success("Recommended Resources:")
    for r in recommendation:
        st.markdown(f"- {r}")
