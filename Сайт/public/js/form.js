
function calculate() {
    const names = ["location", "network", "budget", "metro", "competitors"];
    let total = 0;

    for (let name of names) {
      const selected = document.querySelector(`input[name="${name}"]:checked`);
      if (!selected) {
        alert("Пожалуйста, выберите вариант для всех вопросов.");
        return;
      }
      total += parseFloat(selected.value);
    }
    sendStats()
    if (total > 4) {
      alert("✅ Высокий коэффициент: " + total.toFixed(3));
    } else if (total < 3) {
      alert("⚠️ Низкий коэффициент: " + total.toFixed(3));
    } else {
      alert("🟡 Средний коэффициент: " + total.toFixed(3));
    }
  }