document.addEventListener("DOMContentLoaded", () => {
    const contentDiv = document.getElementById("content");
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get("id");
  
    if (!id) {
      contentDiv.innerHTML = "<p>Ошибка: Параметр 'id' не найден в URL.</p>";
      return; 
    }
    fetch("http://localhost:5295/Franchisto/Statistics/AddStatistics", {
      method: "PUT",
      headers: {
          "Accept": "application/json",
          "Content-Type": "application/json"
      },
      body: JSON.stringify({
          statName: "Переход на страницу документа из поиска",
          count: 1
      }),
      keepalive: true
  }).catch(err => {
      console.error("Ошибка при отправке статистики:", err);
  });
    let startTime = Date.now();
    
    const API_URL = `http://localhost:5295/Franchisto/Docs/GetDocById?id=${id}`;
    
    fetch(API_URL)
      .then((res) => {
        if (!res.ok) throw new Error(`Ошибка сервера: ${res.status}`);
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
        contentDiv.innerHTML = "<p>Не удалось загрузить документ.</p>";
      });
  
    window.addEventListener("beforeunload", () => {
      const endTime = Date.now();
      const secondsSpent = Math.floor((endTime - startTime) / 1000);
  
      fetch("http://localhost:5295/Franchisto/Statistics/AddStatisticsToDocs", {
        method: "PUT",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          id,
          spenttime: secondsSpent
        }),
        keepalive: true
      });
    });
  });
  