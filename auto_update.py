from google import genai
import requests
import json
import os

# GitHub Secrets থেকে ডাটাগুলো নেবে
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FIREBASE_URL = "https://best-predict-35909-default-rtdb.asia-southeast1.firebasedatabase.app/"

def run_ai():
    print("🤖 AI কাজ শুরু করছে... লেটেস্ট ফুটবল ম্যাচ এনালাইসিস করছে...")
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = """
        Research top 15 football matches for today and tomorrow. 
        Return ONLY a raw JSON object starting with { and ending with }.
        Keys: today, tomorrow.
        Fields: league, time, homeTeam, awayTeam, homeLogo, awayLogo, mainPick, prediction, odds, doubleChance, btts, correctScore, totalGoals, team1Goals, team2Goals, aiAnalysis, winningChance, confidenceLevel.
        isFinished: false, isWon: false.
        """

        # Gemini 3.5 Flash লেটেস্ট মডেল ব্যবহার করছি
        response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
        ai_text = response.text.strip()
        
        json_start = ai_text.find('{')
        json_end = ai_text.rfind('}') + 1
        json_data = json.loads(ai_text[json_start:json_end])
        
        # Firebase Singapore Server এ আপলোড
        res = requests.put(f"{FIREBASE_URL}/matches.json", json=json_data)
        if res.status_code == 200:
            print("✅ সাকসেস! অ্যাপের ডেটা আপডেট হয়েছে।")
        else:
            print(f"❌ Firebase Error: {res.text}")
            
    except Exception as e:
        print(f"❌ এরর: {e}")

if __name__ == "__main__":
    run_ai()
