// Допилить
const followButton = document.getElementById("subs");
const unfollowButton = document.getElementById("unsubs");
const followData = JSON.parse(
  document.getElementById("follow-data").textContent,
);
const followUrl = followData.follow_url;
const unfollowUrl = followData.unfollow_url;

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

if (followButton) {
  followButton.addEventListener("click", function (event) {
    event.preventDefault();

    console.log(followButton.value);
    const formData = new FormData();
    formData.append("follow_user_name", followButton.value);

    fetch(followUrl, {
      method: "POST",
      headers: {
        "X-CSRFToken": follow_csrftoken,
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "ok") {
          location.reload();
        } else {
          console.error(data.message);
        }
      })
      .catch((error) => console.error(error));
  });
} else if (unfollowButton) {
  const unfollow_csrftoken = getCookie("csrftoken");
  unfollowButton.addEventListener("click", function (event) {
    event.preventDefault();

    const unfollow_formData = new FormData();
    unfollow_formData.append("follow_user_name", unfollowButton.value);

    fetch(unfollowUrl, {
      method: "POST",
      headers: {
        "X-CSRFToken": unfollow_csrftoken,
      },
      body: unfollow_formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status == "ok") {
          location.reload();
        } else {
          console.error(data.message);
        }
      })
      .catch((error) => console.error(error));
  });
}
