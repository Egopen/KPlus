
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
    if (total > 4.4) {
      showCustomAlert("✅ Высокий коэффициент: " + total.toFixed(3));
    } else if (total < 3.2) {
      showCustomAlert("⚠️ Низкий коэффициент: " + total.toFixed(3));
    } else {
      showCustomAlert("🟡 Средний коэффициент: " + total.toFixed(3));
    }
  }

  function showCustomAlert(message) {
    document.getElementById("customAlertText").innerText = message;
    document.getElementById("customAlert").classList.remove("hidden");
  }
  
  function closeCustomAlert() {
    document.getElementById("customAlert").classList.add("hidden");
  }