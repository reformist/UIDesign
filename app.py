from flask import Flask, render_template, request, jsonify, redirect, url_for
import json

app = Flask(__name__)

with open('data.json', 'r') as file:
    poker_data = json.load(file)

# we assume 1 user
user_state = {
    "quiz_answers": {},
    "learning_selections": []
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/learn/<int:lesson_id>')
def learn(lesson_id):
    lesson_info = poker_data['lessons'].get(str(lesson_id))
    
    if not lesson_info:
        #move to quiz when lessons end
        return redirect(url_for('quiz', question_id=1))
        
    return render_template('learn.html', lesson=lesson_info, lesson_id=lesson_id)

@app.route('/quiz/<int:question_id>')
def quiz(question_id):
    question_info = poker_data['quiz'].get(str(question_id))
    
    if not question_info:
        return redirect(url_for('result'))
        
    return render_template('quiz.html', question=question_info, question_id=question_id)

@app.route('/quiz/result')
def result():
    score = 0 
    return render_template('result.html', score=score, answers=user_state['quiz_answers'])

# may need to add some more routes

if __name__ == '__main__':
    app.run(debug=True)