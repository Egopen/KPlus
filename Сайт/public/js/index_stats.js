document.addEventListener("DOMContentLoaded", () => {
    const cookies = document.cookie.split(";");
    let flag = true;

    for (let cookie of cookies) {
        if (cookie.trim().startsWith("is_first_visit=false")) {
            flag = false;
            break;
        }
    }

    if (flag) {
        document.cookie = "is_first_visit=false";

        fetch("http://localhost:5295/Franchisto/Statistics/AddStatistics", {
            method: "PUT",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                statName: "Вход на сайт",
                count: 1
            }),
            keepalive: true
        }).catch(err => {
            console.error("Ошибка при отправке статистики:", err);
        });
    }
});
function handleChecklistClick() {
    fetch("http://localhost:5295/Franchisto/Statistics/AddStatistics", {
        method: "PUT",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            statName: "Открыт чек-лист",
            count: 1
        }),
        keepalive: true
    }).catch(err => {
        console.error("Ошибка статистики чек-листа:", err);
    });
    window.open('./docs/чек-лист.pdf', '_blank');
}
