function aiSpeechRecognitionPage(){
    window.location.href = '/ai_process/';
}

function autoResize(textarea) {
    textarea.style.height = "auto"; // Reset height to auto
    textarea.style.height = Math.min(textarea.scrollHeight, 100) + "px"; // Set height based on scrollHeight, limited to 300px
    console.log("auto resizing");
}

document.getElementById('question').addEventListener('input', function() {
    autoResize(this);
});

var dotsAnimation = document.getElementById('wave');
function startAnimation() {
    dotsAnimation.style.display = 'inline'; // Make the animation visible
}

function stopAnimation() {
    dotsAnimation.style.display = 'none';
}

document.getElementById('promptForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    var question = document.getElementById('question').value;
    document.getElementById('conversationHistory').innerHTML += '<span style="color: red; font-weight: bold;">' + question + '</span><br>';
    //setTimeout(scrollToBottom, 100);
    startAnimation();
    const formData = new FormData(this);
    fetch('/generate_response/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('question').value = ''; // Clear input value
        stopAnimation();
        console.log('Question:', data.question);
        console.log('Response:', data.response);
        // Display response on the page
        document.getElementById('conversationHistory').innerHTML += data.response + '<br><br><hr><hr>'; // Display response
        //setTimeout(scrollToBottom, 100);

    })
    .catch(error => console.error('Error:', error));
});
