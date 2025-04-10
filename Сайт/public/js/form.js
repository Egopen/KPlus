
function calculate() {
    const names = ["location", "network", "budget", "metro", "competitors"];
    let total = 0;

    for (let name of names) {
      const selected = document.querySelector(`input[name="${name}"]:checked`);
      if (!selected) {
        alert("У вас есть незаполненные поля. Пожалуйста, заполните форму полностью.");
        return;
      }
      total += parseFloat(selected.value);
    }
    sendStats()

    const maxScore = 6.207;
    const percent = (total / maxScore) * 100 - 1;
    const coefficient = (total-0.01) / maxScore;
    const percentStr = percent.toFixed(1) + "%";
    if (percent > 71) {
      showCustomAlert("✅ Высокий коэффициент: " + percentStr, "#28a745");
    } else if (percent < 51) {
      showCustomAlert("⚠️ Низкий коэффициент: " + percentStr, "#dc3545");
    } else {
      showCustomAlert("🟡 Средний коэффициент: " + percentStr, "#ffc107");
    }
    setTimeout(() => showExplanationAlert(coefficient), 1000);
}

  function showCustomAlert(message, color = "#333") {
    let alertBox = document.createElement("div");
    alertBox.textContent = message;
    alertBox.style.position = "fixed";
    alertBox.style.top = "20px";
    alertBox.style.right = "20px";
    alertBox.style.padding = "15px 25px";
    alertBox.style.backgroundColor = color;
    alertBox.style.color = "white";
    alertBox.style.fontSize = "16px";
    alertBox.style.borderRadius = "8px";
    alertBox.style.boxShadow = "0 4px 12px rgba(0, 0, 0, 0.3)";
    alertBox.style.opacity = "0";
    alertBox.style.transition = "opacity 0.5s ease, transform 0.5s ease";
    alertBox.style.zIndex = "9999";
    alertBox.style.transform = "translateY(-20px)";
  
    document.body.appendChild(alertBox);
  
    // Trigger animation
    requestAnimationFrame(() => {
      alertBox.style.opacity = "1";
      alertBox.style.transform = "translateY(0)";
    });
  
    // Remove after 4 seconds
    setTimeout(() => {
      alertBox.style.opacity = "0";
      alertBox.style.transform = "translateY(-20px)";
      setTimeout(() => document.body.removeChild(alertBox), 900);
    }, 5000);
  }

  function showExplanationAlert(coefficient) {
    let explanation = "";
    let color = "";
  
    if (coefficient >= 0.01 && coefficient <= 0.509) {
      explanation = `
  Если Ваш процент в диапазоне от 1% до 50,9% – низкая экономическая эффективность
  
  Обоснование:
  Наш калькулятор показывает расчет от 1% до 100%, где 1% – это низкая экономическая эффективность, а 100% – высокая.
  Исходя из предоставленных Вами данных, предполагаемые доходы от использования франшизы значительно ниже совокупных затрат, которые Вы потратите на открытие киберспортивного клуба.
  Полученный коэффициент говорит о низкой рентабельности проекта и высоких рисках окупаемости.
      `;
      color = "#dc3545"; // красный
    } else if (coefficient >= 0.51 && coefficient <= 0.71) {
      explanation = `
  Если Ваш процент в диапазоне от 51% до 71% — умеренная экономическая эффективность
  
  Обоснование:
  Наш калькулятор показывает расчет от 1% до 100%, где 1% – это низкая экономическая эффективность, а 100% – высокая.
  Исходя из предоставленных Вами данных Вы находитесь в приемлемом диапазоне, при котором проект имеет шансы на окупаемость, но остается уязвимым к колебаниям доходов и затрат.
  Это означает, что прибыль от бизнеса покрывает расходы частично, и для достижения устойчивой выгоды необходимо провести более детальный анализ, чтобы оценить риски и потенциал дальнейшего увеличения выгоды.
      `;
      color = "#ffc107"; // жёлтый
    } else if (coefficient > 0.71 && coefficient <= 1) {
      explanation = `
  Если Ваш процент в диапазоне от 71% до 100%  — высокая экономическая эффективность
  
  Обоснование:
  Наш калькулятор показывает расчет от 1% до 100%, где 1% – это низкая экономическая эффективность, а 100% – высокая.
  Исходя из предоставленных Вами данных Ваш проект демонстрирует высокую вероятность финансовой устойчивости и способность покрыть все основные издержки в рамках существующих условий договора.
  Полученная информация свидетельствует о высокой вероятности успешного внедрения и окупаемости проекта.
      `;
      color = "#28a745"; // зелёный
    } else {
      return; // если значение вне диапазона — не показываем
    }
  
    const alertBox = document.createElement("div");
    alertBox.textContent = explanation;
    alertBox.style.whiteSpace = "pre-line";
    alertBox.style.position = "fixed";
    alertBox.style.top = "80px";
    alertBox.style.right = "20px";
    alertBox.style.padding = "20px";
    alertBox.style.backgroundColor = color;
    alertBox.style.color = "white";
    alertBox.style.fontSize = "15px";
    alertBox.style.borderRadius = "10px";
    alertBox.style.boxShadow = "0 4px 15px rgba(0, 0, 0, 0.4)";
    alertBox.style.maxWidth = "400px";
    alertBox.style.zIndex = "10000";
    alertBox.style.opacity = "0";
    alertBox.style.transition = "opacity 0.5s ease, transform 0.5s ease";
    alertBox.style.transform = "translateY(-20px)";
  
    document.body.appendChild(alertBox);
  
    requestAnimationFrame(() => {
      alertBox.style.opacity = "1";
      alertBox.style.transform = "translateY(0)";
    });
  
    setTimeout(() => {
      alertBox.style.opacity = "0";
      alertBox.style.transform = "translateY(-20px)";
      setTimeout(() => document.body.removeChild(alertBox), 12000);
    }, 15000);
  }
  