import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("commands.csv")
commands = df["Command"].values
actions = df["Action"].values
paths = df["Path"].values

vectorizer = TfidfVectorizer()
x = vectorizer.fit_transform(commands)

model = LogisticRegression()
model.fit(x, actions)

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
df.to_csv("processed_commands.csv", index=False)

print("Model Training Complete. 'Saved as model.pkl' ")