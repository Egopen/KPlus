document.addEventListener("DOMContentLoaded", () => {
        fetch("http://localhost:5295/Franchisto/Statistics/AddStatistics", {
            method: "PUT",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                statName: "Открытие формы калькулятора",
                count: 1
            }),
            keepalive: true
        }).catch(err => {
            console.error("Ошибка при отправке статистики:", err);
        });
});
function sendStats(){
    fetch("http://localhost:5295/Franchisto/Statistics/AddStatistics", {
        method: "PUT",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            statName: "Выполнен рассчет",
            count: 1
        }),
        keepalive: true
    }).catch(err => {
        console.error("Ошибка статистики рассчета калькулятора:", err);
    });
}
