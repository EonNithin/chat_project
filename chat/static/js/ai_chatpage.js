function aiSpeechRecognitionPage(){
    window.location.href = '/ai_process/';
}

// Function to scroll to the end of the content inside a div
function scrollToBottom() {
    var conversationHistory = document.getElementById("conversationHistory");
    conversationHistory.scrollTop = conversationHistory.scrollHeight;
    console.log("scrolling to bottom");
}

// function autoResize(textarea) {
//     textarea.style.height = "auto"; // Reset height to auto
//     textarea.style.height = Math.min(textarea.scrollHeight, 100) + "px"; // Set height based on scrollHeight, limited to 100px
// }

// document.getElementById('question').addEventListener('input', function() {
//     autoResize(this);
// });

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
    document.getElementById('conversationHistory').innerHTML += '<span style="color: red; font-weight: bold; font-size:30px">' + question + '</span><br>';
    setTimeout(scrollToBottom, 100);
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
        document.getElementById('conversationHistory').innerHTML += '<span style="color: black; font-size:30px">' + data.response + '</span><br><hr>';
        setTimeout(scrollToBottom, 100);
    })
    .catch(error => console.error('Error:', error));
});
