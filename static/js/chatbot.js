const chatBox = document.getElementById("chatBox");
const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");

function addMsg(who, text) {
  const wrap = document.createElement("div");
  wrap.className = `msg msg--${who}`;

  const meta = document.createElement("div");
  meta.className = "msg__meta";
  meta.textContent = who === "user" ? "You" : "MediBot";

  const body = document.createElement("div");
  body.textContent = text;

  wrap.appendChild(meta);
  wrap.appendChild(body);
  chatBox.appendChild(wrap);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function ask(message) {
  const res = await fetch("/chat/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  const data = await res.json();
  return data.reply || "No reply.";
}

addMsg("bot", "Hi! Tell me your symptoms or a health question. I’ll provide general guidance.");

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const msg = (chatInput.value || "").trim();
  if (!msg) return;
  chatInput.value = "";
  addMsg("user", msg);
  addMsg("bot", "Thinking…");
  const last = chatBox.lastElementChild;
  try {
    const reply = await ask(msg);
    last.querySelector("div:last-child").textContent = reply;
  } catch (err) {
    last.querySelector("div:last-child").textContent = `Error: ${err}`;
  }
});

