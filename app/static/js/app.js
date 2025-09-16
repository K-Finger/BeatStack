const form = document.getElementById("upload-form");
const result = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  result.textContent = "Uploading…";

  const data = new FormData(form);
  // title, tags, image, audio are all included by default

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

document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM loaded, binding button");

  const titleEl = document.getElementById("title");
  const tagsEl  = document.getElementById("tags");
  const btn     = document.getElementById("generate-tags");

  if (!btn) {
    console.error("No generate-tags button found");
    return;
  }

  btn.addEventListener("click", async () => {
    const title = titleEl.value.trim();
    console.log("Generate clicked, title=", title);

    if (!title) {
      alert("Please enter a title first.");
      return;
    }

    btn.disabled = true;
    btn.textContent = "Generating…";

    try {
      const resp = await fetch("/api/tags/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title })
      });

      console.log("Tag API response status:", resp.status);

      if (!resp.ok) {
        const text = await resp.text();
        console.error("Tag API error body:", text);
        throw new Error(text || resp.statusText);
      }

      const { tags } = await resp.json();
      console.log("Tags received:", tags);

      // fill the input (comma+space separated)
      tagsEl.value = tags.join(", ");
    } catch (err) {
      console.error("Failed to generate tags:", err);
      alert("Failed to generate tags. Check console for details.");
    } finally {
      btn.disabled = false;
      btn.textContent = "Generate Tags";
    }
  });
});
