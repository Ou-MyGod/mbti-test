const questions = [
  { q: "🎉 聚會後你會？", a: ["精神充滿", "需要獨處"], type: ["E", "I"] },
  { q: "🤝 遇到新朋友你？", a: ["主動交談", "等對方開口"], type: ["E", "I"] },
  { q: "🗓️ 假日偏好？", a: ["參加活動", "待在家裡"], type: ["E", "I"] },
  { q: "🔍 面對資訊你？", a: ["重視細節", "尋找可能性"], type: ["S", "N"] },
  { q: "✈️ 旅行時你？", a: ["行前規劃清楚", "邊走邊看"], type: ["S", "N"] },
  { q: "🎨 想像力？", a: ["不太發揮", "天馬行空"], type: ["S", "N"] },
  { q: "💔 安慰朋友？", a: ["給建議分析", "情感陪伴"], type: ["T", "F"] },
  { q: "📊 看報表？", a: ["數據優先", "感受重要"], type: ["T", "F"] },
  { q: "⚖️ 做決定？", a: ["邏輯推理", "照內心感覺"], type: ["T", "F"] },
  { q: "🎒 出門前？", a: ["整理清單", "隨便抓了就走"], type: ["J", "P"] },
  { q: "🗂️ 安排行程？", a: ["照表操課", "隨機應變"], type: ["J", "P"] },
  { q: "📅 工作風格？", a: ["規劃式", "自由式"], type: ["J", "P"] },
];

let current = 0;
let answers = [];

function startTest() {
  document.getElementById("startCard").style.display = "none";
  document.getElementById("questionCard").style.display = "block";
  showQuestion();
}

function showQuestion() {
  const q = questions[current];
  document.getElementById("questionText").innerText = q.q;
  document.getElementById("btnA").innerText = q.a[0];
  document.getElementById("btnB").innerText = q.a[1];
  document.getElementById("progress").innerText = `第 ${current + 1} / ${questions.length} 題`;
}

function selectAnswer(choice) {
  const q = questions[current];
  answers.push(choice === "A" ? q.type[0] : q.type[1]);
  current++;
  if (current >= questions.length) {
    submitAnswers();
  } else {
    showQuestion();
  }
}

function submitAnswers() {
  const nickname = document.getElementById("nickname").value || "匿名";
  fetch("/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nickname, answers })
  })
  .then(res => res.json())
 .then(data => {
  console.log("伺服器回傳資料：", data); // ← 加這行看後端回什麼
  document.getElementById("questionCard").style.display = "none";
  document.getElementById("resultCard").style.display = "block";
  document.getElementById("mbtiResult").innerText = `${nickname}：${data.mbti}｜${data.result}`;
});
}

function loadHistory() {
  fetch("/history")
    .then(res => res.json())
    .then(list => {
      const ul = document.getElementById("historyList");
      ul.innerHTML = "";
      list.forEach(item => {
        const li = document.createElement("li");
        li.innerText = `${item.nickname}：${item.mbti}｜${item.result}`;
        ul.appendChild(li);
      });
    });
}
