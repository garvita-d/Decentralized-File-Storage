const backend = "http://127.0.0.1:8000";

async function uploadFile() {
    let file = document.getElementById("fileInput").files[0];
    if (!file) return alert("Select a file first!");

    let formData = new FormData();
    formData.append("file", file);

    let res = await fetch(`${backend}/upload`, {
        method: "POST",
        body: formData
    });

    let data = await res.json();
    document.getElementById("uploadResult").innerHTML =
        `Uploaded!<br>Filename: ${data.filename}<br>CID: <b>${data.cid}</b>`;
}

async function downloadFile() {
    let cid = document.getElementById("cid").value.trim();
    if (!cid) return alert("Enter a CID");

    window.location.href = `${backend}/download/${cid}`;
}
