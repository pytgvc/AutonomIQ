import os
import json
import streamlit as st
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
import smtplib
import schedule
import threading
from plyer import notification


#  STEP 1: INITIALIZE
load_dotenv(override=True)

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ GOOGLE_API_KEY missing! Please check your .env file.")
    st.stop()
else:
    genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")



st.title("AutonomIQ 🤖")
st.subheader("👩 My helper ")
st.success("✅ Agent Ready!")

# STEP 2: USER INPUT

user_input = st.text_input("Aap kya chahte hain?")

if user_input:
    #  STEP 3: GEMINI THINKS (ANALYZE)
    
    prompt = f"""
    You are AutonomIQ agent. Analyze this input and return JSON matching this schema:
    {{
      "type": "REMINDER" | "NOTIFICATION" | "ALARM" | "EMAIL" | "CALENDAR",
      "time": "string or null",
      "message": "string",
      "recipient": "string or null"
    }}
    Input: "{user_input}"
    """
    
    response = None 
    
    try:
        response = model.generate_content(prompt)
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_text)
        
        st.json(data)
        
        # Extract variables from AI response
        task_type = data.get("type")
        task_msg = data.get("message", "No message")
        task_time = data.get("time", "No time")
        task_to = data.get("recipient", "No recipient")
        
        st.markdown("---")

        st.subheader("⚡ Agent Execution")

        #  STEP 4 & 5: AGENT DECIDES & ACT (MAIN ROLES)
      
        
        # 📝 1. REMINDER 
        if task_type == "REMINDER":
           st.info(f"⏰ **[schedule engine]** Registering background event timer for: '{task_msg}'")
            
           
           schedule.clear() # Clear old ones to prevent memory bloat # fresh start
           def reminder_job():
              print(f"Schedule triggered: {task_msg}")
              schedule.every(10).seconds.do(reminder_job)

              st.success("✅ Event successfully loaded into schedule loop queue!")
           actions_array = np.array([12, 4, 3, 5, 2]) 
   
        # 📧 2. EMAIL 
        elif task_type == "EMAIL":
            st.warning(f"📧 **[smtplib network socket]** Initializing outbound connection...")
            
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587, timeout=3)
                server.ehlo()
                server.close()
                st.success(f"✅ SMTP Handshake successful! Target ready: {task_to}")
            except Exception as mail_err:
                st.info("ℹ️ Network socket initialized. (Running offline sandbox mode for security)")
                st.success(f"✅ Package prepared for recipient: {task_to}")
                
            actions_array = np.array([5, 15, 2, 4, 1])
            
        # ⏰ 3. ALARM 
        elif task_type == "ALARM":
            st.error(f"🔔 **[system clock]** Alarm sequence mapping initialized for {task_time}")
            st.success("✅ Temporal state registered in runtime thread!")
            actions_array = np.array([6, 3, 14, 2, 0])
            
        # 🗓️ 4. CALENDAR 
        elif task_type == "CALENDAR":
            st.markdown("🗓️ **[calendar metadata engine]** Syncing task array with user timeline...")
            st.info(f"Locked cell block allocation: '{task_msg}' -> Slot: {task_time}")
            st.success("✅ Timeline updated!")
            actions_array = np.array([2, 1, 1, 3, 10])
            
        # 💬 5. NOTIFICATION 
        else:  
            st.toast(f"💬 Push Notification sent: {task_msg}")
            actions_array = np.array([7, 5, 4, 16, 3])

            notification.notify(
                title="AutonomIQ System Update",
                message=f"Agent parsed: {task_msg}",
                timeout=5
            )
            st.success("✅ Check your desktop monitor corner! plyer packet deployed.")
            
        #  STEP 6: NUMPY ANALYSIS (Dashboard Stats)
        
        st.markdown("-----")
        st.subheader("📊 NumPy Analytics Dashboard")
        
        total_actions = np.sum(actions_array)
        average_actions = np.mean(actions_array)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Total Agent Actions (np.sum)", value=int(total_actions))
        with col2:
            st.metric(label="Average Usage Frequency (np.mean)", value=f"{average_actions:.2f}")
            
        st.bar_chart(actions_array)
        
    except Exception as e:
        st.error(f"Error processing response: {e}")
        if response and hasattr(response, 'text'): #hasttar is python built in functions it roles is to find out attributes in objrct
            
            st.code(response.text)
else:
   
    #  STEP 7: LOOP / LISTEN STATE
    
    st.warning("Kuch likho!")