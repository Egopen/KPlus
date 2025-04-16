document.getElementById('fileInput').addEventListener('change', async function(event) {
    const file = event.target.files[0];
    const uploadText = document.getElementById('uploadText');
    const fileNameSpan = document.getElementById('fileName');

    if (!uploadText || !fileNameSpan ) return;

    if (file) {
        if (file.type !== "application/pdf") {
            alert("Пожалуйста, загрузите только PDF-файл!");
            event.target.value = null;  
            uploadText.textContent = "Нажмите для загрузки";
            preview.style.display = 'none';
            return;
        }

        uploadText.textContent = "Файл обрабатывается моделью...";
        fileInput.disabled = true;
        const formData = new FormData();
        formData.append("file", file);

        console.log("Отправка файла:", file.name);

        try {
            const response = await fetch("http://localhost:8081/api/analyze", {
                method: "POST",
                body: formData,
            });
        
            console.log("Response status:", response.status);
        
            if (!response.ok) {
                throw new Error("Ошибка анализа: " + response.statusText);
            }
        
            const html = await response.text();
            console.log("Ответ от сервера:", html);
        
            localStorage.setItem("analysisResult", html);
            window.location.href = "/doc_analysis";
        
        } catch (error) {
            event.target.value = null;
            console.error("Ошибка при отправке:", error);
            alert("Не удалось отправить файл: " + error.message);
            fileInput.disabled = flase;
            uploadText.textContent = "Нажмите для загрузки";
        }
    } else {
        fileInput.disabled = flase;
        event.target.value = null;
        uploadText.textContent = "Нажмите для загрузки";
        preview.style.display = 'none';
    }
});
