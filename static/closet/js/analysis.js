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

  document.getElementById("result").textContent = JSON.stringify(
    result,
    null,
    2
  );

  if (result.outfit_id) {
    document.getElementById(
      "outfit-id-display"
    ).textContent = `Outfit ID: ${result.outfit_id}`;
    elements.saveToClosetButton.setAttribute(
      "data-outfit-id",
      result.outfit_id
    );
    elements.saveToClosetButton.style.display = "block"; // 버튼 보이기
    elements.saveToClosetButton.disabled = false;
  }

  updateUIWithResult(elements, result);
}

function updateUIForUpload(elements) {
  elements.uploadButton.disabled = true;
  elements.loadingDiv.style.display = "block";
  elements.errorSection.style.display = "none";
  elements.fileSelectButton.style.display = "none";
}

function updateUIWithResult(elements, result) {
  elements.resultText.textContent = JSON.stringify(result, null, 2);
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
