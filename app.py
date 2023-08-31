from flask import Flask, request, render_template, flash, jsonify, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, Question, satisfaction_survey


"""
Varible respones: Where we store the users answers to survey questions
"""
responses = []

"""
An instance of the class Survey called statisfaction_survey. Used to test Survey functionality. Directions specifically state for now to use satisfication_survey.
"""
satisfaction_survey = Survey(
    "Customer Satisfaction Survey",
    "Please fill out a survey about your experience with us.",
    [
        Question("Have you shopped here before?"),
        Question("Did someone else shop with you today?"),
        Question("On average, how much do you spend a month on frisbees?",
                 ["Less than $10,000", "$10,000 or more"]),
        Question("Are you likely to shop here again?"),
    ])

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def homepage():
    """Creates home page, greeting User with the title of the survey they'll be taking and the corresponding instructions."""
    """Base.html is parent template but, start_survey.html is what we're using here to extend base.html"""
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('start_survey.html', title=title, instructions=instructions)
   

@app.route('/questions/<int:num>')
def question(num):
    """Displays survey questions with corresponding choices. Must put indicies of array for now. 0= question 1 and so forth"""
    """Due to the steps of assignment at the moment this is route is only accessbile by user inputting corresponding question numbers into route varible"""
    question_displayed = satisfaction_survey.questions[num].question
    choices = question_displayed.choices
    return render_template('questions.html', num=num, question_displayed=question_displayed, choices=choices)

@app.route('/questions', methods=['POST'])
def answer():
    """When an individual answer is submitted the answer is then appended to the responses list"""
    """Buggy and not working properly. next_question = len(responses) in conjuction with how POST request work I believe is creating the issue."""
    answer = request.form["choice"]
    responses.append(answer)
    next_question = len(responses)
    return redirect(f"/questions/{next_question}")

"""
For Kwame:
    The reason why I chose to use len is because it was a spur of the moment and I liked the idea. \
        - If I answer a question then the length of responses array will be equal to one more than the current index of the current question
        - Then I can just redirect to the next question by using the length of the responses array
            Ex:
                User is on question 1 ([0] in list of questions)
                len(respones) = 0
                "User answers question"
                "Users answer is pushed respones Array"
                len(respones) = 1
                redirect(f"/questions/{next_question (1)}) 
                
    1. Works the first time but, after saved responses become longer than length of total amount of question accessible then an index error will be produced with the redirect. (Which I expected to occur)
        - What I didn't expect to occur is that if I refresh the page the previous survey answers will still be stored by responses
    2. I didn't get a chance to research POST methods but, I recall POST storing variable information UNTIL session is closed. 
        Questions: 
            - Do I have the right idea regarding post requests?
            - How could I clear the responses variable after a certain amount of answers? (I was thinking what if I used a dictionary so that if answers to previously answered questions were changed then I can just change the value of the question numbers key)

            Keeping in mind that according to the assignment directions the USER must answer questions in chronological order. Won't be able to use url to skip beyond unanswered questions (Will be implemented way later)
                - I was thinking of using some logic like this....
                    return redirect(f"/question/{next_question}") if len(respones) < len(satisfaction_survey.questions) else None

"""
    

