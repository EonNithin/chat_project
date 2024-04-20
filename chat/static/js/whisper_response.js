// Function to scroll to the end of the content inside a div
function scrollToBottom() {
    var conversationHistory = document.getElementById("cardBody");
    conversationHistory.scrollTop = conversationHistory.scrollHeight;
    console.log("scrolling to bottom");
}

var dotsAnimation = document.getElementById('wave');
function startAnimation() {
    dotsAnimation.style.display = 'inline'; // Make the animation visible
}

function stopAnimation() {
    dotsAnimation.style.display = 'none';
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
document.getElementById('transcribeBtn').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default form submission
    var file = document.getElementById('fileInput').files[0];
    if (file) {
        var formData = new FormData();
        formData.append('file', file);
        
        // Add the CSRF token to the FormData
        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        formData.append('csrfmiddlewaretoken', csrfToken);

        fetch('/transcribe_mp3/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response data
            console.log(data);
        })
        .catch(error => console.error('Error:', error));
    }
});

