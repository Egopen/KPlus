document.addEventListener("DOMContentLoaded", () => {

        fetch("http://localhost:5295/Franchisto/Statistics/AddStatistics", {
            method: "PUT",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                statName: "Переход на страницу загрузки документа",
                count: 1
            }),
            keepalive: true
        }).catch(err => {
            console.error("Ошибка при отправке статистики:", err);
        });
    
});


function SendCheckDocStats(){
    fetch("http://localhost:5295/Franchisto/Statistics/AddStatistics", {
        method: "PUT",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            statName: "Использование загрузки документа",
            count: 1
        }),
        keepalive: true
    }).catch(err => {
        console.error("Ошибка при отправке статистики:", err);
    });
}