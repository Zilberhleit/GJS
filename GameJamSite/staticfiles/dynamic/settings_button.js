window.addEventListener("DOMContentLoaded", function () {
  const settingsButton = document.querySelectorAll(".settings-button");
  console.log("sett btn");
  settingsButton.forEach((button) => {
    button.addEventListener("click", function (event) {
      event.stopPropagation();
      const menu = this.closest('[class^="post-settings-"]').querySelector(
        ".drop-menu",
      );

      document.querySelectorAll(".drop-menu").forEach((otherMenu) => {
        if (otherMenu !== menu) {
          otherMenu.style.display = "none";
        }
      });

      if (menu.style.display == "block") {
        menu.style.display = "none";
      } else {
        menu.style.display = "block";
      }
    });
  });

  document.addEventListener("click", function () {
    document.querySelectorAll(".drop-menu").forEach((menu) => {
      menu.style.display = "none";
    });
  });
});

window.addEventListener("DOMContentLoaded", function () {
  const settingsButton = document.querySelectorAll(".settings-button");
  console.log("sett btn");
  settingsButton.forEach((button) => {
    button.addEventListener("click", function (event) {
      event.stopPropagation();
      const menu = this.closest('[class^="comment-settings-"]').querySelector(
        ".drop-menu-comment",
      );

      document.querySelectorAll(".drop-menu").forEach((otherMenu) => {
        if (otherMenu !== menu) {
          otherMenu.style.display = "none";
        }
      });

      if (menu.style.display == "block") {
        menu.style.display = "none";
      } else {
        menu.style.display = "block";
      }
    });
  });

  document.addEventListener("click", function () {
    document.querySelectorAll(".drop-menu-comment").forEach((menu) => {
      menu.style.display = "none";
    });
  });
});
