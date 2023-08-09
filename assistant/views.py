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
            request.session['messages'] = [
                
            ]
        if request.method == 'POST':
            # get the prompt from the form
            str1= "Here is who I am.'"
            auth= request.POST.get('author')
            bio= request.POST.get('bio')
            mission= request.POST.get('mission')
            temperature = float(request.POST.get('temperature', 0.1))

            prompt="Here is who I am.'"+bio
            request.session['messages'].append({"role": "user", "content": prompt})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=request.session['messages'],
                temperature=temperature,
                max_tokens=1000
            )
            # format the response
            formatted_response = response['choices'][0]['message']['content']
            # append the response to the messages list
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            print(request.session['messages'])
            print("------------------------------------------")

            prompt="I am actually struggling with"+mission
            request.session['messages'].append({"role": "user", "content": prompt})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=request.session['messages'],
                temperature=temperature,
                max_tokens=1000
            )
            # format the response
            formatted_response = response['choices'][0]['message']['content']
            # append the response to the messages list
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            print(request.session['messages'])
            print("------------------------------------------")

            prompt = "Can you be more specific? Can you give me more variety of examples?"
            request.session['messages'].append({"role": "user", "content": prompt})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=request.session['messages'],
                temperature=temperature,
                max_tokens=1000
            )
            # format the response
            formatted_response = response['choices'][0]['message']['content']
            # append the response to the messages list
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            print(request.session['messages'])
            print("------------------------------------------")

            prompt = "Can you put it in a song? Make lyrics to the song which has the title of this or written by this man'"+auth+"'.Also somehow tie christianity and jesus to this. I really want to connect closer to god."
            request.session['messages'].append({"role": "user", "content": prompt})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=request.session['messages'],
                temperature=temperature,
                max_tokens=1000
            )
            # format the response
            formatted_response = response['choices'][0]['message']['content']
            # append the response to the messages list
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            print(request.session['messages'])
            print("------------------------------------------")

            prompt = "please include my bio and what my struggle is into the lyrics"
            request.session['messages'].append({"role": "user", "content": prompt})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=request.session['messages'],
                temperature=temperature,
                max_tokens=1000
            )
            # format the response
            formatted_response = response['choices'][0]['message']['content']
            # append the response to the messages list
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            print(request.session['messages'])
            print("------------------------------------------")

            prompt = "can you make this more modern too?"
            request.session['messages'].append({"role": "user", "content": prompt})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=request.session['messages'],
                temperature=temperature,
                max_tokens=1000
            )
            # format the response
            formatted_response = response['choices'][0]['message']['content']
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            result=formatted_response
            # append the response to the messages list

            request.session.modified = True
            # redirect to the home page
            context = {
                'messages': request.session['messages'],
                'result': result,
                'prompt': '',
                'author' : auth,
                'input_flag' : 1,
                'bio' :bio,
                'temperature': temperature,
            }
            return render(request, 'assistant/home.html', context)
        else:
            # if the request is not a POST request, render the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
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
