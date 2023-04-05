from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"
user_answer: str
user_answer = ""


class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.q_next = quiz_brain
        self.score = 0
        self.limiter = 0
        self.window = Tk()
        self.window.title('Quizzler')
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.scores = Label(text="Score: 0", fg="white", bg=THEME_COLOR)
        self.scores.grid(column=1, row=0)

        self.canvas = Canvas()
        self.canvas.config(width=300, height=250, bg='white')
        self.question = self.canvas.create_text(150, 125,
                                                width=280,
                                                text="Question",
                                                font=('Ariel', 20, 'italic'),
                                                fill=THEME_COLOR)
        self.canvas.grid(columnspan=2, column=0, row=1, pady=30)

        false_image = PhotoImage(file="images/false.png")
        true_image = PhotoImage(file="images/true.png")

        self.true_button = Button(image=true_image, highlightthickness=0, bg=THEME_COLOR, command=self.answer_true)
        self.true_button.grid(column=0, row=2)
        self.false_button = Button(image=false_image, highlightthickness=0, bg=THEME_COLOR, command=self.answer_false)
        self.false_button.grid(column=1, row=2)
        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        n_quiz = self.q_next.next_question()
        self.canvas.itemconfig(self.question, text=n_quiz)

    def answer_true(self):   
        self.limiter += 1
        if self.limiter <= len(self.q_next.question_list):
            if self.q_next.check_answer('True'):
                self.score += 1
                self.canvas.config(width=300, height=250, bg='green')
                self.scores.config(text=f"Score: {self.score}", fg="white", bg=THEME_COLOR)

            else:
                self.canvas.config(width=300, height=250, bg='red')
        else:
            self.true_button.config(state="disabled")
        self.window.after(1000, self.find_exception)

    def answer_false(self):
        self.limiter += 1
        if self.limiter <= len(self.q_next.question_list):
            if self.q_next.check_answer('False'):
                self.score += 1
                self.canvas.config(width=300, height=250, bg='green')
                self.scores.config(text=f"Score: {self.score}", fg="white", bg=THEME_COLOR)

            else:
                self.canvas.config(width=300, height=250, bg='red')

        else:
            self.false_button.config(state="disabled")
        self.window.after(1000, self.find_exception)

    def find_exception(self):
        try:
            self.get_next_question()
        except IndexError:
            self.canvas.config(width=300, height=250, bg='blue')
            self.canvas.itemconfig(self.question, fil="white")
            self.canvas.itemconfig(self.question, font=('Ariel', 20, 'bold'))
            self.canvas.itemconfig(self.question,
                                   text=f"Your total score is: {self.score}/{len(self.q_next.question_list)}")
        else:
            self.canvas.config(width=300, height=250, bg='white')

    def update_score(self) -> int:
        score = self.q_next.check_score()
        return score
