# importing render and redirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
import openai
import os
from dotenv import load_dotenv

load_dotenv()
# loading the API key from the .env file
openai.api_key = os.environ.get("OPENAI_API_KEY")
# this is the home view for handling home page logic

def upload(request):
    if request.method == 'POST':
        upload_file=request.FILES['file']
        filename = request.POST.get('filename')
        if not os.path.exists('upload/'):
            os.mkdir('upload/')

        with open('upload/' + filename, 'wb+') as destination:
            for chunk in upload_file.chunks():
                destination.write(chunk)
        with open('upload/' + filename, "rb") as audio_file:
            script = openai.Audio.transcribe(
                file = audio_file,
                model = "whisper-1",
                response_format="text",
                language="en"
            )
        print(script)
        return HttpResponse(script)
    return HttpResponse("Failed")

def home(request):
    try:
        # if the session does not have a messages key, create one
        if 'messages' not in request.session:
            request.session['messages'] = [{
                "role":"system",
                "content":"You're an a AI assistant that replies to all my questions in markdown format."
            }]
        if request.method == 'POST':
            # get the prompt from the form
            question= request.POST.get('question')
            print("xxx", question)
            temperature = float(request.POST.get('temperature', 0.1))

            request.session['messages'].append({"role": "user", "content": question})
            
            response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo", 
                messages = request.session['messages'], 
                temperature=0.1,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                )
            # format the response
            reply = response['choices'][0]['message']['content']
            # append the response to the messages list
            request.session['messages'].append({"role": "assistant", "content": reply})
            print(request.session['messages'])
            print("------------------------------------------")

            request.session.modified = True
            # redirect to the home page
            context = {
                'messages': request.session['messages'],
                'result': reply,
                'question' : question,
                'input_flag' : 1,
                'temperature': temperature,
            }
            return render(request, 'assistant/home.html', context)
        else:
            # if the request is not a POST request, render the home page
            context = {
                'messages': request.session['messages'],
                'temperature': 0.1,
            }
            return render(request, 'assistant/home.html', context)
    except Exception as e:
        print(e)
        # if there is an error, redirect to the error handler
        return redirect('error_handler')


def new_chat(request):
    # clear the messages list
    request.session['first_input'] = 0
    request.session.pop('messages', None)
    return redirect('home')


# this is the view for handling errors
def error_handler(request):
    return render(request, 'assistant/404.html')
