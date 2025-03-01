import pandas as pd
import joblib
import subprocess
import nltk
from fuzzywuzzy import process

# Load trained model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
df = pd.read_csv("processed_commands.csv")

# Preprocess: Normalize text (lowercase, remove punctuation)
def preprocess_text(text):
    text = text.lower()
    text = "".join([char for char in text if char.isalnum() or char.isspace()])
    return text

# Function to find the closest matching command
def get_best_match(command_text):
    command_text = preprocess_text(command_text)
    command_list = df["Command"].tolist()
    
    best_match, score = process.extractOne(command_text, command_list)
    if score > 80:
        return best_match
    return None

# Function to predict and execute command
def process_command(command_text):
    best_match = get_best_match(command_text)
    if not best_match:
        print("Sorry, I couldn't recognize that command.")
        return

    X_test = vectorizer.transform([best_match])
    predicted_action = model.predict(X_test)[0]
    
    # Get execution path
    action_path = df.loc[df["Action"] == predicted_action, "Path"].values[0]

    print(f"Executing: {predicted_action} ({action_path})")

    try:
        subprocess.run(action_path, shell=True)
    except Exception as e:
        print(f"Error executing command: {e}")

# Example usage
test_command = "ok baasha I like to open my chrome for me "
process_command(test_command)