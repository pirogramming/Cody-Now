function showInput() {
  const categoryInputs = document.querySelectorAll(".category-add");
  categoryInputs.forEach((input) => {
    if (input.style.display === "none" || input.style.display === "") {
      input.style.display = "block";
    } else {
      input.style.display = "none";
    }
  });
}

function showDelete() {
  const deleteButtons = document.querySelectorAll(".delete-category-btn");
  deleteButtons.forEach((button) => {
    if (button.style.display === "none" || button.style.display === "") {
      button.style.display = "block";
    } else {
      button.style.display = "none";
    }
  });
}

function openSlide() {
  const slideCategoryContainer = document.getElementById(
    "show-category-slider"
  );
  if (!slideCategoryContainer) {
    console.error("Error: Slider element not found!");
    return;
  }
  slideCategoryContainer.style.display = "flex";
  setTimeout(() => {
    slideCategoryContainer.classList.add("show-slide");
  }, 10);
}

// ✅ openSlide()를 전역 객체(window)에 등록
window.openSlide = openSlide;

function closeSlide() {
  const slideCategoryContainer = document.getElementById(
    "show-category-slider"
  );
  slideCategoryContainer.classList.remove("show-slide");
  setTimeout(() => {
    slideCategoryContainer.style.display = "none"; // 닫을 때 완전히 숨김
  }, 300); // 애니메이션 시간과 동일하게 설정
}
