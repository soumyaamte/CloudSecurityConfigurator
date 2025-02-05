function uploadFile() {
    let fileInput = document.getElementById('fileInput');
    if (fileInput.files.length === 0) {
        alert("Please select a file first.");
        return;
    }

    let file = fileInput.files[0];
    let formData = new FormData();
    formData.append("file", file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text()) // Expecting HTML content
    .then(data => {
        document.getElementById('report').innerHTML = data; // Inject report HTML
    })
    .catch(error => console.error('Error:', error));
}

document.getElementById('fileInput').addEventListener('change', function() {
    document.getElementById('fileName').textContent = "Selected File: " + this.files[0].name;
});
