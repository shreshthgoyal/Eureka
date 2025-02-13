import os
import pandas as pd
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import tensorflow_hub as hub
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

labels = ["Finance", "Education", "Entertainment", "Fitness", "HR", "Design", "Security", "Legal"]

training_texts = [
    "Stock market trends and financial news",
    "Latest technical research and methods",
    "What is Woodpecker?",
    "Human resources policies and employee management",
    "Graphic design trends and tutorials",
    "Cybersecurity threats and prevention",
    "Legal case studies and law news"
]
training_labels = ["Finance", "Technical", "FAQ", "HR", "Design", "Security", "Legal"]

training_embeddings = embed(training_texts)

svm_clf = make_pipeline(StandardScaler(), SVC(kernel='linear', probability=True))
svm_clf.fit(training_embeddings, training_labels)

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text() if page.extract_text() else ""
            text += " " + page_text
    return text.strip()

def extract_text_from_csv(file_path):
    df = pd.read_csv(file_path, usecols=[1])
    return " ".join(df.iloc[:, 0].astype(str))

def extract_keywords_tfidf(text, num_keywords=5):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    dense = tfidf_matrix.todense()
    dense_list = dense.tolist()
    tfidf_scores = dense_list[0]
    
    keyword_indices = np.argsort(tfidf_scores)[-num_keywords:][::-1]
    keywords = [feature_names[idx] for idx in keyword_indices]
    return keywords

def classify_text(text):
    text_embedding = embed([text])
    prediction = svm_clf.predict(text_embedding)
    return prediction[0]

def summarize_and_interpret(data_folder):
    results = []
    for filename in os.listdir(data_folder):
        file_path = os.path.join(data_folder, filename)
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif filename.endswith('.csv'):
            text = extract_text_from_csv(file_path)
        else:
            continue

        keywords = extract_keywords_tfidf(text)
        classification = classify_text(text)

        results.append({
            'filename': os.path.join(data_folder, filename),
            'keywords': keywords,
            'classification': classification
        })
    
    return results

data_folder = 'data/'
documentInfo = summaries_and_interpretations = summarize_and_interpret(data_folder)