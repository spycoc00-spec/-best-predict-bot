   from google import genai
   import requests
   import json
   import os

   # GitHub Secrets থেকে ডাটাগুলো নেবে
   GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
   FIREBASE_URL = "https://best-predict-35909-default-rtdb.asia-southeast1.firebasedatabase.app/"

   def run_ai():
       print("🤖 AI কাজ শুরু করছে... লেটেস্ট ফুটবল ম্যাচ এনালাইসিস করছে...")
       client = genai.Client(api_key=GEMINI_API_KEY)
       
       prompt = """
       Research top 15 football matches for today and tomorrow. 
       Give me 5 Safe, 5 Medium, 5 Risk matches.
       Return ONLY raw JSON starting with { and ending with }.
       Keys: today, tomorrow.
       Fields: league, time, homeTeam, awayTeam, homeLogo, awayLogo, mainPick, prediction, odds, doubleChance, btts, correctScore, totalGoals, team1Goals, team2Goals, aiAnalysis, winningChance, confidenceLevel.
       Set isFinished: false, isWon: false.
       """

       try:
           # Gemini 3.5 Flash লেটেস্ট মডেল ব্যবহার করছি
           response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
           ai_text = response.text.strip()
           
           json_start = ai_text.find('{')
           json_end = ai_text.rfind('}') + 1
           json_data = json.loads(ai_text[json_start:json_end])
           
           requests.put(f"{FIREBASE_URL}/matches.json", json=json_data)
           print("✅ সাকসেস! অ্যাপের ডেটা আপডেট হয়েছে।")
       except Exception as e:
           print(f"❌ এরর: {e}")

   if __name__ == "__main__":
       run_ai()
   
