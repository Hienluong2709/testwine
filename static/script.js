document.getElementById("wine-form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    const resultList = document.querySelector("#results ul");
    resultList.innerHTML = "<li>Đang tính toán...</li>";

    try {
        const models = ['perceptron', 'logistic_regression', 'mlp'];
        const predictions = await Promise.all(models.map(async (model) => {
            const response = await fetch(`/predict/${model}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });
            return response.json();
        }));

        resultList.innerHTML = "";
        predictions.forEach((result, index) => {
            resultList.innerHTML += `<li>Chất lượng dự đoán (${models[index]}): ${result.prediction}</li>`;
        });
    } catch (error) {
        resultList.innerHTML = "<li>Có lỗi xảy ra khi dự đoán. Vui lòng thử lại.</li>";
        console.error('Error:', error);
    }
});
