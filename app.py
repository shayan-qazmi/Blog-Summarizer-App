from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

app = Flask(__name__)

# 🔐 Set Gemini API key
genai.configure(api_key="AIzaSyArIx5p6ZNaswMrIRyCZIGT5Vcymwbkr7I")

# ✅ Create the model once
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

def generate_summary(text):
    try:
        prompt = f"""
        Create a professional summary of the following blog content.
        Start with a short introduction and end with a conclusion.

        Blog Content:
        {text[:10000]}  # Limit to 10,000 characters
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Failed to generate summary. Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    content = ""
    summary = ""
    if request.method == "POST":
        url = request.form["url"]
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.content, "html.parser")
            paragraphs = soup.find_all("p")
            content = "\n\n".join([p.get_text() for p in paragraphs])

            if content.strip():
                summary = generate_summary(content)
            else:
                summary = "No readable content found."
        except Exception as e:
            content = "Failed to scrape. Error: " + str(e)
    return render_template("index.html", content=content, summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
