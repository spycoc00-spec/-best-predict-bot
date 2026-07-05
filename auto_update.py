from google import genai
import requests
import json
import os

# গিটহাব সিক্রেট থেকে তথ্য
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FIREBASE_URL = "https://best-predict-35909-default-rtdb.asia-southeast1.firebasedatabase.app/"

def run_ai():
    print("🤖 AI কাজ শুরু করছে... আজকের সবচেয়ে নিরাপদ ১৫টি ম্যাচ খুঁজছে...")
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        # প্রম্পটটি ১৫টি সবচেয়ে নিরাপদ (Safest) ম্যাচের জন্য সাজানো হয়েছে
        prompt = """
        ACT AS AN ELITE FOOTBALL ANALYST.
        1. Research all top-tier football matches happening TODAY and TOMORROW globally.
        2. Select exactly 15 matches that have the HIGHEST win probability (the safest 15 picks).
        3. All selections must have a winning chance of 88% or higher.
        4. For each match, provide REAL data: league, time, homeTeam, awayTeam, homeLogo, awayLogo, mainPick, prediction, odds, doubleChance, btts, correctScore, totalGoals, team1Goals, team2Goals, aiAnalysis, winningChance, confidenceLevel.
        5. confidenceLevel should be 'High Confidence' for all.
        6. Return ONLY a raw JSON object with keys "today" and "tomorrow". 
        
        Structure:
        {
          "today": [...15 safest matches if available, or split between today/tomorrow...],
          "tomorrow": []
        }
        """

        # Gemini 1.5 Flash (লেটেস্ট) ব্যবহার করে ডেটা নেওয়া
        response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
        ai_text = response.text.strip()
        
        # JSON অংশটুকু ছেঁকে নেওয়া
        start = ai_text.find('{')
        end = ai_text.lastIndexOf('}') + 1
        json_data = json.loads(ai_text[start:end])
        
        total_matches = len(json_data.get("today", [])) + len(json_data.get("tomorrow", []))
        
        # Firebase Singapore Server এ আপলোড
        res = requests.put(f"{FIREBASE_URL}/matches.json", json=json_data)
        
        if res.status_code == 200:
            print(f"✅ সফল! আজকের সবচেয়ে নিরাপদ {total_matches} টি ম্যাচ আপলোড হয়েছে।")
        else:
            print(f"❌ Firebase error: {res.text}")
            
    except Exception as e:
        print(f"❌ এরর: {e}")

if __name__ == "__main__":
    run_ai()
