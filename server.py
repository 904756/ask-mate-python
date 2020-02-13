import data_manager, sorting_functions

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/list')
def main_page():
    return render_template('index.html', table_elements = data_manager.sort_questions())

@app.route('/question/<question_id>', methods=["GET"])
def show_questions(question_id):
    return render_template('question.html', question_elements= sorting_functions.title_and_message(question_id), answer_elements= sorting_functions.get_answer(question_id), question_id=question_id )


@app.route('/question/<question_id>/new-answer', methods=["GET", "POST"])
def new_answers(question_id):
    if request.method == 'POST':
        message = request.form['message']
        data_manager.write_to_answers("sample_data/answer.csv", question_id, message)
        return redirect(url_for('show_questions', question_id=question_id))
    return render_template('new_answer.html', question_id=question_id)

@app.route("/question/<question_id>/delete", methods=["GET", "POST","DELETE"])
def remove_a_question(question_id):
    if request.method == 'GET':
        data_manager.remove_question(question_id)
        data_manager.remove_answer(question_id)
    return redirect(url_for('main_page'))


@app.route('/add_question', methods=["GET", "POST"])
def add_question():
    if request.method == 'POST':
        message = request.form['message']
        title = request.form['title']
        question_id = data_manager.generate_id('sample_data/question.csv')
        data_manager.write_to_questions("sample_data/question.csv", message, title)
        return redirect(url_for('show_questions', question_id=question_id))
    return render_template('add-question.html')


if __name__ == '__main__':
    app.run(
        debug=True
    )