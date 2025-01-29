from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def dashboard_view(request):
    user = request.user  # 현재 로그인한 사용자
    username = user.username  # OAuth 연결 여부와 상관없이 사용자 이름을 사용
    return render(request, 'closet/dashboard.html', {'username': username})

@login_required
def closet_start_view(request):
    return render(request, 'closet_start.html')

@login_required
def closet_history_view(request):
    return render(request, 'closet_history.html')




from google import genai
from google.genai import types
import base64

def generate():
  client = genai.Client(
      vertexai=True,
      project="sonic-progress-449301-b7",
      location="us-central1"
  )


  model = "gemini-2.0-flash-exp"
  contents = [
    types.Content(
      role="user",
      parts=[
        types.Part.from_text("""기온이 20도정도 되는 날씨의 옷""")
      ]
    ),
   ]
  tools = [
    types.Tool(google_search=types.GoogleSearch())
  ]
  generate_content_config = types.GenerateContentConfig(
    temperature = 1,
    top_p = 0.95,
    max_output_tokens = 8192,
    response_modalities = ["TEXT"],
    safety_settings = [types.SafetySetting(
      category="HARM_CATEGORY_HATE_SPEECH",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_DANGEROUS_CONTENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_HARASSMENT",
      threshold="OFF"
    )],
    tools = tools,
  )

  for chunk in client.models.generate_content_stream(
    model = model,
    contents = contents,
    config = generate_content_config,
    ):
    if not chunk.candidates or not chunk.candidates[0].content.parts:
        continue
    print(chunk.text, end="")

generate()