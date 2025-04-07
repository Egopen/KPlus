document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('.open-form-button');

    if (button) {
        button.addEventListener('click', async () => {
            console.log("Кнопка нажата");
            try {
                const response = await fetch('http://localhost:8000/open_form/');
                const data = await response.json();
                alert(data.message);
            } catch (error) {
                console.error('Ошибка при открытии формы:', error);
                alert('Ошибка при попытке открыть форму');
            }
        });
    } else {
        console.error("Кнопка не найдена на странице");
    }
});
