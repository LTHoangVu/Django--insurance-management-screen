document
  .querySelectorAll(".cls-dropdown-menu-container")
  .forEach((dropdown) => {
    const dropdownContent = dropdown.querySelector(".cls-dropdown-menu");
    const container = dropdown.querySelector(".cls-data-container");

    if (!container.dataset.clickAttached) {
      container.dataset.clickAttached = "true";
      container.addEventListener("click", () => {
        console.log("Dropdown clicked:", dropdown);
        dropdownContent.classList.toggle("show");
      });

      dropdown.querySelectorAll(".cls-option").forEach((item) => {
        item.addEventListener("click", () => {
          console.log("item clicked:", item);
          const id = item.querySelector(".cls-number-data").textContent;
          const value = item.querySelector(".cls-type-data").textContent;
          dropdown.querySelector(".cls-txt-id-number").value = id;
          dropdown.querySelector(".cls-txt-name").textContent = value;
          dropdownContent.classList.remove("show");
        });
      });
    }

    window.addEventListener("click", function (e) {
      if (
        !dropdownContent.contains(e.target) &&
        !container.contains(e.target)
      ) {
        dropdownContent.classList.remove("show");
      }
    });
  });
