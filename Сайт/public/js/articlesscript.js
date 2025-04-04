document.addEventListener("DOMContentLoaded", () => {
    const API_URL = "http://localhost:5295/Franchisto/Docs/GetStartDocs";
    const listElement = document.getElementById("list");
    const searchInput = document.getElementById("search-input");
    const searchButton = document.getElementById("search-button");
  
    searchButton.addEventListener("click", () => {
      const query = searchInput.value.trim();
  
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
          link.setAttribute("href", `http://localhost:5295/Franchisto/Docs/View?id=${risk.id}`);
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
  