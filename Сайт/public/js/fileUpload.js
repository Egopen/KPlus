document.getElementById('fileInput').addEventListener('change', async function(event) {
    const file = event.target.files[0];
    const uploadText = document.getElementById('uploadText');
    const fileNameSpan = document.getElementById('fileName');
    const preview = document.getElementById('preview');

    if (!uploadText || !fileNameSpan || !preview) return;

    if (file) {
        if (file.type !== "application/pdf") {
            alert("Пожалуйста, загрузите только PDF-файл!");
            event.target.value = null;  // Сбросить input
            fileNameSpan.textContent = "Файл не выбран";
            uploadText.textContent = "Нажмите для загрузки";
            preview.style.display = 'none';
            return;
        }

        // Обновляем текст и показываем превью
        fileNameSpan.textContent = file.name;
        uploadText.textContent = "Файл загружен";
        preview.src = URL.createObjectURL(file);
        preview.style.display = 'block';

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("http://localhost:8081/api/analyze", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error("Ошибка анализа: " + response.statusText);
            }

            const html = await response.text();

            localStorage.setItem("analysisResult", html);

           
            window.location.href = "/doc_analysis";  

        } catch (error) {
            console.error("Ошибка при отправке:", error);
            alert("Не удалось отправить файл: " + error.message);
        }
    } else {
        fileNameSpan.textContent = "Файл не выбран";
        uploadText.textContent = "Нажмите для загрузки";
        preview.style.display = 'none';
    }
});
