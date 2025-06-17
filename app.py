from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS mbti_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ei TEXT, sn TEXT, tf TEXT, jp TEXT,
            mbti TEXT, result TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_mbti_result(mbti):
    descriptions = {
        "INTJ": "獨立思考的戰略家，擅長規劃與預測未來。",
        "INFP": "溫柔理想主義者，重視價值與內在世界。",
        "ENTP": "熱情創意發想者，喜歡挑戰與改變。",
        "ISFJ": "忠誠細心的守護者，關注他人需求。",
        # 可以加更多類型
    }
    return descriptions.get(mbti, "你是一位獨特的人格類型！")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    ei = data["ei"]
    sn = data["sn"]
    tf = data["tf"]
    jp = data["jp"]
    mbti = ei + sn + tf + jp
    result = get_mbti_result(mbti)

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO mbti_results (ei, sn, tf, jp, mbti, result) VALUES (?, ?, ?, ?, ?, ?)",
              (ei, sn, tf, jp, mbti, result))
    conn.commit()
    conn.close()

    return jsonify({"mbti": mbti, "result": result})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
