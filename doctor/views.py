from django.shortcuts import render, get_object_or_404
from .models import DoctorProfile, PatientEducation
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import google.generativeai as genai
import pyttsx3
from gtts import gTTS
import os
from googletrans import Translator
import vlc
import speech_recognition as sr
import subprocess
from django.shortcuts import render, redirect
from .models import PatientProfile
from .forms import PatientProfileForm

from social_django.models import UserSocialAuth

from django.shortcuts import redirect
from django.shortcuts import render, redirect
from .models import PatientReport
from .forms import PatientReportForm

from django.shortcuts import render, redirect
from .models import UserSocialAuth, PatientReport
from .forms import PatientReportForm
from django.conf import settings
from twilio.rest import Client
import speech_recognition as sr
from googletrans import Translator
import random


def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'pages/sign-in.html')


def doctor_list(request):
    # display doctors according to the time only 
    doctors = DoctorProfile.objects.all()
    if request.method=='POST':
        language_query = request.POST.get('language')
        speciality_query = request.POST.get('speciality')
        if language_query:
            doctors = doctors.filter(doctor_language__icontains=language_query)
        if speciality_query:
            doctors = doctors.filter(doctor_speciality__icontains=speciality_query)
    else:
        dt=request.session.get('doctortype')
        doctors = doctors.filter(doctor_speciality__icontains=dt)

    return render(request, 'doctor/doctor_list.html', {'doctors': doctors})

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, pk=doctor_id)
    # Return doctor details as JSON response
    return JsonResponse({
        'doctor_name': doctor.doctor_name,
        'doctor_phone_number': doctor.doctor_phone_number,
        'doctor_timings': doctor.doctor_timings,
        'doctor_bio': doctor.doctor_bio,
        'doctor_room_id': doctor.doctor_room_id,
    })


def video_call_with_doctor(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, pk=doctor_id)
    return render(request, 'doctor/video_call_with_doctor.html', {'doctor': doctor})


def educational_content(request):
    # Retrieve all instances of PatientEducation from the database
    educational_topics = PatientEducation.objects.all()

    # Extract video IDs from the URLs and add them to the context
    video_ids = []
    for topic in educational_topics:
        video_url = topic.url
        video_id = None
        
        # Check if the video URL contains 'v='
        if 'v=' in video_url:
            # Split the URL at 'v=' and take the second part
            video_id = video_url.split('v=')[1]
        
        video_ids.append(video_id)
    print(video_ids)
    context = {
        'educational_topics': educational_topics,
        'video_ids': video_ids,  # Pass the list of video IDs to the template
    }

    return render(request, 'patient/education.html', context)
#Chat with AI Doctor

def chat_with_ai(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        response = get_ai_response('"'+user_input+'"'+"reply in 100 words at max in same language as previous input")
        
        # Read out the response using pyttsx3
        print(response)

        return render(request, 'doctor/ai.html', {'user_input': user_input, 'response': response})
    return render(request, 'doctor/ai.html', {})

def get_ai_response(user_input):
   

    model =model = genai.GenerativeModel('gemini-pro')
     
    context = "you are an multilingual ai doctor who suggests patients and consults them about their problems regarding health "
    message = f"{context} {user_input}"
    response = model.generate_content(message)
    answer = response.text
    print(f'hi{answer}')
    return response.text 





def check_patient_profile(request):
    try:
        user_social_auth = UserSocialAuth.objects.filter(user=request.user).first()
        if user_social_auth:
            profile = PatientProfile.objects.filter(user=user_social_auth).first()
            if profile:
                return redirect('doctor_list')
        return redirect('patient_profile')
    except AttributeError:
        return redirect('login')  # Redirect to login if user is not authenticated

def patient_profile(request):
    try:
        user_social_auth = UserSocialAuth.objects.filter(user=request.user).first()
        if not user_social_auth:
            return redirect('login')  # Redirect to login if user has no associated social auth

        if request.method == 'POST':
            form = PatientProfileForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = user_social_auth
                profile.save()
                return redirect('doctor_list')
        else:
            form = PatientProfileForm()
        
        return render(request, 'patient/patient_profile_form.html', {'form': form})
    except UserSocialAuth.DoesNotExist:
        return redirect('login')  # Redirect to login if user is not authenticated


def fill_patient_report(request):
    if request.method == 'POST':
        form = PatientReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user.social_auth.get(provider='provider_name')  # Assuming 'provider_name' is the name of the provider used for authentication
            report.save()
            return redirect('doctor_dashboard')  # Redirect to doctor dashboard or any other appropriate page
    else:
        form = PatientReportForm()
    
    return render(request, 'patient_report.html', {'form': form})




def patient_list(request):
    # Retrieve the list of users
    patients = UserSocialAuth.objects.all()
    return render(request, 'patient/patient_list.html', {'patients': patients})





def fill_report(request):
    if request.method == 'POST':
        form = PatientReportForm(request.POST)
        report = form.save(commit=False)
        report.save()
        precaution = form.cleaned_data['precaution']
        patient_name = f"{form.cleaned_data['name']} {form.cleaned_data['last_name']}"
        disease = form.cleaned_data['disease']
        medication = form.cleaned_data['medication']
        phoneno=form.cleaned_data['phone_number']
        # Call the function to send the report via SMS
        send_report_via_sms(phoneno,precaution, patient_name, disease, medication)
        # Send the report via SMS
        return redirect('chat_with_ai')  # Redirect to success page
    else:
        form = PatientReportForm()
    
    return render(request, 'patient/patient_report.html', {'form': form})

def handle_recorded_file(filepath):
    recognizer = sr.Recognizer()

    # Load Google Translate API
    translator = Translator()

    # Load Hindi audio file (replace 'hindi_audio.wav' with your actual file)
    with sr.AudioFile(filepath) as source:
        audio_data = recognizer.record(source)

    # Recognize speech from Hindi audio
    try:
        hindi_text = recognizer.recognize_google(audio_data, language='hi-IN')
        print("Hindi Text:", hindi_text)

        # Translate Hindi text to English
        english_translation = translator.translate(hindi_text, src='hi', dest='en').text
        print("English Translation:", english_translation)

        

        model =model = genai.GenerativeModel('gemini-pro')
        
        message = "You just need to tell what type of doctur to consult only one word ,"+ english_translation+",select one from phscian,pediatrican, neurologist,nephrologist,dermatologist and gynaclologist"
        # message = f"{context} {english_translation}"
        response = model.generate_content(message)
        answer = response.text
        print(f'hi{answer}')
        return [response.text ,hindi_text,english_translation]

    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Speech Recognition service; {0}".format(e))
    except Exception as e:
        print("Translation Error:", e)

    
def recorded_audio(request):
    if request.method == 'POST':
        # Execute the provided audio recording script
        subprocess.run(['python', 'C:\\hack\\rural\\record.py'])
        
        x=handle_recorded_file("C:\\hack\\rural\\sounds\\output.wav")
        request.session['doctortype'] = x[0][0:3]
       
        return render(request, 'recording.html', {'result': x[0],'hindi':x[1],'english':x[2]})
        

    return render(request, 'recording.html', {'result': ""})



def send_report_via_sms(phoneno,precaution, patient_name, diagnosis,medication):
    # Twilio credentials
    try:
        
        # Initialize Twilio client
        client = Client(account_sid, auth_token)

        # Compose the message body
        message_body = f"Patient Name: {patient_name}\nDiagnosis: {diagnosis}\nMedication: {medication}\nPrecaution:{precaution}"


        # Send the report via SMS
        

        # Print the message SID for reference
        print("Message SID:", message.sid)
    except:
        return 0


def videocall(request):
    return render(request, 'videocall.html', {'name': "rahul" + " " + "jagtap"})

def join_room(request):
    roomID=random.randrange(0,1000)
    roomID=str(roomID)
    return redirect("/meeting?roomID=" + roomID)
    