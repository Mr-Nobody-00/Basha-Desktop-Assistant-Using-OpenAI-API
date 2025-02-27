import pandas as pd
import subprocess
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load CSV data
df = pd.read_csv("commands.csv")

# Extract commands, actions, and paths
commands = df["Command"].values
actions = df["Action"].values
paths = df["Path"].values  # New: Execution paths

# Convert text commands into numerical features
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(commands)

# Train Logistic Regression model
model = LogisticRegression()
model.fit(X, actions)

# Function to predict action and execute command
def process_command(command_text):
    X_test = vectorizer.transform([command_text])
    predicted_action = model.predict(X_test)[0]

    # Get execution path for the predicted action
    action_path = df.loc[df["Action"] == predicted_action, "Path"].values[0]

    print(f"Executing: {predicted_action} ({action_path})")

    try:
        subprocess.run(action_path, shell=True)
    except Exception as e:
        print(f"Error executing command: {e}")

# Example usage
test_command = "Hey baasha I like to open my spotify app to listen to the music"
process_command(test_command)
