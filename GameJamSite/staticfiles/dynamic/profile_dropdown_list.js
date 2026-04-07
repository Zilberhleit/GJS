//Выпадающий список
window.addEventListener('DOMContentLoaded', (event) => {
    document.querySelectorAll('.user_games').forEach(card => {
        card.addEventListener('click', function(event) {
            console.log("Clicked:", this); // Проверяем, срабатывает ли клик
            if (event.target === this || event.target.tagName === 'H5') {
                this.classList.toggle('open');
            }
            console.log("Class list:", this.classList); // Проверяем, меняется ли класс
        });
    });
});