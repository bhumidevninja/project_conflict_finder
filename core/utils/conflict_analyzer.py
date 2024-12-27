from sentence_transformers import SentenceTransformer,util

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def get_similarities(new_desc, existing_descs):
    new_embedding = model.encode(new_desc, convert_to_tensor=True)
    existing_embeddings = model.encode(existing_descs, convert_to_tensor=True)
    similarities = util.cos_sim(new_embedding, existing_embeddings)
    similarity_scores = similarities[0].tolist()

    # Process results
    threshold = 0.5
    similar_descs = [
        (desc, score) for desc, score in zip(existing_descs, similarity_scores) if score > threshold
    ]
    print(similar_descs)
    return similar_descs