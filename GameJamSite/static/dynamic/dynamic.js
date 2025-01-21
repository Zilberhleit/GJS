let currentQuestionID = 0;
    const questions = {{ poll_list_json|safe }};
    const questionField = document.querySelectorAll('.question');
    const questionText = document.querySelector('.question-text');
    console.log(questionField);

    if (questions.length != 0) {
        questionText.innerText = questions[currentQuestionID].question_text;
    }

    function change_question(answer){
        const formData = new FormData();
        formData.append('question_id', currentQuestionID+1);
        formData.append('answer', answer);

        fetch("{% url 'submit' poll_jam_uuid.uuid %}", {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Don't exist response");
            }
            return response.json();
        })
        .then(data => {
            if (data.question_id) {
                currentQuestionID += 1;
                if (currentQuestionID < questions.length) {
                    questionText.innerText = questions[currentQuestionID].question_text;
                }
            }
            else if (data.message) {
                alert(data.message);
                window.location.href = "{% url 'gamejam_detail' poll_jam_uuid.uuid %}";
            }
        });
    }