from flask import Flask
import requests
import os
from bs4 import BeautifulSoup

app = Flask(__name__)

response = """
<html>
<head>
<title>Python 230: Ustjay ethay Actsfayig</title>
</head>
<body>
<h1>Python 230: Ustjay ethay Actsfayig</h1>
<p>Original quote: {src_quote}</p>
<p>Pig Latinized quote: {pig_quote}</p>
<p><a href="/">Again!</a></p>
</body>
</html>
"""

def get_fact():
    fact_response = requests.get("http://unkno.com/")

    soup = BeautifulSoup(fact_response.content, "html.parser")
    fact = soup.find_all("div", id="content")

    return fact[0].getText().strip()


def piggify(src_quote):
    data = {'input_text': src_quote}
    quotify_response = requests.post(url="https://hidden-journey-62459.herokuapp.com/piglatinize/", data=data)
    soup = BeautifulSoup(quotify_response.content, "html.parser")
    soup.body.h1.decompose()
    soup.body.h2.decompose()
    return soup.body

@app.route('/', methods=['GET'])
def get_index():
    src_quote = get_fact()
    pig_quote = piggify(src_quote)
    return response.format(src_quote=src_quote, pig_quote=pig_quote)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)