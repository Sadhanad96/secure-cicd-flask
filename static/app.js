document.addEventListener("DOMContentLoaded", () => {
  const uploadBtn = document.getElementById("uploadBtn");
  const clearBtn = document.getElementById("clearBtn");
  const fileInput = document.getElementById("codefile");
  const status = document.getElementById("status");
  const resultBox = document.getElementById("resultBox");
  const resultsEl = document.getElementById("results");

  uploadBtn.addEventListener("click", async () => {
    const file = fileInput.files[0];
    if (!file) {
      status.innerHTML = `<p class="text-sm text-red-600">Select a .py file first.</p>`;
      return;
    }
    status.innerHTML = `<p class="text-sm text-gray-600">Uploading & scanning... ⏳</p>`;
    const fd = new FormData();
    fd.append("codefile", file);

    try {
      const res = await fetch("/upload", {
        method: "POST",
        body: fd
      });
      if (!res.ok) {
        const txt = await res.text();
        status.innerHTML = `<p class="text-sm text-red-600">Error: ${res.status} ${txt}</p>`;
        return;
      }
      const data = await res.json();
      status.innerHTML = `<p class="text-sm text-green-600">Scan completed for ${data.filename}</p>`;
      resultBox.classList.remove("hidden");
      resultsEl.textContent = JSON.stringify(data.results, null, 2);
    } catch (err) {
      status.innerHTML = `<p class="text-sm text-red-600">Network or server error.</p>`;
      console.error(err);
    }
  });

  clearBtn.addEventListener("click", () => {
    fileInput.value = "";
    status.innerHTML = "";
    resultsEl.textContent = "";
    resultBox.classList.add("hidden");
  });
});
