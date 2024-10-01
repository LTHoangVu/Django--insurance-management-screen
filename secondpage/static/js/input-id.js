const personIDInput = document.getElementById("personID");
const personLink = document.getElementById("personLink");

// Khi người dùng gõ vào ô input, cập nhật href của thẻ a
personIDInput.addEventListener("input", function () {
  const personID = personIDInput.value; // Lấy giá trị personID từ input
  personLink.href = `{% url 'secondpage' %}?personID=${personID}`; // Cập nhật URL với personID
});
