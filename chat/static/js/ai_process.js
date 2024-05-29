function aiChatPage(){
    window.location.href = '/ai_chatpage/';
}

var spinner = document.getElementById('spinner');

function startAnimation() {
    spinner.style.display = 'block';
}

function stopAnimation() {
    spinner.style.display = 'none';
}

function aiProcessLatestRecordedFile() {
    const aiProcessLatestfile = document.getElementById('ai-process-latest-file');
    const mp3LatestFileIcon = document.getElementById('mp3-file-icon');
    const tabsContainer = document.getElementById('tabs-container');
    //const btn1BelowCard = document.getElementById('btn1-below-card');
    //const btn2BelowCard = document.getElementById('btn2-below-card');

    //btn1BelowCard.style.display = 'none';
    //btn2BelowCard.style.display = 'none';

    startAnimation();

    // Fetch the latest MP3 file path
    fetch('/transcribe_mp3/')
        .then(response => response.json())
        .then(data => {
            stopAnimation();
            aiProcessLatestfile.style.display = 'none';
            mp3LatestFileIcon.style.display = 'block';
            tabsContainer.style.display = 'block';
            // Print response in console
            console.log('audio_url:', data.latest_file);
            console.log('Summary:', data.response_text);
            console.log('Quiz Questions:', data.quiz_question);

            // Add summary and quiz questions to corresponding divs
            document.getElementById('class-summary').innerHTML = formatSummary(data.response_text);
            document.getElementById('quiz-questions').innerHTML = formatQuizQuestions(data.quiz_question);
        })
        .catch(error => console.error('Error:', error));

}

// Function to format the summary text
function formatSummary(summary) {
    return summary.replace(/\n/g, '<br>');
}

// Function to format the quiz questions text
function formatQuizQuestions(quizQuestions) {
    let formattedQuestions = '';
    const questionBlocks = quizQuestions.split('\n\n'); // Split by double newlines for each question block

    questionBlocks.forEach(block => {
        if (block.trim() !== '') {
            // Find the position of the answer and split accordingly
            const answerIndex = block.lastIndexOf('Answer:');
            if (answerIndex !== -1) {
                const questionPart = block.slice(0, answerIndex).trim();
                const answerPart = block.slice(answerIndex).trim();

                formattedQuestions += `
                    <div class="quiz-question">
                        <p>${questionPart.replace(/\n/g, '<br>')}</p>
                        <p><strong>${answerPart.replace(/\n/g, '<br>')}</strong></p>
                    </div>
                    <hr>
                `;
            } else {
                formattedQuestions += `
                    <div class="quiz-question">
                        <p>${block.replace(/\n/g, '<br>')}</p>
                    </div>
                    <hr>
                `;
            }
        }
    });

    return formattedQuestions;
}

function chooseFileToAIProcess() {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'audio/mp3'; // Accept only MP3 files
    
    // Event listener for when a file is selected
    fileInput.addEventListener('change', function(event) {
        const selectedFile = event.target.files[0];
        
        // Check if a file is selected
        if (selectedFile) {
            const fileURL = URL.createObjectURL(selectedFile);
            // Process the file as needed
            console.log('Selected file:', selectedFile.name);
            // Perform any additional processing or uploading here
        }
    });
    
    // Trigger the file input click event
    fileInput.click();
}