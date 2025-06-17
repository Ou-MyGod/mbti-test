document.getElementById("mbtiForm").addEventListener("submit", async function (e) {
    e.preventDefault();
  
    const form = e.target;
    const data = {
      ei: form.ei.value,
      sn: form.sn.value,
      tf: form.tf.value,
      jp: form.jp.value
    };
  
    const res = await fetch("/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
  
    const json = await res.json();
    document.getElementById("result").innerHTML = `
      <h3>你的MBTI結果：${json.mbti}</h3>
      <p>${json.result}</p>
    `;
  });
  