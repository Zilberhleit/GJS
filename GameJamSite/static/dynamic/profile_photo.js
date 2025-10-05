// Скрипт динамического обновления аватарки и шапки профиля
const imageInput = document.getElementById('avatar-input');
const hatInput = document.getElementById('hat-input');

const loadPhotoStatus = document.querySelector('.load-photo-status');
const uploadData = JSON.parse(document.getElementById('upload-data').textContent);
console.log(uploadData);
const url = uploadData.upload_url;

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

imageInput.addEventListener('change', function(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append('avatar_image', imageInput.files[0]);

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData
    })
        .then(response => response.json())
        .then(data => {      
            if (data.avatar){
                const avatarImg = document.getElementById('avatar-img');
                avatarImg.src = data.avatar;
            }
            loadPhotoStatus.textContent = data['message'];
        })
        .catch(error => console.error(error));
});

hatInput.addEventListener('change', function(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append('hat_image', hatInput.files[0]);

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.hat){
                const hatImg = document.getElementById('hat-img');
                hatImg.src = data.hat;
            }
            loadPhotoStatus.textContent = data['message'];
        })
        .catch(error => console.error(error));
});