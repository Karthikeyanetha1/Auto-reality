import { CameraPreview } from '@capacitor-community/camera-preview';

const canvas = document.getElementById("overlay");
const ctx = canvas.getContext("2d");
const instruction = document.getElementById("instruction");

let lastBBox = null;
let isRequestInFlight = false;

// ======= TUNING VALUES =======
const SEND_INTERVAL = 350; // ms (safe for mobile)
const SMOOTHING = 0.25;     // 0.15–0.3 (lower = smoother)
// ============================

async function startCamera() {
  await CameraPreview.start({
    position: 'rear',
    parent: 'camera-container',
    className: 'camera-preview',
    toBack: true
  });

  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  setInterval(sendFrame, SEND_INTERVAL);
}

// ===== SEND FRAME TO AI =====
async function sendFrame() {
  if (isRequestInFlight) return;
  isRequestInFlight = true;

  try {
    const frame = await CameraPreview.capture({ quality: 55 });
    const img = "data:image/jpeg;base64," + frame.value;

    const res = await fetch("/detect", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: img })
    });

    const result = await res.json();
    drawResult(result);
  } catch (e) {
    console.warn("AI frame dropped");
  }

  isRequestInFlight = false;
}

// ===== DRAW + SMOOTH =====
function drawResult(result) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (!result || !result.bbox) return;

  let [x, y, w, h] = result.bbox;

  // EMA smoothing
  if (lastBBox) {
    x = smooth(x, lastBBox.x);
    y = smooth(y, lastBBox.y);
    w = smooth(w, lastBBox.w);
    h = smooth(h, lastBBox.h);
  }

  lastBBox = { x, y, w, h };

  ctx.strokeStyle = "#00ff66";
  ctx.lineWidth = 4;
  ctx.strokeRect(
    x * canvas.width,
    y * canvas.height,
    w * canvas.width,
    h * canvas.height
  );

  instruction.innerText = result.issue || "Analyzing...";
}

function smooth(current, previous) {
  return previous + SMOOTHING * (current - previous);
}

startCamera();
