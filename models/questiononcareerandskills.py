import google.generativeai as ai
import pandas as pd

class CareerQuestionGenerator:
    def __init__(self, api_key, dataset_path):
        # API Key and Dataset path
        self.api_key = api_key
        self.dataset_path = dataset_path
        
        # Load dataset
        self.df = pd.read_csv(dataset_path)
        
        # Normalize the skills to lowercase
        self.df['Skills'] = self.df['Skills'].str.lower()
        
        # Configure the API
        ai.configure(api_key=self.api_key)
        
        # Create a new model
        self.model = ai.GenerativeModel("gemini-pro")
        self.chat = self.model.start_chat()

    def get_skills_for_career(self, career):
        # Find the row where the career matches
        career_row = self.df[self.df['Career'] == career]
        
        if not career_row.empty:
            # Assuming 'Skills' is a comma-separated string
            skills = career_row['Skills'].values[0]
            return skills
        else:
            return f"Career {career} not found."
        
    def generate_questions_from_input(self,career):
        skills = self.get_skills_for_career(career)
    # Generate questions
        question_message = (
            "Generate around 10 only Questions with difficulty level:hard and options as A, B, C, D on " 
            + career+" and "+skills+" and" 
            + " and make the options separated by <br> and questions separated by @."
            " Don't give any headings or any other text. Don't give numbering as well."
        )
        question_response = self.chat.send_message(question_message).text
        generated_questions = question_response.split('@')
        
        # Clean and validate questions
        generated_questions = [
            question.strip() for question in generated_questions if question.strip()
        ]
        
        # Generate correct answers
        answer_message = "Generate only answers for the given questions as a comma-separated list."
        answer_response = self.chat.send_message(answer_message).text
        correct_answers = answer_response.split(',')
        correct_answers = [answer.strip() for answer in correct_answers if answer.strip()]
        # Ensure matching length of questions and answers
        if len(generated_questions) != len(correct_answers):
            print("Warning: Mismatch between questions and answers.")
            print(f"Questions: {len(generated_questions)}, Answers: {len(correct_answers)}")
            # Handle mismatch (truncate or pad with placeholders)
            min_length = min(len(generated_questions), len(correct_answers))
            generated_questions = generated_questions[:min_length]
            correct_answers = correct_answers[:min_length]
        
        return generated_questions, correct_answers