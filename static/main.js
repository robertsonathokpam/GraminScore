document.addEventListener("DOMContentLoaded", function() {
    
    const fileInput = document.getElementById("fileInput");
    const previewDiv = document.getElementById("filePreview");
    const dropZone = document.getElementById("dropZone");
    const form = document.getElementById("analyzeForm");
    const submitBtn = document.getElementById("submitBtn");
    const loader = document.getElementById("loadingOverlay");

    // File Selection Logic
    fileInput.addEventListener("change", function() {
        previewDiv.innerHTML = ""; // Clear existing
        if (this.files && this.files.length > 0) {
            
            // Loop through files and create little tags
            Array.from(this.files).forEach(file => {
                const tag = document.createElement("span");
                tag.className = "file-tag";
                tag.textContent = file.name;
                previewDiv.appendChild(tag);
            });

            // Change border to green to indicate success
            dropZone.style.borderColor = "#10b981";
            dropZone.style.backgroundColor = "#f0fdf4";
        }
    });

    // Form Submit Animation
    if(form) {
        form.addEventListener("submit", function() {
            submitBtn.style.display = "none";
            loader.classList.remove("hidden");
            loader.style.display = "flex";
        });
    }

    // Drag & Drop Visuals
    if(dropZone) {
        ['dragenter', 'dragover'].forEach(eName => {
            dropZone.addEventListener(eName, (e) => {
                e.preventDefault();
                dropZone.style.borderColor = "#2563eb";
                dropZone.style.transform = "scale(1.02)";
            });
        });

        ['dragleave', 'drop'].forEach(eName => {
            dropZone.addEventListener(eName, (e) => {
                e.preventDefault();
                dropZone.style.borderColor = "#cbd5e1";
                dropZone.style.transform = "scale(1)";
            });
        });

        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            fileInput.files = dt.files;
            // Trigger change event manually
            fileInput.dispatchEvent(new Event('change'));
        });
    }
});
