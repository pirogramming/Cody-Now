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
function deleteOutfit(button) {
  const outfitId = button.getAttribute("data-id");
  if (!confirm("정말로 삭제하시겠습니까?")) {
    return;
  }

  fetch(`/delete-outfit/${outfitId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCSRFToken(), // CSRF 토큰 추가
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`서버 응답 오류: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      if (data.message) {
        // 삭제 성공 시 해당 아이템을 화면에서 제거
        const outfitElement = document.getElementById(`outfit-${outfitId}`);
        if (outfitElement) {
          outfitElement.remove();
        }
        alert("옷이 성공적으로 삭제되었습니다.");
      } else if (data.error) {
        alert(`삭제 실패: ${data.error}`);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("서버 오류 발생. 콘솔에서 오류를 확인하세요.");
    });
}

// CSRF 토큰 가져오기 (Django 보안 적용)
function getCSRFToken() {
  return document
    .querySelector("meta[name='csrf-token']")
    .getAttribute("content");
}
