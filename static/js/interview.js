document.addEventListener("DOMContentLoaded", () => {
    console.log("interview.js loaded"); // Debugging log
    const simulationResults = JSON.parse(sessionStorage.getItem("simulationResults"));
    console.log("Retrieved from sessionStorage:", simulationResults); // Debugging log

    const questionElement = document.getElementById("question");
    console.log("Question Element:", questionElement);
    if (!simulationResults) {
        questionElement.textContent = "Error: No interview data found.";
        return;
    }

    const recordButton = document.getElementById("recordButton");
    const submitButton = document.getElementById("submitButton");
    const loadingDiv = document.getElementById("loading");
    const resultsDiv = document.getElementById("results");
    let answers = [];
    let mediaRecorder;
    let audioChunks = [];

    // Function to start recording
    const startRecording = async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();

        mediaRecorder.addEventListener("dataavailable", event => {
            console.log("Data available", event.data);
            audioChunks.push(event.data);
        });

        mediaRecorder.addEventListener("stop", () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/mpeg' });
            audioChunks = [];
            return audioBlob;
        });
    };

    // Function to stop recording
    const stopRecording = () => {
        return new Promise(resolve => {
            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/mpeg' });
                audioChunks = [];
                console.log("Stop function", audioBlob);
                resolve(audioBlob);
            });
            mediaRecorder.stop();
        });
    };

    // Display the question from simulationResults
    let currentQuestionIndex = 0;

    const displayQuestion = () => {
        if (currentQuestionIndex < simulationResults.length) {
            questionElement.textContent = simulationResults[currentQuestionIndex];
            recordButton.style.display = "block";
            submitButton.style.display = "none";
        } else {
            questionElement.textContent = "Interview completed.";
            recordButton.style.display = "none";
            submitButton.style.display = "block";
        }
    };
    console.log("Total Questions:", simulationResults.length);
    console.log("Current Index:", currentQuestionIndex);
    console.log("First Question:", simulationResults[0]);
    console.log("Current Question:", simulationResults[currentQuestionIndex]); // Should NOT be undefined
    // Initial display of the first question
    displayQuestion();
    console.log("Current Question:", simulationResults[currentQuestionIndex]);

    // Event listener for the record button
    recordButton.addEventListener("click", async () => {
        if (recordButton.textContent === "Record Answer") {
            await startRecording();
            recordButton.textContent = "Stop Recording";
        } else {
            const audioBlob = await stopRecording();
            //const audioUrl = URL.createObjectURL(audioBlob);
            //const audioElement = document.createElement("audio");
            //audioElement.controls = true;
            //audioElement.src = audioUrl;
            //resultsDiv.appendChild(audioElement);
            answers.push({ question: simulationResults[currentQuestionIndex].text, audioBlob });
            currentQuestionIndex++;
            displayQuestion();
            recordButton.textContent = "Record Answer";
        }
    });

    // Event listener for the submit button
    submitButton.addEventListener("click", async () => {
        const formData = new FormData();
        answers.forEach((answer, index) => {
            formData.append(`audio-${index}`, answer.audioBlob, `answer-${index}.mp3`);
            formData.append(`question-${index}`, answer.question);
        });
        console.log("FormData:", formData);
        try {
            const response = await fetch('/results', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error("Failed to submit answers.");
            }

            const result = await response.json();
            //sessionStorage.setItem("interviewResults", JSON.stringify(result));
            window.location.href = 'results.html';
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    });
});
