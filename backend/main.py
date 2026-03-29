from fastapi import FastAPI, UploadFile, File, HTTPException
import requests
import google.generativeai as genai
import os
from dotenv import load_dotenv
from model import predict_disease

load_dotenv()
app = FastAPI(title="FarmShieldX API")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.post("/analyze")
async def analyze_crop(lat: float, lon: float, file: UploadFile = File(...)):
    # 1. Process Image and Predict
    image_bytes = await file.read()
    disease_name = predict_disease(image_bytes)

    # 2. Fetch Environmental Data
    weather_key = os.getenv("WEATHER_API_KEY")
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_key}&units=metric"
    
    try:
        weather_res = requests.get(weather_url).json()
        weather_desc = weather_res.get('weather', [{}])[0].get('description', 'unknown conditions')
        temp = weather_res.get('main', {}).get('temp', 'unknown')
        env_context = f"{weather_desc.capitalize()}, {temp}°C"
    except Exception:
        env_context = "Weather data unavailable"

    # 3. Generate Action Plan via Gemini
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        Act exclusively as an expert agricultural advisor. 
        A farmer has uploaded a photo of a crop diagnosed with: {disease_name}.
        The current local weather is: {env_context}.
        Provide a concise, 3-step actionable mitigation strategy. Account for the weather conditions in your advice. Do not output markdown headers, just a numbered list.
        """
        response = model.generate_content(prompt)
        action_plan = response.text
    except Exception as e:
        action_plan = "Unable to generate advice at this time. Please consult a local agronomist."

    return {
        "disease": disease_name,
        "weather": env_context,
        "action_plan": action_plan
    }