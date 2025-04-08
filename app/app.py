from flask import Flask, render_template, request
from search import search_documents

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    query = request.form.get("query", "")  # Получаем запрос из формы
    results = []
    
    if query:
        results = search_documents(query)  # Запускаем поиск по запросу
    
    return render_template("index.html", query=query, results=results)

if __name__ == "__main__":
    app.run(debug=True)