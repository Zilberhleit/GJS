let currentQuestionID = 0;
const questions = document.querySelectorAll('.question-container');

if (questions.length > 0) {
    questions[currentQuestionID].style.display = 'block';
} else {
    console.error('Нет доступных вопросов');
}

function change_question(questionID, answer){
    const formData = new FormData();
    formData.append('question_id', questionID);
    formData.append('answer', answer);

    fetch(submitUrl, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        }
    })
    .then(response => {
        if (response.ok) {
            questions[currentQuestionID].style.display = 'none';
            questionID++;
            if (questionID < question.length){
                questions[questionID].style.display = 'block';
            }
            else {
                alert('ok'); //вместо ок, должна быть отправка игрока на участие в джеме
            }
        } else {
            console.error('Ошибка при отправке ответа');
        }
    })
}