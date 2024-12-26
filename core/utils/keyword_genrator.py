from sklearn.feature_extraction.text import TfidfVectorizer

def generate_keywords(description):
    vectorizer = TfidfVectorizer(max_features=5, stop_words='english')
    vectorizer.fit([description])  
    return ', '.join(vectorizer.get_feature_names_out())