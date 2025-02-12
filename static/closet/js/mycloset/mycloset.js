function showDeleteButton() {
  const deleteButton = document.querySelectorAll(".delete-button");
  deleteButton.forEach((input) => {
    // 현재 display 상태를 확인하여 반대로 설정
    if (input.style.display === "none" || input.style.display === "") {
      input.style.display = "block";
    } else {
      input.style.display = "none";
    }
  });
}

document
  .querySelector(".category-container")
  .addEventListener("click", function (event) {
    if (event.target.closest(".delete-button")) {
      var categoryDiv = event.target.closest(".category-wrapper"); // ✅ `.category-wrapper`에서 찾기
      console.log("찾은 카테고리 요소:", categoryDiv); // ✅ categoryDiv가 올바르게 선택되었는지 확인

      if (!categoryDiv) {
        console.error(
          "❌ categoryDiv가 null입니다. .category-wrapper를 찾을 수 없습니다."
        );
        return;
      }

      var categoryId = categoryDiv.getAttribute("data-id"); // ✅ `data-id` 가져오기
      console.log("카테고리 ID:", categoryId); // ✅ 값이 올바르게 나오는지 확인

      if (!categoryId) {
        console.error("❌ 카테고리 ID를 찾을 수 없습니다.");
        return;
      }

      if (!confirm("정말 이 카테고리를 삭제하시겠습니까?")) return;

      fetch("/delete-category/", {
        method: "POST",
        headers: {
          "X-CSRFToken": getCsrfToken(),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ category_id: categoryId }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("서버 오류: " + response.status);
          }
          return response.json();
        })
        .then((data) => {
          if (data.success) {
            alert("카테고리가 삭제되었습니다!");
            categoryDiv.remove(); // ✅ `.category-wrapper` 삭제
          } else {
            alert("오류 발생: " + data.error);
          }
        })
        .catch((error) => console.error("카테고리 삭제 실패:", error));
    }
  });

function getCsrfToken() {
  return document
    .querySelector("meta[name='csrf-token']")
    .getAttribute("content");
}
