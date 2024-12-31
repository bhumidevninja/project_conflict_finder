from groq import Groq
import requests
import time
import os

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/paraphrase-MiniLM-L6-v2"

def get_similarity_score(new_desc, existing_descs, retries=3, delay=5, timeout=120):
    API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/paraphrase-MiniLM-L6-v2"
    HEADERS = {"Authorization": f"Bearer {os.getenv("HUGGING_FACE_TOKEN")}"}
    
    # Prepare the payload where we are comparing new_desc with each existing_desc
    payload = {
        "inputs": {
            "source_sentence": new_desc,  # The new description you're comparing
            "sentences": existing_descs    # List of existing descriptions to compare with
        }
    }

    for _ in range(retries):
        try:
            # Make the API request
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=timeout)

            if response.status_code == 200:
                response_json = response.json()
                print("Response JSON:", response_json)  # Log the full response for debugging
                
                # Check if the response contains similarity scores
                if isinstance(response_json, list) and len(response_json) > 0:
                    similarity_scores = response_json  # The response is a list of similarity scores
                    return similarity_scores
                else:
                    raise Exception("Unexpected response structure or empty result.")

            elif response.status_code == 503:
                # Retry if the model is not ready
                print("Model is loading, retrying...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff

            else:
                # Handle other HTTP errors
                raise Exception(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.Timeout:
            # Retry if the request times out
            print(f"Request timed out after {timeout} seconds, retrying...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff

        except requests.exceptions.RequestException as e:
            # Catch other types of requests exceptions
            print(f"Request error: {str(e)}")
            time.sleep(delay)
            delay *= 2  # Exponential backoff

    raise Exception(f"Failed to get similarity score after {retries} retries.")


def get_similarities(new_desc, existing_descs, threshold=0.6):
    # Get similarity scores for the new description compared to each existing description
    similarity_scores = get_similarity_score(new_desc, existing_descs)
    
    # Filter descriptions based on the threshold similarity score
    similar_descs = [
        (desc, score) for desc, score in zip(existing_descs, similarity_scores) if score > threshold
    ]
    
    return similar_descs


def get_suggestions(description):
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"here is my project topic description\\n. {description}. can you please list out  unique feature that i can add into this? give only 5 suggestion which is easy to integrate and handle",
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content

