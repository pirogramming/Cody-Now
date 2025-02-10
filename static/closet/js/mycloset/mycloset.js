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
