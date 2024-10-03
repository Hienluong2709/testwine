document.getElementById("wine-form").addEventListener("submit", async function (event) {
    event.preventDefault();
  
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
  
    const response = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
  
    const result = await response.json();
  
    const resultList = document.querySelector("#results ul");
    resultList.innerHTML = "";
    resultList.innerHTML = `<li>Chất lượng dự đoán: ${result.prediction}</li>`;
  });
  