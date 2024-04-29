// Function to scroll to the end of the content inside a div
function scrollToBottom() {
    var conversationHistory = document.getElementById("cardBody");
    conversationHistory.scrollTop = conversationHistory.scrollHeight;
    console.log("scrolling to bottom");
}

var spinner = document.getElementById('spinner');

function startAnimation() {
    spinner.style.display = 'block';
}

function stopAnimation() {
    spinner.style.display = 'none';
}

var conversationHistory = document.getElementById('conversationHistory');

document.getElementById('fetchLatestBtn').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default button behavior

    // Call the transcribe_mp3 function via AJAX
    try {
        var formData = new FormData();
        
        // Add the CSRF token to the FormData
        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        formData.append('csrfmiddlewaretoken', csrfToken);
        
        conversationHistory.innerHTML='';

        scrollToBottom();
        startAnimation(); // Start the animation
        
        fetch('/transcribe_mp3/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            stopAnimation();
            //conversationHistory.innerHTML += '<div><strong>Transcribed Text:</strong><br> <span style="color: navy;">' + data.transcribed_text + '</span></div>';
            conversationHistory.innerHTML += '<div><strong>Summary:</strong><br>' + data.response_text + '<br></div><br>'; 
            conversationHistory.innerHTML += '<div><strong>Quiz Questions:</strong><br>' + data.quiz_question + '<br></div><br>'; 
            // Scroll to the bottom of the conversation history
            scrollToBottom();
            console.log(data);
        })
        .catch(error => console.error('Error:', error));
    } catch (error) {
        console.error('Error:', error);
    }
});

