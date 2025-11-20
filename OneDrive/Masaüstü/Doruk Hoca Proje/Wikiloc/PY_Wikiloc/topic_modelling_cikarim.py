import json
from bs4 import BeautifulSoup
import re

# Path to your HTML file
html_path = r"C:\Users\aylin\Downloads\topic_visualization.html"

# Load the HTML
with open(html_path, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Find the script tag containing the LDAvis data
script_tags = soup.find_all("script")
json_data = None

for tag in script_tags:
    if tag.string and "ldavis" in tag.string and "data =" in tag.string:
        # 🛠 NON-GREEDY match to avoid extra data issue
        match = re.search(r"var\s+ldavis_[^=]*=\s+({.*?});", tag.string, re.DOTALL)
        if match:
            json_data = match.group(1)
            break

if not json_data:
    raise ValueError("❌ Could not find LDAvis JSON data.")

# Load JSON safely
data = json.loads(json_data)

# Function to extract top words
def get_top_words_per_topic(data, lambda_value=0.2, n_words=15):
    topic_info = data["tinfo"]
    topics = sorted(set(data["mdsDat"]["topics"]))

    topic_words = {topic: [] for topic in topics}

    for i in range(len(topic_info["Term"])):
        category = topic_info["Category"][i]
        if category.startswith("Topic"):
            parts = category.split()
            if len(parts) == 2 and parts[1].isdigit():
                topic_num = int(parts[1])
                term = topic_info["Term"][i]
                relevance = lambda_value * topic_info["logprob"][i] + (1 - lambda_value) * topic_info["loglift"][i]
                topic_words[topic_num].append((term, relevance))
            else:
                print(f"⚠️ Skipping malformed category entry: {category}")

    # Sort and return top terms
    top_words_per_topic = {}
    for topic, terms in topic_words.items():
        sorted_terms = sorted(terms, key=lambda x: -x[1])[:n_words]
        top_words_per_topic[topic] = [term for term, _ in sorted_terms]

    return top_words_per_topic

# Get top words
top_words = get_top_words_per_topic(data, lambda_value=0.2, n_words=15)

# Print results
for topic_id, words in top_words.items():
    print(f"Topic {topic_id}: {', '.join(words)}")
