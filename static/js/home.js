document.addEventListener("DOMContentLoaded", () => {
    const interviewForm = document.getElementById("interview-form");
    const positionInput = document.getElementById("position");
    const companyInput = document.getElementById("company");
    const jobDescriptionInput = document.getElementById("job-description");
    const resumeInput = document.getElementById("resume");
    const resultsDiv = document.getElementById("results");
    const loadingDiv = document.getElementById("loading");
    const profileInput = document.getElementById("profile-type");

    // Event listener for the interview form
    interviewForm.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent form from submitting normally

        const position = positionInput.value.trim();
        const company = companyInput.value.trim();
        const jobDescription = jobDescriptionInput.value.trim();
        const resume = resumeInput.files[0];
        const profile=profileInput.value.trim()

        if (!position || !company || !jobDescription || !resume || !profile) {
            resultsDiv.innerHTML = "<p class='text-danger'>Please fill in all fields and upload your resume.</p>";
            return;
        }

        // Show the loading spinner
        loadingDiv.style.display = "block";
        resultsDiv.innerHTML = ""; // Clear previous results

        const formData = new FormData();
        formData.append("position", position);
        formData.append("company", company);
        formData.append("jobDescription", jobDescription);
        formData.append("resume", resume);
        formData.append("profile_type", profile);

        try {
            // Send the form data to the simulate API
            const response = await fetch('/simulate', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error("Failed to simulate interview.");
            }

            const simulationResults = await response.json();

            // Hide the loading spinner
            loadingDiv.style.display = "none";

            sessionStorage.setItem("simulationResults", JSON.stringify(simulationResults));
            console.log(sessionStorage.getItem("simulationResults"));
            // Redirect to the interview page
            window.location.href = "/interview";
        } catch (error) {
            // Hide the loading spinner if there's an error
            loadingDiv.style.display = "none";
            resultsDiv.innerHTML = `<p class='text-danger'>Error: ${error.message}</p>`;
        }
    });
});
