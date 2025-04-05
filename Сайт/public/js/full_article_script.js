document.addEventListener("DOMContentLoaded", () => {
  const contentDiv = document.getElementById("content");

  const urlParams = new URLSearchParams(window.location.search);
  const id = urlParams.get("id");

  if (!id) {
      contentDiv.innerHTML = "<p>Ошибка: Параметр 'id' не найден в URL.</p>";
      return; 
  }
  const API_URL = `http://localhost:5295/Franchisto/Docs/GetDocById?id=${id}`;
  fetch(API_URL)
      .then((res) => {
          if (!res.ok) {
              throw new Error(`Ошибка сервера: ${res.status}`);
          }
          return res.json();
      })
      .then((data) => {
          if (!data || !data.content) {
              contentDiv.innerHTML = "<p>Ошибка: Неверный формат данных от сервера.</p>";
              return;
          }
          const cleanedContent = data.content.replace(/[\n\r]+/g, " ");
          contentDiv.innerHTML = cleanedContent;
      })
      .catch((err) => {
          contentDiv.innerHTML = "<p>Не удалось загрузить риск.</p>";
      });
});
