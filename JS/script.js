// script.js

const dropZone = document.getElementById("drop-zone");
const output = document.getElementById("output");
const MAX_FILE_SIZE = 1024 * 1024; // 1MB max

// highlight drop zone when file is dragged over
dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("hover");
});

// remove highlight when drag leaves
dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("hover");
});

// handle dropped file
dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("hover");

    const file = e.dataTransfer.files[0];
    if (!file) {
        output.textContent = "No file dropped.";
        return;
    }

    if (!file.name.endsWith(".json")) {
        output.textContent = "Please drop a valid .json file.";
        return;
    }

    if (file.type !== "application/json") {
        output.textContent = "File is not a valid JSON type.";
        return;
    }

    if (file.size > MAX_FILE_SIZE) {
        output.textContent = "File is too large. Max 1MB allowed.";
        return;
    }

    const reader = new FileReader();

    reader.onload = (event) => {
        const text = event.target.result.trim();
        if (text === "") {
            output.textContent = "File is empty.";
            return;
        }

        try {
            const json = JSON.parse(text);
            output.textContent = JSON.stringify(json, null, 2);
        } catch (err) {
            output.textContent = "Invalid JSON:\n" + err.message;
        }
    };

    reader.onerror = () => {
        output.textContent = "Error reading file.";
    };

    reader.readAsText(file);
});
// clear output when clicking on drop zone
dropZone.addEventListener("click", () => {
    output.textContent = "";
}); 
