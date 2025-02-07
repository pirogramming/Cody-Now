//폼 제출 및 분석
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
  };

  try {
    await handleFormSubmit(event.target, elements);
  } catch (error) {
    handleError(error, elements);
  } finally {
    // 분석 완료 후 상태 초기화
    isUploading = false;
    elements.uploadButton.disabled = false;
    elements.loadingDiv.style.display = "none"; // 로딩바 숨기기
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
    throw new Error(result.error || "알 수 없는 오류가 발생했습니다.");
  }
  const result = await response.json();
  console.log(result);
  analysisResult = result;
// 만약 응답이 { outfit_id, data: { ... } } 형식이면 data 내부를 사용
  const analysisData = result.data ? result.data : result;
  displayFilteredResults(analysisData);

  if (result.outfit_id) {
    document.getElementById("outfit-id-display").textContent = `Outfit ID: ${result.outfit_id}`;
    document.getElementById("saveToClosetBtn").setAttribute("data-outfit-id", result.outfit_id);
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
  elements.loadingDiv.style.display = "none"; // 분석 결과가 표시될 때 로딩바 숨기기
}

function handleError(error, elements) {
  console.error("Error:", error);
  elements.errorSection.style.display = "block";
  elements.errorMessage.textContent =
    error.message || "AI 분석 중 오류가 발생했습니다. 다시 시도해주세요.";
  elements.fileSelectButton.style.display = "block";
  elements.loadingDiv.style.display = "none"; // 에러 발생 시에도 로딩바 숨기기
  isUploading = false;
}
// 분석 결과를 화면에 표시하는 함수 (디버깅 코드 포함)
function displayFilteredResults(data) {
  const displayContainer = document.getElementById("result");
  displayContainer.innerHTML = ""; // 이전 결과 초기화

  // 데이터가 올바르게 전달되었는지 확인
  if (!data || Object.keys(data).length === 0) {
    console.warn("분석 데이터가 비어 있습니다:", data);
    displayContainer.textContent = "분석 결과가 없습니다.";
    return;
  }
  // ✅ 태그 
  const tagsContainer = document.createElement("div");
  tagsContainer.classList.add("tags");
  if (data.tag && Array.isArray(data.tag)) {
      data.tag.forEach(tag => {
          const tagElement = document.createElement("a"); // 클릭 가능한 태그
          tagElement.href = "#";
          tagElement.textContent = `#${tag}`;
          tagElement.classList.add("tag-item");
          tagsContainer.appendChild(tagElement);
      });
  }
  // ✅ 카테고리 정보
  const infoContainer = document.createElement("div");
  infoContainer.classList.add("result-section");

  const filteredData = {
    "Category": data.category || "없음",
    "Fit": data.fit|| "없음",
    "Season": data.season || "없음",
    "Style": data.design_style || "없음",
    "Detail": data.detail || "없음",
  };

  // 동적으로 새로운 p 태그들을 생성하여 추가
  Object.entries(filteredData).forEach(([key, value]) => {
    const p = document.createElement("p");
    p.textContent = `${key}: ${Array.isArray(value) ? value.join(", ") : value}`;

    // 스타일 직접 적용
    p.style.fontSize = "14px";       // 글씨 크기
    p.style.color = "#333";          // 글자 색상 (어두운 회색)
    p.style.margin = "5px 0";        // 위아래 여백 추가
    p.style.fontWeight = key === "Category" || key === "Fit" || key === "Season" || key === "Style" || key === "Detail" || key === "Product Comment"? "bold" : "normal"; // 특정 키만 굵게

    displayContainer.appendChild(p);
  });
  // ✅ 제품 설명
  const productComment = document.createElement("p");
  productComment.classList.add("product-comment");
  productComment.textContent = `Product Comment: ${data.comment || "제품 설명이 없습니다."}`;

  displayContainer.appendChild(tagsContainer);
  displayContainer.appendChild(infoContainer);
  displayContainer.appendChild(productComment);

}


