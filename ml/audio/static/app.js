function refresh() {
  fetch("/status")
    .then(r => r.json())
    .then(d => {
      document.getElementById("confidence").innerText = d.confidence;

      let badge = document.getElementById("badge");
      badge.innerText = d.severity;
      badge.className = "badge " + d.severity.toLowerCase();

      let bar = document.getElementById("bar");
      bar.style.width = (d.confidence * 100) + "%";

      if (d.severity === "NORMAL") bar.style.background = "#22c55e";
      if (d.severity === "WARNING") bar.style.background = "#facc15";
      if (d.severity === "CRITICAL") bar.style.background = "#ef4444";
    });
}

refresh();
setInterval(refresh, 10000);
