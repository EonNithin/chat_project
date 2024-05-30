function aiSpeechRecognitionPage(){
    window.location.href = '/ai_process/';
}

function autoResize(textarea) {
    textarea.style.height = "auto"; // Reset height to auto
    textarea.style.height = Math.min(textarea.scrollHeight, 100) + "px"; // Set height based on scrollHeight, limited to 300px
    console.log("auto resizing");
}

// Function to scroll to the end of the content inside a div
function scrollToBottom() {
    var conversationHistory = document.getElementById("chat-cardBody");
    conversationHistory.scrollTop = conversationHistory.scrollHeight;
    console.log("scrolling to bottom");
}


function startAnimation() {
    spinner.style.display = 'block';
}

function stopAnimation() {
    spinner.style.display = 'none';
}

document.getElementById('question').addEventListener('input', function() {
    autoResize(this);
});

document.getElementById('promptForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var question = document.getElementById('question').value;
    document.getElementById('conversationHistory').innerHTML += '<span style="color: red; font-weight: bold;">' + question + '</span><br>';
    setTimeout(scrollToBottom, 100);
    startAnimation(); // Start the animation
    var formData = new FormData(this);
    fetch('/generate_response/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('question').value = ''; // Clear input value
        stopAnimation(); // Stop the animation
        document.getElementById('conversationHistory').innerHTML += data.response + '<br><br><hr><hr>'; // Display response
        setTimeout(scrollToBottom, 100);
        console.log(data); 
    })
    .catch(error => console.error('Error:', error));
});
setTimeout(scrollToBottom, 100);