document.addEventListener("DOMContentLoaded", () => {
    const resultsDiv = document.getElementById("results");
    const loadingDiv = document.getElementById("loading");

    // Show the loading spinner
    loadingDiv.style.display = "block";
    resultsDiv.innerHTML = ""; // Clear previous results

    fetch('/results_processed')
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            // Hide the loading spinner
            loadingDiv.style.display = "none";

            // Display the question asked
            const questionDiv = document.getElementById("question-asked");
            questionDiv.innerHTML = `
                <h2>Question Asked</h2>
                <p>${data.question}</p>
            `;

            // Display the abstract of the response
            const abstractDiv = document.getElementById("abstract-response");
            abstractDiv.innerHTML = `
                <h2>Abstract of Response</h2>
                <p>${data.abstract_response}</p>
            `;

            // Display the suggested improvements
            const improvementsDiv = document.getElementById("suggested-improvements");
            const improvementsList = data.suggested_improvements.map(improvement => `<li>${improvement}</li>`).join('');
            improvementsDiv.innerHTML = `
                <h2>Suggested Improvements</h2>
                <ul>${improvementsList}</ul>
            `;
        })
        .catch(error => {
            // Hide the loading spinner in case of error
            loadingDiv.style.display = "none";
            console.error("Error:", error);
            resultsDiv.innerHTML = "<p>An error occurred. Please try again later.</p>";
        });
});
