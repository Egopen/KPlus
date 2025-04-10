document.addEventListener("DOMContentLoaded", () => {
    const listElement = document.getElementById("list");
    const searchInput = document.getElementById("search-input");
    const searchButton = document.getElementById("search-button");
    searchButton.addEventListener("click", () => {
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
      const query = searchInput.value.trim();
    
        if (query) {
          window.location.href = `/articles_search?query=${encodeURIComponent(query)}&page=1`;
        }
      });
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get("query");
    const page = urlParams.get("page") || 1;
   
    if (!query) {
      listElement.innerHTML = "<li>Параметр 'query' отсутствует в URL.</li>";
      return;
    }
  
    const API_URL = `http://localhost:8080/Franchisto/Docs/SearchByQuery?query=${encodeURIComponent(query)}&page=${page}`;
  
    fetch(API_URL)
      .then((res) => res.json())
      .then((data) => {
        if (!data || data.length === 0) {
          listElement.innerHTML = "<li>Ничего не найдено.</li>";
          return;
        }
  
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
        listElement.innerHTML = "<li>Ошибка при загрузке данных.</li>";
      });
  });
  