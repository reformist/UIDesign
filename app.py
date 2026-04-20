from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import json

app = Flask(__name__)

with open('data.json', 'r') as file:
    poker_data = json.load(file)

# We assume 1 user
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
        return redirect(url_for('quiz', question_id=1))
    return render_template('learn.html', lesson=lesson_info, lesson_id=lesson_id)

@app.route('/record_lesson', methods=['POST'])
def record_lesson():
    """
    Records user activity on a lesson page.
    Expects form fields: lesson_id, action, detail (optional)

    action values:
      'visit'         — user landed on the page
      'view_position' — user clicked a table seat (detail = position id, e.g. 'btn')
      'view_tier'     — user expanded a hand strength tier (detail = tier id, e.g. 'premium')
      'complete'      — user clicked Continue / Take the Quiz
    """
    entry = {
        "lesson_id": request.form.get("lesson_id"),
        "action":    request.form.get("action"),
        "detail":    request.form.get("detail", None),
        "timestamp": datetime.now().isoformat()
    }
    user_state["learning_selections"].append(entry)
    return jsonify({"status": "ok"})

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

if __name__ == '__main__':
    app.run(debug=True)