const followButton = document.getElementById("subs");
const unfollowButton = document.getElementById("unsubs");
const followData = JSON.parse(
  document.getElementById("follow-data").textContent,
);

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const follow_csrftoken = getCookie("csrftoken");

followButton.addEventListener("click", function (event) {
  event.preventDefault();

  console.log(followButton.value);
  const formData = new FormData();
  formData.append("follow_user_id", followButton.value);

  // fetch
});
