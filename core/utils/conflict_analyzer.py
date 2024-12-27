import requests
import time

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/paraphrase-MiniLM-L6-v2"
HEADERS = {"Authorization": f"Bearer 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"}

def get_similarity_score(source_sentence, sentences, retries=3, delay=5, timeout=10):
    payload = {"source_sentence": source_sentence, "sentences": sentences}  # Correct the payload structure

    for _ in range(retries):
        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=timeout)

            if response.status_code == 200:
                # Print the full response to understand the structure
                print("Response JSON:", response.json())  # Log the full response
                response_json = response.json()

                # Check if the response is a list and contains a similarity score
                if isinstance(response_json, list) and len(response_json) > 0:
                    similarity_scores = response_json  # The response is a list of similarity scores
                    return similarity_scores  # Return the similarity scores
                else:
                    raise Exception("Unexpected response structure.")
            elif response.status_code == 503:
                print("Model is loading, retrying...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                raise Exception(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.Timeout:
            print(f"Request timed out after {timeout} seconds, retrying...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
        except Exception as e:
            raise e
    
    raise Exception(f"Failed to get similarity score after {retries} retries.")


def get_similarities(new_desc, existing_descs, threshold=0.5):
    # Get similarity scores for the new description compared to each existing description
    similarity_scores = get_similarity_score(new_desc, existing_descs)
    
    # Filter descriptions based on the threshold similarity score
    similar_descs = [
        (desc, score) for desc, score in zip(existing_descs, similarity_scores) if score > threshold
    ]
    
    print("Similar descriptions:", similar_descs)
    return similar_descs

