iimport { CameraPreview } from "@capacitor-community/camera-preview";

const canvas = document.getElementById("overlay");
const ctx = canvas.getContext("2d");
const instruction = document.getElementById("instruction");

let targetBox = null;
let currentBox = null;
let lastSent = 0;
let lastSpokenIssue = null;

/* ----------------- HELPERS ----------------- */

function lerp(a, b, t) {
  return a + (b - a) * t;
}

/* ----------------- VOICE ----------------- */

function speakOnce(text) {
  if (!window.speechSynthesis) return;
  if (text === lastSpokenIssue) return;

  lastSpokenIssue = text;
  window.speechSynthesis.cancel();

  const msg = new SpeechSynthesisUtterance(text);
  msg.rate = 0.95;
  msg.pitch = 1;
  msg.lang = "en-US";

  window.speechSynthesis.speak(msg);
}

/* ----------------- HAPTICS ----------------- */

function vibrateSeverity(confidence) {
  if (!navigator.vibrate) return;

  if (confidence < 0.6) {
    navigator.vibrate(60);
  } else if (confidence < 0.8) {
    navigator.vibrate([120, 80, 120]);
  } else {
    navigator.vibrate([300, 150, 300]);
  }
}

/* ----------------- CAMERA ----------------- */

async function startCamera() {
  await CameraPreview.start({
    position: "rear",
    parent: "camera-container",
    className: "camera-preview",
    width: window.innerWidth,
    height: window.innerHeight,
    toBack: true
  });

  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  requestAnimationFrame(drawLoop);
  setInterval(sendFrame, 350); // AI throttle (FPS safe)
}

/* ----------------- AI FRAME SEND ----------------- */

async function sendFrame() {
  const now = Date.now();
  if (now - lastSent < 350) return;
  lastSent = now;

  const frame = await CameraPreview.capture({ quality: 55 });
  const img = "data:image/jpeg;base64," + frame.value;

  fetch("/detect", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image: img })
  })
    .then(res => res.json())
    .then(res => {
      targetBox = res.bbox;
      instruction.innerText = res.issue;

      speakOnce(res.issue);
      vibrateSeverity(res.confidence);
    });
}

/* ----------------- DRAW LOOP ----------------- */

function drawLoop() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (targetBox) {
    if (!currentBox) currentBox = [...targetBox];

    for (let i = 0; i < 4; i++) {
      currentBox[i] = lerp(currentBox[i], targetBox[i], 0.15);
    }

    drawBox(currentBox);
  }

  requestAnimationFrame(drawLoop);
}

/* ----------------- BOX RENDER ----------------- */

function drawBox([x, y, w, h]) {
  ctx.strokeStyle = "#00ff88";
  ctx.lineWidth = 4;
  ctx.shadowColor = "#00ff88";
  ctx.shadowBlur = 10;

  ctx.strokeRect(
    x * canvas.width,
    y * canvas.height,
    w * canvas.width,
    h * canvas.height
  );
}

/* ----------------- START ----------------- */

startCamera();
