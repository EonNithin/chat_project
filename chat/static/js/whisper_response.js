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

document.getElementById('fileInput').addEventListener('change', function(event) {
    var file = event.target.files[0];
    console.log(file);
    if (file) {
        // Enable transcribe button if a file is selected
        document.getElementById('transcribeBtn').disabled = false;
    } else {
        // Disable transcribe button if no file is selected
        document.getElementById('transcribeBtn').disabled = true;
    }
});

var conversationHistory = document.getElementById('conversationHistory');

document.getElementById('transcribeBtn').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default form submission
    var file = document.getElementById('fileInput').files[0];
    if (file) {
        var formData = new FormData();
        formData.append('file', file);
        
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
            conversationHistory.innerHTML += '<div><strong>Response Text:</strong>' + data.response_text + '</div>'; 
            // Scroll to the bottom of the conversation history
            scrollToBottom();
            console.log(data);
        })
        .catch(error => console.error('Error:', error));
    }
});

