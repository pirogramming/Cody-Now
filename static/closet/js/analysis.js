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
  document.getElementById("result").textContent = JSON.stringify(
    result,
    null,
    2
  );
  if (result.outfit_id) {
    document.getElementById(
      "outfit-id-display"
    ).textContent = `Outfit ID: ${result.outfit_id}`;
    document
      .getElementById("saveToClosetBtn")
      .setAttribute("data-outfit-id", result.outfit_id);
    document.getElementById("saveToClosetBtn").disabled = false;
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
