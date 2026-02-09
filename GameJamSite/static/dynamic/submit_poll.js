let currentQuestionID = 0;
const questions = JSON.parse(document.getElementById('poll-list-json').textContent);
const questionField = document.querySelectorAll('.question');
const questionText = document.querySelector('.question-text');
const url = JSON.parse(document.getElementById('user-answers-data').textContent);

if (questions.length != 0) {
    questionText.innerText = questions[currentQuestionID].theme;
}

function change_question(answer){
    questions[currentQuestionID].decision = answer;

    currentQuestionID++;
    if (currentQuestionID >= questions.length) {
        send_answer_to_server();
    }
    else {
        questionText.innerText = questions[currentQuestionID].theme;
    }
}

function send_answer_to_server(){
    const formData = new FormData();
    formData.append('result', questions);
    fetch(url, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ result: questions })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Don't exist response");
        }
        return response.json();
    })
    .then(data => {
        if (data.message) {
            alert(data.message);
            window.location.href = "{% url 'gamejam_detail' poll_jam_uuid.uuid %}";
        }
    });
}