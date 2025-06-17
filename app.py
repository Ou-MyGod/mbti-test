from flask import Flask, request, jsonify, render_template
import sqlite3
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def init_db():
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS mbti_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT NOT NULL,
                mbti TEXT NOT NULL,
                result TEXT NOT NULL
            )
        ''')
        conn.commit()

def get_mbti_description(mbti):
    descriptions = {
        "INTJ": ("🧠", "戰略家，冷靜分析、擅長規劃"),
        "INTP": ("📚", "哲學家，愛思考、邏輯導向"),
        "ENTJ": ("🦁", "領導者，果斷、有野心"),
        "ENTP": ("🎭", "辯論家，幽默創新"),
        "INFJ": ("🦉", "輔導者，理想主義與同理心"),
        "INFP": ("🌷", "治癒者，溫柔善感、重視價值"),
        "ENFJ": ("☀️", "主持人，溫暖領導型"),
        "ENFP": ("🦄", "夢想家，熱情創意爆棚"),
        "ISTJ": ("🗂️", "管理員，守紀律、務實"),
        "ISFJ": ("🛡️", "守護者，細心、照顧他人"),
        "ESTJ": ("🧱", "組織者，有效率、規則導向"),
        "ESFJ": ("🍰", "關懷者，社交高手、樂於助人"),
        "ISTP": ("🔧", "工匠型，喜歡動手、獨立"),
        "ISFP": ("🎨", "藝術家，隨和、熱愛美感"),
        "ESTP": ("🚀", "冒險家，行動快速、愛冒險"),
        "ESFP": ("🎉", "表演者，愛熱鬧、生活玩家")
    }
    return descriptions.get(mbti, ("❓", "未知類型"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.get_json()
        print("收到的原始資料：", data)

        nickname = data.get("nickname", "匿名")
        answers = data.get("answers", [])

        if not answers or len(answers) < 12:
            return jsonify({"error": "請完成全部 12 題測驗"}), 400

        counts = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
        for letter in answers:
            if letter in counts:
                counts[letter] += 1

        mbti = (
            "E" if counts["E"] >= counts["I"] else "I"
        ) + ("S" if counts["S"] >= counts["N"] else "N") + (
            "T" if counts["T"] >= counts["F"] else "F"
        ) + ("J" if counts["J"] >= counts["P"] else "P")

        emoji, description = get_mbti_description(mbti)
        result_text = f"{emoji} {description}"

        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO mbti_results (nickname, mbti, result) VALUES (?, ?, ?)",
                      (nickname, mbti, result_text))
            conn.commit()

        return jsonify({"mbti": mbti, "result": result_text})
    except Exception as e:
        print("🚨 錯誤發生：", e)
        return jsonify({"error": f"後端錯誤：{str(e)}"}), 500

@app.route("/history")
def history():
    try:
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("SELECT nickname, mbti, result FROM mbti_results ORDER BY id DESC LIMIT 10")
            rows = c.fetchall()
        return jsonify([
            {"nickname": row[0], "mbti": row[1], "result": row[2]} for row in rows
        ])
    except Exception as e:
        print("🚨 錯誤發生：", e)
        return jsonify({"error": f"資料庫讀取失敗：{str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(host="0.0.0.0", port=port)
