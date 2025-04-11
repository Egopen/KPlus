document.addEventListener("DOMContentLoaded", function() {
    const analysisResult = localStorage.getItem("analysisResult");

    if (analysisResult) {
        document.querySelector(".main-content").innerHTML = analysisResult;
        localStorage.removeItem("analysisResult");
    } else {
        document.querySelector(".main-content").innerHTML = "<p>Результат не найден.</p>";
    }
});