function toggleNav() {
    var nav = document.getElementById("sideNav");
    nav.classList.toggle("open");
}

document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const uploadText = document.getElementById('uploadText');
    const fileNameSpan = document.getElementById('fileName');
    const preview = document.getElementById('preview');

    if (!uploadText || !fileNameSpan || !preview) return;

    if (file) {
        // Проверяем, что файл - это PDF
        if (file.type !== "application/pdf") {
            alert("Пожалуйста, загрузите только PDF-файл!");
            event.target.value = null; // Сброс input
            fileNameSpan.textContent = "Файл не выбран";
            uploadText.textContent = "Нажмите для загрузки";
            preview.style.display = 'none';
            return;
        }

        fileNameSpan.textContent = file.name;
        uploadText.textContent = "Файл загружен";

        // Вариант 1: Показываем иконку PDF
        //preview.src = "pdf-icon.png"; // Укажи путь к иконке PDF
        
        // Вариант 2: Показываем сам PDF в iframe
        preview.src = URL.createObjectURL(file);

        preview.style.display = 'block';
    } else {
        fileNameSpan.textContent = "Файл не выбран";
        uploadText.textContent = "Нажмите для загрузки";
        preview.style.display = 'none';
    }
});

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
