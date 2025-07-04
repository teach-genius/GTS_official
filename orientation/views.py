import os
import json
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')
chat_session = model.start_chat()

INITIAL_PROMPT = (
    "Tu es GTS, un expert en orientation scolaire et professionnelle. Ta mission est d'aider chaque personne, quel que soit son niveau (collégien, lycéen, étudiant, adulte en reconversion), à trouver une voie adaptée à ses compétences, centres d'intérêt et objectifs."
    "Sois structuré, précis, méthodique et bienveillant. Pose une seule question à la fois pour mieux cerner le profil. Réponds de façon claire, concise, sans longs paragraphes. Ne donne pas trop d'informations d’un coup. Pose des questions pertinentes pour avancer pas à pas."
)

@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "").strip()

            if not message:
                return JsonResponse({"error": "Message vide"}, status=400)

            # Injecter le prompt initial une seule fois
            if not chat_session.history:
                full_message = f"{INITIAL_PROMPT}\n\n{message}"
            else:
                full_message = message

            response = chat_session.send_message(full_message)
            return JsonResponse({"reply": response.text})

        except Exception as e:
            print("❌ Erreur Gemini Flash :", e)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)
