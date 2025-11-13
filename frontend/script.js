const API_URL = "http://127.0.0.1:5000/api"; // Flask backend

async function uploadFile() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];
  const status = document.getElementById("uploadStatus");

  if (!file) {
    status.innerText = "Please select a file first.";
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  status.innerText = " Uploading...";

  try {
    const response = await fetch(`${API_URL}/upload`, {
      method: "POST",
      body: formData,
    });
    const data = await response.json();

    if (data.hash) {
      status.innerText = ` Uploaded successfully. Hash: ${data.hash}`;
      fetchFiles();
    } else {
      status.innerText = " Upload failed.";
    }
  } catch (err) {
    console.error(err);
    status.innerText = " Error uploading file.";
  }
}

async function fetchFiles() {
  const list = document.getElementById("fileList");
  list.innerHTML = "<li>Loading...</li>";

  try {
    const response = await fetch(`${API_URL}/files`);
    const files = await response.json();
    list.innerHTML = "";

    if (files.length === 0) {
      list.innerHTML = "<li>No files found.</li>";
      return;
    }

    files.forEach((file) => {
      const li = document.createElement("li");
      li.innerHTML = `
        <span><b>${file.name}</b> <small>(${file.hash})</small></span>
        <button onclick="downloadFile('${file.hash}')">Download</button>
      `;
      list.appendChild(li);
    });
  } catch (err) {
    console.error(err);
    list.innerHTML = "<li>Error fetching files.</li>";
  }
}

async function searchByHash() {
  const hash = document.getElementById("hashInput").value.trim();
  const result = document.getElementById("searchResult");

  if (!hash) {
    result.innerText = "Please enter a hash.";
    return;
  }

  try {
    const response = await fetch(`${API_URL}/find/${hash}`);
    const data = await response.json();

    if (data.found) {
      result.innerText = ` File found: ${data.filename}`;
    } else {
      result.innerText = " File not found in this node.";
    }
  } catch (err) {
    result.innerText = " Error searching for file.";
  }
}

function downloadFile(hash) {
  window.location.href = `${API_URL}/download/${hash}`;
}
