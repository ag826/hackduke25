document.addEventListener("DOMContentLoaded", () => {
    const resultsDiv = document.getElementById("results");
    const loadingDiv = document.getElementById("loading");
    const interviewResults = JSON.parse(sessionStorage.getItem("interviewResults")); // Array of answers

    // Show the loading spinner
    loadingDiv.style.display = "block";
    resultsDiv.innerHTML = ""; // Clear previous results

    // Simulate a delay to show the loading spinner
    setTimeout(() => {
        // Hide the loading spinner
        loadingDiv.style.display = "none";

        if (interviewResults && interviewResults.length > 0) {
            interviewResults.forEach((result, index) => {
                // Create a container for each question and answer
                const resultContainer = document.createElement("div");
                resultContainer.classList.add("result-container");

                // Display the question asked
                const questionDiv = document.createElement("div");
                questionDiv.innerHTML = `
                    <h2>Question ${index + 1}</h2>
                    <p>${result.question}</p>
                `;
                resultContainer.appendChild(questionDiv);

                // Display the abstract of the response
                const abstractDiv = document.createElement("div");
                abstractDiv.innerHTML = `
                    <h2>Abstract of Response</h2>
                    <p>${result.abstract_response}</p>
                `;
                resultContainer.appendChild(abstractDiv);

                // Display the suggested improvements
                const improvementsDiv = document.createElement("div");
                const improvementsList = result.suggested_improvements.map(improvement => `<li>${improvement}</li>`).join('');
                improvementsDiv.innerHTML = `
                    <h2>Suggested Improvements</h2>
                    <ul>${improvementsList}</ul>
                `;
                resultContainer.appendChild(improvementsDiv);

                // Append the result container to the results div
                resultsDiv.appendChild(resultContainer);
            });
        } else {
            resultsDiv.innerHTML = "<p>No interview results found. Please try again later.</p>";
        }
    }, 1000); // Simulate a 1 second delay
});
