//이미지 미리보기
function previewImage(input) {
  const previewIcon = document.getElementById("image-preview-icon");
  const previewImage = document.getElementById("preview-image");
  const previewContainer = document.getElementById("preview-container");
  const uploadButton = document.getElementById("upload-btn");
  const fileSelectButton = document.getElementById("file-input-container");
  const uploadControls = document.getElementById("upload-controls");

  if (!input.files || input.files.length === 0) {
    resetPreview();
    return;
  }

  const reader = new FileReader();
  reader.onload = function (e) {
    setupPreview(e.target.result);
  };
  reader.readAsDataURL(input.files[0]);
}

function resetPreview() {
  const elements = {
    previewIcon: document.getElementById("image-preview-icon"),
    previewImage: document.getElementById("preview-image"),
    uploadButton: document.getElementById("upload-btn"),
    fileSelectButton: document.getElementById("file-input-container"),
    previewContainer: document.getElementById("preview-container"),
    uploadControls: document.getElementById("upload-controls"),
  };

  elements.previewIcon.style.display = "inline-block";
  elements.previewImage.style.display = "none";
  elements.uploadButton.style.display = "none";
  elements.fileSelectButton.style.display = "block";
  elements.previewContainer.style.display = "flex";
  elements.previewContainer.style.flexDirection = "column";
  elements.uploadControls.style.display = "flex";
  elements.uploadControls.style.flexDirection = "column";
}

function setupPreview(imageUrl) {
  const elements = {
    previewContainer: document.getElementById("preview-container"),
    uploadControls: document.getElementById("upload-controls"),
    previewIcon: document.getElementById("image-preview-icon"),
    previewImage: document.getElementById("preview-image"),
    fileSelectButton: document.getElementById("file-input-container"),
    uploadButton: document.getElementById("upload-btn"),
    customUploadButton: document.getElementById("custom-upload-btn"),
  };

  elements.previewContainer.style.display = "flex";
  elements.previewContainer.style.flexDirection = "row";
  elements.uploadControls.style.display = "flex";
  elements.uploadControls.style.flexDirection = "column";
  elements.previewIcon.style.display = "none";
  elements.previewImage.src = imageUrl;
  elements.previewImage.style.display = "block";
  elements.fileSelectButton.style.display = "block";
  elements.uploadButton.style.display = "inline-block";
  elements.customUploadButton.style.display = "none";
}
