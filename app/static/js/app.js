const form = document.getElementById("upload-form");
const result = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  result.textContent = "Uploading…";

  const data = new FormData(form);
  // title, image, audio are all included by default

  try {
    const res = await fetch("/api/uploads", {
      method: "POST",
      body: data
    });
    if (!res.ok) throw new Error(res.statusText);

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    result.innerHTML = `<video controls src="${url}" style="max-width: 100%;"></video>`;
  } catch (err) {
    result.textContent = "Error: " + err.message;
  }
});
