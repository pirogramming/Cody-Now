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
  // 만약 응답이 { outfit_id, data: { ... } } 형식이면 data 내부를 사용
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

function updateUIWithResult(elements, result) {
  elements.resultSection.style.display = "block";
  elements.uploadControls.classList.add("hidden");
  elements.getCodyButton.style.display = "block";
  elements.loadingDiv.style.display = "none";

  // ✅ "나만의 옷장에 저장하기" 버튼 표시
  const saveButton = document.getElementById("show-category-slide");
  saveButton.style.display = "block";

  // ✅ 버튼 클릭 시 슬라이드 열기 이벤트 추가
  saveButton.addEventListener("click", openSlide);
}
document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("show-category-slide").style.display = "none";
});

function handleError(error, elements) {
  console.error("Error:", error);
  elements.errorSection.style.display = "block";
  elements.errorMessage.textContent =
    error.message || "AI 분석 중 오류가 발생했습니다. 다시 시도해주세요.";
  elements.fileSelectButton.style.display = "block";
  elements.loadingDiv.style.display = "none";
  isUploading = false;
}
// 분석 결과를 화면에 표시하는 함수 (디버깅 코드 포함)
function displayFilteredResults(data) {
  const displayContainer = document.getElementById("result");
  const displayContainer_Comment = document.getElementById("product-comment-tag");
  displayContainer.innerHTML = ""; // 기존 결과 초기화
  displayContainer_Comment.innerHTML = "";
  if (!data || Object.keys(data).length === 0) {
    console.warn("분석 데이터가 비어 있습니다:", data);
    displayContainer.textContent = "분석 결과가 없습니다.";
    return;
  }

  // ✅ 정보 컨테이너 (제품 설명, 태그, 카테고리 정보)
  const infoContainer = document.createElement("div");
  infoContainer.classList.add("info-container");

  // ✅ 태그 섹션 (최상단)
  const tagsContainer = document.createElement("div");
  tagsContainer.classList.add("tags");
  if (data.tag && Array.isArray(data.tag)) {
    data.tag.forEach((tag) => {
      const tagElement = document.createElement("p");
      tagElement.textContent = `#${tag}`;
      tagElement.classList.add("tag-item");
      tagsContainer.appendChild(tagElement);
    });
  }

  // ✅ 카테고리 정보 (태그 아래)
  const categoryInfo = document.createElement("div");
  categoryInfo.classList.add("showresult-section");
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

  // ✅ Product Comment (독립된 아래 섹션)
  const productCommentSection = document.createElement("div");
  productCommentSection.classList.add("product-comment-section");

  const productComment = document.createElement("p");
  productComment.classList.add("product-comment");
  productComment.innerHTML = `<span class="bold">Product Comment</span><br>${
    data.comment || "제품 설명이 없습니다."
  }`;

  productCommentSection.appendChild(productComment);

  // ✅ 요소 배치 순서 조정
  infoContainer.appendChild(tagsContainer); // 태그
  infoContainer.appendChild(categoryInfo); // 카테고리 정보

  displayContainer.appendChild(infoContainer);
  displayContainer_Comment.appendChild(productCommentSection); // Product Comment는 독립된 아래 섹션
}


// "나만의 옷장에 저장하기" 버튼 클릭 이벤트 추가
document
  .getElementById("saveToClosetBtn")
  .addEventListener("click", async function () {
    const outfitId = this.getAttribute("data-outfit-id");
    if (!outfitId) return;

    try {
      const response = await fetch("/save-to-closet", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ outfit_id: outfitId }),
      });

      if (!response.ok) {
        throw new Error("옷장에 저장하는 중 오류가 발생했습니다.");
      }
      alert("나만의 옷장에 저장되었습니다!");
    } catch (error) {
      console.error("Error saving to closet:", error);
      alert("저장에 실패했습니다. 다시 시도해주세요.");
    }
  });
