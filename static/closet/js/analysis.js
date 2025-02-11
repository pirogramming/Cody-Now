let isUploading = false;
let analysisResult = null;

document.querySelector("form").onsubmit = async function (event) {
  event.preventDefault();
  if (isUploading) return;

  const elements = {
    fileSelectButton: document.getElementById("file-input-container"),
    uploadButton: document.getElementById("upload-btn"),
    loadingDiv: document.getElementById("loading"),
    resultSection: document.getElementById("result-section"),
    resultText: document.getElementById("result"),
    uploadControls: document.getElementById("upload-controls"),
    errorSection: document.getElementById("error-section"),
    errorMessage: document.getElementById("error-message"),
    errorTrace: document.querySelector(".error-trace"),
    getCodyButton: document.getElementById("get-cody"),
    saveToClosetButton: document.getElementById("saveToClosetBtn"),
  };

  try {
    await handleFormSubmit(event.target, elements);
  } catch (error) {
    handleError(error, elements);
  } finally {
    isUploading = false;
    elements.uploadButton.disabled = false;
    elements.loadingDiv.style.display = "none";
  }
};

async function handleFormSubmit(form, elements) {
  isUploading = true;
  updateUIForUpload(elements);

  const formData = new FormData(form);
  const response = await fetch("", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("알 수 없는 오류가 발생했습니다.");
  }
  const result = await response.json();
  console.log(result);
  analysisResult = result;

  const analysisData = result.data ? result.data : result;
  displayFilteredResults(analysisData);

  if (result.outfit_id) {
    document.getElementById(
      "outfit-id-display"
    ).textContent = `Outfit ID: ${result.outfit_id}`;
    document
      .getElementById("saveToClosetBtn")
      .setAttribute("data-outfit-id", result.outfit_id);
    document.getElementById("saveToClosetBtn").disabled = false;
  }

  updateUIWithResult(elements);
}

function updateUIForUpload(elements) {
  elements.uploadButton.disabled = true;
  elements.loadingDiv.style.display = "block";
  elements.errorSection.style.display = "none";
  elements.fileSelectButton.style.display = "none";
}

function updateUIWithResult(elements) {
  elements.resultSection.style.display = "block";
  elements.uploadControls.classList.add("hidden");
  elements.getCodyButton.style.display = "block";
  elements.loadingDiv.style.display = "none";

  // ✅ 버튼을 보이게 설정
  const saveButton = document.getElementById("show-category-slide");
  if (saveButton) {
    saveButton.style.display = "block"; // 버튼 표시
  }
}

function handleError(error, elements) {
  console.error("Error:", error);
  elements.errorSection.style.display = "block";
  elements.errorMessage.textContent =
    error.message || "AI 분석 중 오류가 발생했습니다. 다시 시도해주세요.";
  elements.fileSelectButton.style.display = "block";
  elements.loadingDiv.style.display = "none";
  isUploading = false;
}

function displayFilteredResults(data) {
  const displayContainer = document.getElementById("result");
  displayContainer.innerHTML = "";

  if (!data || Object.keys(data).length === 0) {
    console.warn("분석 데이터가 비어 있습니다:", data);
    displayContainer.textContent = "분석 결과가 없습니다.";
    return;
  }

  const infoContainer = document.createElement("div");
  infoContainer.classList.add("info-container");

  const tagsContainer = document.createElement("div");
  tagsContainer.classList.add("tags");
  if (data.tag && Array.isArray(data.tag)) {
    data.tag.forEach((tag) => {
      const tagElement = document.createElement("a");
      tagElement.href = "#";
      tagElement.textContent = `#${tag}`;
      tagElement.classList.add("tag-item");
      tagsContainer.appendChild(tagElement);
    });
  }

  const categoryInfo = document.createElement("div");
  categoryInfo.classList.add("result-section");
  const filteredData = {
    Category: data.category || "없음",
    Fit: data.fit || "없음",
    Season: data.season || "없음",
    Style: data.design_style || "없음",
    Detail: data.detail || "없음",
  };

  Object.entries(filteredData).forEach(([key, value]) => {
    const p = document.createElement("p");
    p.innerHTML = `<span class="bold">${key}:</span> ${
      Array.isArray(value) ? value.join(", ") : value
    }`;
    categoryInfo.appendChild(p);
  });

  const productCommentSection = document.createElement("div");
  productCommentSection.classList.add("product-comment-section");

  const productComment = document.createElement("p");
  productComment.classList.add("product-comment");
  productComment.innerHTML = `<span class="bold">Product Comment</span><br>${
    data.comment || "제품 설명이 없습니다."
  }`;

  productCommentSection.appendChild(productComment);

  infoContainer.appendChild(tagsContainer);
  infoContainer.appendChild(categoryInfo);

  displayContainer.appendChild(infoContainer);
  displayContainer.appendChild(productCommentSection);
}

document.addEventListener("DOMContentLoaded", function () {
  const saveButton = document.getElementById("show-category-slide");
  const categorySlider = document.getElementById("show-category-slider");

  if (saveButton) {
    saveButton.addEventListener("click", function () {
      if (categorySlider) {
        categorySlider.style.display = "flex"; // 슬라이더 표시
        setTimeout(() => {
          categorySlider.classList.add("show-slide"); // 애니메이션 적용
        }, 10);
      } else {
        console.error("Error: show-category-slider element not found!");
      }
    });
  }
});
function closeSlide() {
  const categorySlider = document.getElementById("show-category-slider");
  if (categorySlider) {
    categorySlider.classList.remove("show-slide");
    setTimeout(() => {
      categorySlider.style.display = "none";
    }, 300);
  }
}

// ✅ 전역 등록
window.closeSlide = closeSlide;
