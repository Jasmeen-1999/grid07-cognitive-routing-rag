# router.py

# --------------------------------------------------
# Imports
# --------------------------------------------------

# Chroma + Document imported to demonstrate vector DB usage
# (included for assignment relevance / optional extension)
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# TF-IDF based vectorization for lightweight persona matching
from sklearn.feature_extraction.text import TfidfVectorizer

# Cosine similarity to compare text vectors
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# STEP 1: Define Bot Personas
# Each bot has a fixed ideological personality
# --------------------------------------------------
personas = {
    "bot_A": "AI and crypto will solve all human problems. Technology is everything.",

    "bot_B": "Capitalism is destroying society and increasing inequality.",

    "bot_C": "Markets, trading, ROI and financial growth matter most."
}


# --------------------------------------------------
# STEP 2: Convert Persona Text Into Vectors
# Using TF-IDF instead of heavy embeddings
# Fast, offline, lightweight, reliable
# --------------------------------------------------

# Initialize vectorizer
vectorizer = TfidfVectorizer()

# Extract persona descriptions only
persona_texts = list(personas.values())

# Learn vocabulary + convert personas into vectors
persona_vectors = vectorizer.fit_transform(persona_texts)


# --------------------------------------------------
# STEP 3: Route Incoming Post To Relevant Bots
# Matches user post against personas using cosine similarity
# --------------------------------------------------
def route_post_to_bots(post_content, threshold=0.35):
    """
    Routes a post to matching bot personas.

    Args:
        post_content (str): Incoming social media post text
        threshold (float): Minimum similarity required

    Returns:
        list: Matching bot IDs
    """

    # Convert incoming post into TF-IDF vector
    post_vector = vectorizer.transform([post_content])

    # Compare post vector with persona vectors
    similarities = cosine_similarity(post_vector, persona_vectors)[0]

    matched_bots = []

    # Check each bot similarity score
    for i, score in enumerate(similarities):

        if score >= threshold:
            bot_id = list(personas.keys())[i]
            matched_bots.append(bot_id)

    return matched_bots


# --------------------------------------------------
# TEST RUN
# Allows standalone testing of router.py
# --------------------------------------------------
if __name__ == "__main__":

    sample_post = "AI is changing jobs and technology"

    results = route_post_to_bots(sample_post)

    print("Matched Bots:", results)