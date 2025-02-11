function showDeleteButton() {
  const deleteButtons = document.querySelectorAll(".delete-button");
  deleteButtons.forEach((button) => {
    button.style.display =
      button.style.display === "none" || button.style.display === ""
        ? "block"
        : "none";
  });
}

function deleteOutfit(button) {
  const outfitId = button.getAttribute("data-id");

  if (!confirm("정말로 삭제하시겠습니까?")) {
    return;
  }

  const csrfToken = getCSRFToken();
  if (!csrfToken) {
    alert(
      "보안 문제로 인해 요청을 실행할 수 없습니다. 페이지를 새로고침 해주세요."
    );
    return;
  }

  fetch(`/delete-outfit/${outfitId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken, // CSRF 토큰 추가
      "Content-Type": "application/json",
    },
    body: JSON.stringify({}), // Django가 JSON을 올바르게 처리할 수 있도록 빈 객체라도 포함
  })
    .then((response) =>
      response.json().then((data) => ({ status: response.status, body: data }))
    )
    .then(({ status, body }) => {
      if (status === 200) {
        // 삭제 성공 시 해당 아이템을 화면에서 제거
        const outfitElement = document.getElementById(`outfit-${outfitId}`);
        if (outfitElement) {
          outfitElement.remove();
        }
        alert("옷이 성공적으로 삭제되었습니다.");
      } else {
        throw new Error(`삭제 실패: ${body.error}`);
      }
    })
    .catch((error) => {
      console.error("삭제 중 오류 발생:", error);
      alert(`서버 오류로 인해 삭제할 수 없습니다. ${error.message}`);
    });
}

// CSRF 토큰 가져오기 (Django 보안 적용)
function getCSRFToken() {
  const cookie = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="));

  if (!cookie) {
    console.error("CSRF 토큰을 찾을 수 없습니다.");
    return null;
  }

  return cookie.split("=")[1];
}
