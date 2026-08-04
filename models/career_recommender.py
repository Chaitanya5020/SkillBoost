import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Load the dataset
df = pd.read_csv('Complete_Careers_and_Skills.csv')
df['Skills'] = df['Skills'].str.lower()  # Normalize the skills to lowercase

# Initialize vectorizer
vectorizer = CountVectorizer()
skills_matrix = vectorizer.fit_transform(df['Skills'])

def recommend_careers(input_skills, top_n=5):
    """
    Recommend careers based on input skills.
    
    Args:
        input_skills (str): A comma-separated string of user skills.
        top_n (int): Number of top recommendations.
    
    Returns:
        list: List of top recommended careers.
    """
    input_skills = input_skills.lower()  # Convert input to lowercase
    input_vector = vectorizer.transform([input_skills])  # Vectorize input

    # Compute similarity scores
    similarity_scores = cosine_similarity(input_vector, skills_matrix).flatten()

    # Add similarity scores and sort
    df['Similarity'] = similarity_scores
    recommendations = df.sort_values(by='Similarity', ascending=False).head(top_n)

    return recommendations[['Career']].to_dict(orient='records')  # Convert to list of dictionaries
