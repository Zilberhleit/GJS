function disable_poll_button(button, answer){
    const container = button.closest('.question-container');
    const yesButton = container.querySelector('.yes-button');
    const noButton = container.querySelector('.no-button');
    if (answer === 'yes') {
        yesButton.disabled = true;
        noButton.disabled = false;
    } else {
        yesButton.disabled = false;
        noButton.disabled = true;
    }
}