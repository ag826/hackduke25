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

                // Display what worked
                const workedDiv = document.createElement("div");
                workedDiv.innerHTML = `
                    <ul>
                        <li><strong><em>What worked?</em></strong>
                            <ul>
                            <li>${result.what_worked}</li>
                            </ul>
                        </li>
                    </ul>
                `;
                resultContainer.appendChild(workedDiv);

                // Display what could have been improved
                const improveDiv = document.createElement("div");
                improveDiv.innerHTML = `
                    <ul>
                        <li><strong><em>What could have been improved?</em></strong>
                            <ul>
                            <li>${result.what_improve}</li>
                            </ul>
                        </li>
                    </ul>
                `;
                resultContainer.appendChild(improveDiv);

                // Display sample answer
                const sampleDiv = document.createElement("div");
                sampleDiv.innerHTML = `
                    <ul>
                        <li><strong><em>Given your background, what would an alternate answer have looked like?</em></strong>
                            <ul>
                            <li>${result.alt_answer}</li>
                            </ul>
                        </li>
                    </ul>                
                `;

                resultContainer.appendChild(sampleDiv);

                // Display overall score
                const scoreDiv = document.createElement("div");
                scoreDiv.innerHTML = `
                    <ul>
                        <li><strong><em>Overall Score: ${result.alt_answer} </em></strong>
                        </li>
                    </ul> 
                `;
                resultContainer.appendChild(scoreDiv);

                // Display what could have been improved
                const criteriaDiv = document.createElement("div");
                criteriaDiv.innerHTML = `
                    <ul>
                        <li><em>Grading Criteria: ${result.criteria} </em>
                        </li>
                    </ul>
                `;
                resultContainer.appendChild(criteriaDiv);


                // // Display the suggested improvements
                // const improvementsDiv = document.createElement("div");
                // const improvementsList = result.suggested_improvements.map(improvement => `<li>${improvement}</li>`).join('');
                // improvementsDiv.innerHTML = `
                //     <h3>Feedback on your responses:</h3>
                //     <ul>${improvementsList}</ul>
                // `;
                // resultContainer.appendChild(improvementsDiv);

                // Append the result container to the results div
                resultsDiv.appendChild(resultContainer);
            });
        } else {
            resultsDiv.innerHTML = "<p>No interview results found. Please try again later.</p>";
        }
    }, 1000); // Simulate a 1 second delay
});
