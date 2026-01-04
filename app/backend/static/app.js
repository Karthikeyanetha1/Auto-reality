document.getElementById("diagnoseForm").onsubmit = async (e) => {
  e.preventDefault();

  const file = document.getElementById("file").files[0];
  const data = new FormData();
  data.append("file", file);

  document.getElementById("output").textContent = "Analyzing...";

  const res = await fetch("/detect", {
    method: "POST",
    body: data
  });

  const json = await res.json();
  document.getElementById("output").textContent =
    JSON.stringify(json, null, 2);
};
