import os
import pandas as pd
import PyPDF2
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import spacy
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
    "Latest educational research and teaching methods",
    "Movie reviews and entertainment news",
    "Workout routines and fitness tips",
    "Human resources policies and employee management",
    "Graphic design trends and tutorials",
    "Cybersecurity threats and prevention",
    "Legal case studies and law news"
]
training_labels = ["Finance", "Education", "Entertainment", "Fitness", "HR", "Design", "Security", "Legal"]

training_embeddings = embed(training_texts)

# Train an SVM classifier
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
    df = pd.read_csv(file_path, usecols=[2])
    return " ".join(df.iloc[:, 0].astype(str))

def summarize_text(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 2)  # Summarize to 2 sentences
    return " ".join([str(sentence) for sentence in summary])

def extract_keywords_tfidf(text, num_keywords=5):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    dense = tfidf_matrix.todense()
    dense_list = dense.tolist()
    tfidf_scores = dense_list[0]
    
    # Use numpy to handle sorting and indexing
    keyword_indices = np.argsort(tfidf_scores)[-num_keywords:][::-1]
    keywords = [feature_names[idx] for idx in keyword_indices]
    return keywords

def classify_text(text):
    # Convert text to embeddings
    text_embedding = embed([text])
    # Use the trained SVM classifier to classify the text
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

        summary = summarize_text(text)
        keywords = extract_keywords_tfidf(text)
        classification = classify_text(text)

        results.append({
            'filename': os.path.join(data_folder, filename),
            'summary': summary,
            'keywords': keywords,
            'classification': classification
        })
    
    return results

data_folder = 'data/'
documentInfo = summaries_and_interpretations = summarize_and_interpret(data_folder)

# Display results
for info in documentInfo:
    print(f"Filename: {info['filename']}")
    print(f"Summary: {info['summary']}")
    print(f"Keywords: {info['keywords']}")
    print(f"Classification: {info['classification']}")
    print("-" * 80)
