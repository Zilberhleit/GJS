const container = document.getElementById('circle-container');
    for (let i = 0; i < 4; i++) {
        console.log("aaaa" + i);
        div = document.createElement('div');
        div.className = 'circle';
        container.appendChild(div);
    }

    const circles = document.querySelectorAll('.circle');

    container.addEventListener('mousemove', (e) => {
        const rect = container.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        circles.forEach(circle => {
            const circleRect = circle.getBoundingClientRect();
            const circleX = circleRect.left + circleRect.width / 2;
            const circleY = circleRect.top + circleRect.height / 2;

            const dx = circleX - e.clientX;
            const dy = circleY - e.clientY;

            // Нормализуем вектор и умножаем на дистанцию
            const distance = Math.sqrt(dx * dx + dy * dy);
            const moveX = (dx / distance) * 20;
            const moveY = (dy / distance) * 20;

            circle.style.transform = `translate(${moveX}px, ${moveY}px)`;
        });
    });

    container.addEventListener('mouseleave', () => {
        circles.forEach(circle => {
            circle.style.transform = 'translate(0, 0)';
        });
    });