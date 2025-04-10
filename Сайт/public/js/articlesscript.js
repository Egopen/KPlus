document.addEventListener("DOMContentLoaded", () => {
    const API_URL = "http://localhost:8080/Franchisto/Docs/GetStartDocs";
    const listElement = document.getElementById("list");
    const searchInput = document.getElementById("search-input");
    const searchButton = document.getElementById("search-button");
    fetch("http://localhost:8080/Franchisto/Statistics/AddStatistics", {
      method: "PUT",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        statName: "Вход на страницу с документами",
        count: 1
      }),
      keepalive: true
    }).catch(err => {
      console.error("Ошибка при отправке статистики:", err);
    });
    searchButton.addEventListener("click", () => {
      const query = searchInput.value.trim();
      fetch("http://localhost:8080/Franchisto/Statistics/AddStatistics", {
        method: "PUT",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          statName: "Использование поиска",
          count: 1
        }),
        keepalive: true
      }).catch(err => {
        console.error("Ошибка при отправке статистики:", err);
      });
      if (query) {
        window.location.href = `/articles_search?query=${encodeURIComponent(query)}&page=1`;
      }
    });
    fetch(API_URL)
      .then((res) => res.json())
      .then((data) => {
        data.forEach((risk) => {
          const li = document.createElement("li");
          const link = document.createElement("a");
          link.textContent = risk.title;
          link.setAttribute("href", `http://localhost:3000/article?id=${risk.id}`);
          li.appendChild(link);
          li.setAttribute("data-id", risk.id);
          listElement.appendChild(li);
        });
      })
      .catch((err) => {
        console.error("Ошибка загрузки рисков:", err);
        listElement.innerHTML = "<li>Не удалось загрузить риски.</li>";
      });
  });
  