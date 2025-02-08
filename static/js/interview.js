document.addEventListener("DOMContentLoaded", () => {
    const simulationResults = JSON.parse(sessionStorage.getItem("simulationResults"));
    if (!simulationResults) {
        questionElement.textContent = "Error: No interview data found.";
        return;
    }

    questionElement.textContent = simulationResults.first_question;

    // TO DO

    const recordButton = document.getElementById("recordButton");
    const submitButton = document.getElementById("submitButton");
    const questionElement = document.getElementById("question");
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
                resolve(audioBlob);
            });
            mediaRecorder.stop();
        });
    };

    // Fetch and display the question
    const fetchQuestion = async () => {
        try {
            const response = await fetch('/get_question');
            if (!response.ok) {
                throw new Error("Failed to fetch question.");
            }
            const question = await response.json();
            questionElement.textContent = question.text;
        } catch (error) {
            questionElement.textContent = `Error: ${error.message}`;
        }
    };

    // Event listener for the record button
    recordButton.addEventListener("click", async () => {
        if (recordButton.textContent === "Record Answer") {
            await startRecording();
            recordButton.textContent = "Stop Recording";
        } else {
            const audioBlob = await stopRecording();
            const audioUrl = URL.createObjectURL(audioBlob);
            const audioElement = document.createElement("audio");
            audioElement.controls = true;
            audioElement.src = audioUrl;
            resultsDiv.appendChild(audioElement);
            recordButton.style.display = "none";
            submitButton.style.display = "block";
            answers.push({ audioBlob });
        }
    });

    // Event listener for the submit button
    submitButton.addEventListener("click", async () => {
        const formData = new FormData();
        answers.forEach((answer, index) => {
            formData.append(`audio-${index}`, answer.audioBlob, `answer-${index}.mp3`);
        });

        try {
            const response = await fetch('/process_response', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error("Failed to submit answers.");
            }

            const result = await response.json();
            window.location.href = 'results.html';
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    });

    // Initial fetch of the question
    fetchQuestion();
});
