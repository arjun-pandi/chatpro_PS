from flask import Flask, render_template, request, jsonify
import pyttsx3
import time

app = Flask(__name__)

speaking_paragraph = ['Benefits of Trees for the Planet\n''Trees are a source of oxygen. They absorb carbon dioxide and help regulate climatic conditions, along with transforming carbon dioxide into oxygen by photosynthesis.  Trees control the atmospheric temperature and improve soil fertility. They are also vital for wildlife to survive and thrive. Further, trees provide an aesthetically pleasing landscape. Since they provide many benefits to living beings, it is important to understand how trees contribute to the planet.\n']

# Function to speak text
def speak(text, gender='male', rate=150, volume=1.0):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)  # Speed of speech (words per minute)
    engine.setProperty('volume', volume)  # Volume level (0.0 to 1.0)

    # Select voice based on gender
    voices = engine.getProperty('voices')
    if gender == 'male':
        engine.setProperty('voice', voices[0].id)  # Male voice
    elif gender == 'female':
        engine.setProperty('voice', voices[1].id)  # Female voice

    engine.say(text)
    engine.runAndWait()

# Global variables to track user information
users = {}
current_user = None
current_question_number = 0
current_category = None
score = 0
wrong_attempts = 0
user_responses = []

# Define listening_questions globally
listening_questions = {
    'Question 1:': {
        'Question': '1. What event are Samantha and Mike discussing?',
        'Options': ['a) Movie night', 'b) Music festival', 'c) Art exhibition', 'd) Sports competition'],
        'Answer': 'b'
    },
    'Question 2:': {
        'Question': '2. When is the event taking place?',
        'Options': ['a) March 20th', 'b) March 25th', 'c) March 30th', 'd) April 5th'],
        'Answer': 'c'
    },
    'Question 3:': {
        'Question': '3. What is the name of the event?',
        'Options': ['a) Sunset Sounds', 'b) City Park Fest', 'c) Downtown Jam', 'd) Urban Beats'],
        'Answer': 'a'
    },
    'Question 4:': {
        'Question': '4. Where is the event happening?',
        'Options': ['a) City Hall', 'b) City Park downtown', 'c) Local theater', 'd) Community center'],
        'Answer': 'b'
    },
    'Question 5:': {
        'Question': '5. Is there an entry fee for the event? If yes, how much is it?',
        'Options': ['a) Free entry', 'b) $5 per person', 'c) $10 per person', 'd) $15 per person'],
        'Answer': 'c'
    },
    'Question 6:': {
        'Question': '6. What time does the event start?',
        'Options': ['a) 12 PM', 'b) 2 PM', 'c) 4 PM', 'd) 6 PM'],
        'Answer': 'c'
    },
    'Question 7:': {
        'Question': '7. Is there a specific dress code for the event?',
        'Options': ['a) Formal attire', 'b) Beachwear', 'c) Casual', 'd) Sportswear'],
        'Answer': 'c'
    },
    'Question 8:': {
        'Question': '8. Who informed Mike about the event?',
        'Options': ['a) Samantha', 'b) David', 'c) Emily', 'd) John'],
        'Answer': 'a'
    },
    'Question 9:': {
        'Question': '9. How did Samantha describe the dress code?',
        'Options': ['a) Elegant', 'b) Casual', 'c) Business attire', 'd) Traditional'],
        'Answer': 'b'
    },
    'Question 10:': {
        'Question': "10. What is Mike's response to Samantha's information about the event?",
        'Options': ['a) Thanks for letting me know!', "b) I'm not interested.", "c) I'll check my schedule.",
                    'd) Is there food available?'],
        'Answer': 'a'
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cody/message', methods=['POST'])
def message():
    global current_user, current_category, current_question_number, score

    user_message = request.json['message']
    response = ""
    buttons = []
    print(user_message)

    if user_message =='listening_skill':
        print('check is on')
        response = "Checking Mic in one and two 🔊"
        buttons = [{'label': '🔊', 'value': 'play_audio'}]
    if user_message == 'listening_skill':
        print('hi- its working')
        response = "You've selected Listening skills. <br> Instructions: Listen to the audio and write down the sentence."
        # Display the speaker button
        buttons = [{'label': '🔊', 'value': 'play_audio'}]

        # Function to play audio
        def speak_conversation():
            speak("Samantha: Hey, Mike! Have you heard about the upcoming event next Saturday?", gender='female')
            time.sleep(1)
            speak("Mike: No, what's happening?", gender='male')
            time.sleep(1)
            speak("Samantha: It's a music festival called 'Sunset Sounds' on March 30th, starting at 4 PM.",
                  gender='female')
            time.sleep(1)
            speak("Mike: Sounds fun! Where is it taking place?", gender='male')
            time.sleep(1)
            speak("Samantha: It's at the City Park downtown.", gender='female')
            time.sleep(1)
            speak("Mike: Cool! Is there an entry fee?", gender='male')
            time.sleep(1)
            speak("Samantha: Yes, it's $10 per person.", gender='female')
            time.sleep(1)
            speak("Mike: Got it. Is there a dress code?", gender='male')
            time.sleep(1)
            speak("Samantha: Yep, it's casual. Just wear something comfy.", gender='female')
            time.sleep(1)
            speak("Mike: Alright, I'll mark my calendar. Thanks for letting me know, Samantha!", gender='male')
            time.sleep(1)
            speak("Samantha: No problem, Mike! It'll be great to see you there!", gender='female')

            pass  # Placeholder

        speak_conversation()  # Call the function to play audio

        # Display listening questions
        listening_questions = {
            'Question 1:': {
                'Question': '1. What event are Samantha and Mike discussing?',
                'Options': ['a) Movie night', 'b) Music festival', 'c) Art exhibition', 'd) Sports competition'],
                'Answer': 'b'
            },
            'Question 2:': {
                'Question': '2. When is the event taking place?',
                'Options': ['a) March 20th', 'b) March 25th', 'c) March 30th', 'd) April 5th'],
                'Answer': 'c'
            },
            'Question 3:': {
                'Question': '3. What is the name of the event?',
                'Options': ['a) Sunset Sounds', 'b) City Park Fest', 'c) Downtown Jam', 'd) Urban Beats'],
                'Answer': 'a'
            },
            'Question 4:': {
                'Question': '4. Where is the event happening?',
                'Options': ['a) City Hall', 'b) City Park downtown', 'c) Local theater', 'd) Community center'],
                'Answer': 'b'
            },
            'Question 5:': {
                'Question': '5. Is there an entry fee for the event? If yes, how much is it?',
                'Options': ['a) Free entry', 'b) $5 per person', 'c) $10 per person', 'd) $15 per person'],
                'Answer': 'c'
            },
            'Question 6:': {
                'Question': '6. What time does the event start?',
                'Options': ['a) 12 PM', 'b) 2 PM', 'c) 4 PM', 'd) 6 PM'],
                'Answer': 'c'
            },
            'Question 7:': {
                'Question': '7. Is there a specific dress code for the event?',
                'Options': ['a) Formal attire', 'b) Beachwear', 'c) Casual', 'd) Sportswear'],
                'Answer': 'c'
            },
            'Question 8:': {
                'Question': '8. Who informed Mike about the event?',
                'Options': ['a) Samantha', 'b) David', 'c) Emily', 'd) John'],
                'Answer': 'a'
            },
            'Question 9:': {
                'Question': '9. How did Samantha describe the dress code?',
                'Options': ['a) Elegant', 'b) Casual', 'c) Business attire', 'd) Traditional'],
                'Answer': 'b'
            },
            'Question 10:': {
                'Question': "10. What is Mike's response to Samantha's information about the event?",
                'Options': ['a) Thanks for letting me know!', "b) I'm not interested.", "c) I'll check my schedule.",
                            'd) Is there food available?'],
                'Answer': 'a'
            }
        }

        buttons += [{'label': 'Submit', 'value': 'submit_listening_answers'}]
        print('hi- its working - on 1')
    if current_user is None:
        # If the current user is not set, start the chat by greeting
        response = "Hello! I'm Cody, your grammar quiz bot. Type start to begin the quiz."
        current_user = user_message
        users[current_user] = {'score': 0, 'attempts': 0}
    elif users[current_user]['attempts'] == 0:
        if user_message.lower() == 'start':
            response = "Great! Select the skill you would like to practice:"
            buttons = [
                {'label': 'Listening Skills', 'value': 'listening_skill'},
                {'label': 'Speaking Skills', 'value': 'speaking_skill'},
                {'label': 'Writing Skills', 'value': 'writing_skill'}
            ]
    elif user_message == 'listening_skills':
        print('hi- its working')
        response = "You've selected Listening skills. <br> Instructions: Listen to the audio and write down the sentence."
        # Display the speaker button
        buttons = [{'label': '🔊', 'value': 'play_audio'}]

        # Function to play audio
        def speak_conversation():
            speak("Samantha: Hey, Mike! Have you heard about the upcoming event next Saturday?", gender='female')
            time.sleep(1)
            speak("Mike: No, what's happening?", gender='male')
            time.sleep(1)
            speak("Samantha: It's a music festival called 'Sunset Sounds' on March 30th, starting at 4 PM.",
                  gender='female')
            time.sleep(1)
            speak("Mike: Sounds fun! Where is it taking place?", gender='male')
            time.sleep(1)
            speak("Samantha: It's at the City Park downtown.", gender='female')
            time.sleep(1)
            speak("Mike: Cool! Is there an entry fee?", gender='male')
            time.sleep(1)
            speak("Samantha: Yes, it's $10 per person.", gender='female')
            time.sleep(1)
            speak("Mike: Got it. Is there a dress code?", gender='male')
            time.sleep(1)
            speak("Samantha: Yep, it's casual. Just wear something comfy.", gender='female')
            time.sleep(1)
            speak("Mike: Alright, I'll mark my calendar. Thanks for letting me know, Samantha!", gender='male')
            time.sleep(1)
            speak("Samantha: No problem, Mike! It'll be great to see you there!", gender='female')

            pass  # Placeholder

        speak_conversation()  # Call the function to play audio

        # Display listening questions
        listening_questions = {
            'Question 1:': {
                'Question': '1. What event are Samantha and Mike discussing?',
                'Options': ['a) Movie night', 'b) Music festival', 'c) Art exhibition', 'd) Sports competition'],
                'Answer': 'b'
            },
            'Question 2:': {
                'Question': '2. When is the event taking place?',
                'Options': ['a) March 20th', 'b) March 25th', 'c) March 30th', 'd) April 5th'],
                'Answer': 'c'
            },
            'Question 3:': {
                'Question': '3. What is the name of the event?',
                'Options': ['a) Sunset Sounds', 'b) City Park Fest', 'c) Downtown Jam', 'd) Urban Beats'],
                'Answer': 'a'
            },
            'Question 4:': {
                'Question': '4. Where is the event happening?',
                'Options': ['a) City Hall', 'b) City Park downtown', 'c) Local theater', 'd) Community center'],
                'Answer': 'b'
            },
            'Question 5:': {
                'Question': '5. Is there an entry fee for the event? If yes, how much is it?',
                'Options': ['a) Free entry', 'b) $5 per person', 'c) $10 per person', 'd) $15 per person'],
                'Answer': 'c'
            },
            'Question 6:': {
                'Question': '6. What time does the event start?',
                'Options': ['a) 12 PM', 'b) 2 PM', 'c) 4 PM', 'd) 6 PM'],
                'Answer': 'c'
            },
            'Question 7:': {
                'Question': '7. Is there a specific dress code for the event?',
                'Options': ['a) Formal attire', 'b) Beachwear', 'c) Casual', 'd) Sportswear'],
                'Answer': 'c'
            },
            'Question 8:': {
                'Question': '8. Who informed Mike about the event?',
                'Options': ['a) Samantha', 'b) David', 'c) Emily', 'd) John'],
                'Answer': 'a'
            },
            'Question 9:': {
                'Question': '9. How did Samantha describe the dress code?',
                'Options': ['a) Elegant', 'b) Casual', 'c) Business attire', 'd) Traditional'],
                'Answer': 'b'
            },
            'Question 10:': {
                'Question': "10. What is Mike's response to Samantha's information about the event?",
                'Options': ['a) Thanks for letting me know!', "b) I'm not interested.", "c) I'll check my schedule.",
                            'd) Is there food available?'],
                'Answer': 'a'
            }
        }

        buttons += [{'label': 'Submit', 'value': 'submit_listening_answers'}]


    elif user_message == 'submit_listening_answers':
        # Logic to check answers and calculate score goes here
        def check_listening_answers(user_responses):
            # Assuming user_responses is a list of user's answers
            correct_answers = ['Option 1', 'Option 2', 'Option 3', 'Option 4']  # Example correct answers
            score = 0
            for user_answer, correct_answer in zip(user_responses, correct_answers):
                if user_answer == correct_answer:
                    score += 1
            return score

        # Call the function to check answers and update the score
        score = check_listening_answers(user_responses)

    # After calculating score
        total_questions = 10
        response += f"\nYour score is: {score}/{total_questions}\nDo you want to try again or exit?"
        buttons += [
            {'label': 'Try Again', 'value': 'try_again'},
            {'label': 'Exit', 'value': 'exit'}
        ]

    return jsonify({'message': response, 'buttons': buttons})

# Route for handling user's responses
@app.route('/response', methods=['POST'])
def response():
    global current_user, current_category, current_question_number, score

    data = request.json
    user_response = data['response']
    correct_answer = listening_questions[current_category][current_question_number]['Answer']

    # Check user's response and update score
    if user_response == correct_answer:
        score += 1

    current_question_number += 1

    # Check if all questions have been answered
    if current_question_number < len(listening_questions[current_category]):
        # Ask the next question
        question_data = listening_questions[current_category][current_question_number]
        response = f"{question_data['Question']}"
        buttons = [
            {'label': 'Option A', 'value': 'A'},
            {'label': 'Option B', 'value': 'B'},
            {'label': 'Option C', 'value': 'C'},
            {'label': 'Option D', 'value': 'D'}
        ]
    else:
        # Quiz ended, display score
        response = f"Quiz ended. Your score is {score}/{len(listening_questions[current_category])}."
        current_user = None
        current_category = None
        score = 0

    return jsonify({'message': response, 'buttons': buttons})

if __name__ == '__main__':
    app.run(debug=True)
