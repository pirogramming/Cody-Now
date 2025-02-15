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
  const overlay = document.getElementById("category-slide-overlay"); // 배경 요소 가져오기
  if (!slideCategoryContainer) {
    console.error("Error: Slider element not found!");
    return;
  }
  slideCategoryContainer.style.display = "flex";
  overlay.style.display = "block"; // 배경 활성화
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
  const overlay = document.getElementById("category-slide-overlay"); // 배경 요소 가져오기
  slideCategoryContainer.classList.remove("show-slide");
  setTimeout(() => {
    slideCategoryContainer.style.display = "none"; // 닫을 때 완전히 숨김
    overlay.style.display = "none"; // 배경 활성화
  }, 300); // 애니메이션 시간과 동일하게 설정
}

// ✅ CSRF 토큰 가져오기 함수
function getCsrfToken() {
  return document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="))
    ?.split("=")[1];
}

function loadCategories() {
  const categoryList = document.getElementById("category-list");
  const url = categoryList.getAttribute("data-url"); // ✅ HTML에서 API URL 가져오기
  const deleteImgSrc = categoryList.getAttribute("data-delete-img"); // ✅ 삭제 버튼 이미지 경로 가져오기

  fetch(url) // Django 뷰 호출
    .then((response) => {
      if (!response.ok) {
        throw new Error("서버 응답 오류");
      }
      return response.json();
    })
    .then((data) => {
      categoryList.innerHTML = ""; // 기존 목록 초기화

      if (data.categories.length > 0) {
        data.categories.forEach((category) => {
          const categoryDiv = document.createElement("div");
          categoryDiv.classList.add("category-item");
          categoryDiv.setAttribute("data-id", category.id);
          categoryDiv.innerHTML = `
            <label>
              <input type="checkbox" name="category" value="${category.id}" />
              <span class="category-name">${category.name}</span>
            </label>
            <img class="delete-category-btn" src="${deleteImgSrc}" />
          `;
          categoryList.appendChild(categoryDiv);
        });
      } else {
        categoryList.innerHTML =
          '<p id="no-category-message">등록된 카테고리가 없습니다.</p>';
      }
    })
    .catch((error) => console.error("카테고리 불러오기 실패:", error));
}

// ✅ 카테고리 추가 기능
document
  .getElementById("addCategoryBtn")
  .addEventListener("click", function () {
    const categoryName = document.getElementById("new_category").value.trim();
    const url = this.getAttribute("data-url"); // ✅ URL을 HTML에서 가져옴

    if (!categoryName) {
      alert("카테고리 이름을 입력하세요.");
      return;
    }

    fetch(url, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCsrfToken(),
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name: categoryName }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          loadCategories();
          document.getElementById("new_category").value = "";
        } else {
          alert(data.error);
        }
      })
      .catch((error) => console.error("카테고리 추가 실패:", error));
  });

// ✅ 카테고리 삭제 기능 (이벤트 위임 방식)
document
  .getElementById("category-list")
  .addEventListener("click", function (event) {
    if (event.target.classList.contains("delete-category-btn")) {
      const categoryDiv = event.target.closest(".category-item");
      const categoryId = categoryDiv.getAttribute("data-id");
      const deleteUrl = document
        .getElementById("category-list")
        .getAttribute("data-delete-url"); // ✅ HTML에서 URL 가져오기

      if (!confirm("정말 이 카테고리를 삭제하시겠습니까?")) return;

      fetch(deleteUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCsrfToken(),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ category_id: categoryId }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("서버 응답 오류");
          }
          return response.json();
        })
        .then((data) => {
          if (data.success) {
            alert("카테고리가 삭제되었습니다!");
            loadCategories(); // ✅ 카테고리 목록 다시 불러오기
          } else {
            alert(data.error);
          }
        })
        .catch((error) => console.error("카테고리 삭제 실패:", error));
    }
  });

// ✅ "나만의 옷장에 저장하기" 버튼 클릭 이벤트
document
  .getElementById("saveToClosetBtn-category")
  .addEventListener("click", function () {
    let outfitId = this.getAttribute("data-outfit-id");
    let saveUrl = this.getAttribute("data-url"); // ✅ HTML에서 URL 가져오기

    if (!outfitId) {
      alert("먼저 이미지를 업로드하세요!");
      return;
    }

    let selectedCategories = [];
    document
      .querySelectorAll("input[name='category']:checked")
      .forEach((checkbox) => {
        selectedCategories.push(checkbox.value);
      });

    if (selectedCategories.length === 0) {
      alert("최소 한 개의 카테고리를 선택해주세요!");
      return;
    }

    fetch(saveUrl, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCsrfToken(),
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        outfit_id: outfitId,
        category_ids: selectedCategories,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("서버 응답 오류");
        }
        return response.json();
      })
      .then((data) => {
        if (data.success) {
          alert(data.message);
          closeSlide();
        } else {
          alert(data.error);
        }
      })
      .catch((error) => console.error("오류:", error));
  });

// ✅ 페이지 로드 시 카테고리 불러오기 실행
document.addEventListener("DOMContentLoaded", loadCategories);
