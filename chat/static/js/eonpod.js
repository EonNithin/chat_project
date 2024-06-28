// Connect to OBS WebSocket server
const obs = new OBSWebSocket();
let isConnected = false;
let isRecording = false;
let isStreaming = false;

async function connectToOBS() {
    try {
        await obs.connect('ws://0.0.0.0:4459', 'AJ8MIYdZZJV7rLXA'); // Connect OBS
        isConnected = true;
        await updateRecordingButton();
        await updateStreamingButton();
        console.log('Connected to OBS Studio');
    } catch (error) {
        console.error('Failed to connect to OBS Studio:', error);
        alert('Failed to connect to OBS Studio, OBS Studio app needs to be opened. Load page again after OBS app is opened');
    }
}

async function disconnectFromOBS() {
    try {
        await obs.disconnect(); // disconnect OBS
        isConnected = false;
        console.log('Disconnected from OBS Studio');
    } catch (error) {
        console.error('Failed to disconnect from OBS Studio:', error);
    }
}

// Automatically connect to OBS on page load
document.addEventListener("DOMContentLoaded", async () => {
    await connectToOBS();
});

// Automatically disconnect from OBS on page unload
//window.addEventListener("beforeunload", async () => {
//    await disconnectFromOBS();
//});

// Function to toggle recording state
async function toggleRecording() {
    const startRecordButton = document.getElementById("startRecord");
    const stopRecordButton = document.getElementById("stopRecord");
    const textLabelRecord = document.getElementById("text-label-record");
    const progressBar = document.getElementById("progress-bar1");

    if (isRecording) {
        // Stop recording
        try {
            await obs.call('StopRecord');
            console.log('Stopped recording');
            sendRecordingStatus(false);
            startRecordButton.style.display = "block";
            stopRecordButton.style.display = "none";
            textLabelRecord.textContent = "Start Recording";
            progressBar.style.visibility = "hidden"; // Hide progress bar
            progressBar.style.width = "0%"; // Reset progress bar
            isRecording = false;
            
        // Call a function to convert saved mp4 recording file to mp3 file
        fetch('/convert_mp4_to_mp3/')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('MP3 file path is:', data.mp3_filepath);
                    // You can now use the mp3_filepath variable as needed
                } else {
                    console.error('Error converting MP4 to MP3:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
            
        } catch (error) {
            console.error('Failed to stop recording:', error);
            alert('Failed to stop recording. Please refresh page and check your connection to OBS Studio');
        }
    } else {
        // Start recording
        try {
            await obs.call('StartRecord');
            console.log('Started recording');
            sendRecordingStatus(true);
            startRecordButton.style.display = "none";
            stopRecordButton.style.display = "block";
            textLabelRecord.textContent = "Stop Recording";
            progressBar.style.visibility = "visible"; // Show progress bar
            isRecording = true;
        } catch (error) {
            console.error('Failed to start recording:', error);
            alert('Failed to start recording. Please refresh page and check you are connected to OBS Studio');
        }
    }
}

async function updateRecordingButton() {
    try {
        const response = await obs.call("GetRecordStatus");
        isRecording = response.outputActive;
        console.log(response);
        console.log(isRecording);
        if(isRecording){
            sendRecordingStatus(true);
        }
        else{
            sendRecordingStatus(false);
        }
        const startRecordButton = document.getElementById('startRecord');
        const stopRecordButton = document.getElementById('stopRecord');
        const textLabelRecord = document.getElementById("text-label-record");
        const progressBar = document.getElementById("progress-bar1");
        if (isRecording) {
            startRecordButton.style.display = 'none';
            stopRecordButton.style.display = 'block';
            textLabelRecord.textContent = 'Stop Recording';
            progressBar.style.visibility = "visible"; 
        } else {
            startRecordButton.style.display = 'block';
            stopRecordButton.style.display = 'none';
            textLabelRecord.textContent = 'Start Recording';
            progressBar.style.visibility = "hidden"; 
        }
    } catch (error) {
        console.error('Failed to get recording status:', error);
    }
}

function sendRecordingStatus(status) {
    fetch('/update_recording_status/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is sent with the request
        },
        body: JSON.stringify({is_recording: status})
    }).then(response => {
        if (!response.ok) {
            console.error('Failed to update recording status on server');
        }
    }).catch(error => {
        console.error('Error in sending recording status:', error);
    });
}

// Function to get the CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function toggleStreaming(){
    const startStreamButton = document.getElementById("startStream");
    const stopStreamButton = document.getElementById("stopStream");
    const textLabelRecord = document.getElementById("text-label-stream");
    const progressBar = document.getElementById("progress-bar2");

    if (isStreaming) {
        // Stop Streaming
        try {
            await obs.call('StopStream');
            console.log('Stopped Streaming');
            sendStreamingStatus(false);
            startStreamButton.style.display = "block";
            stopStreamButton.style.display = "none";
            textLabelRecord.textContent = "Start Streaming";
            progressBar.style.visibility = "hidden"; // Hide progress bar
            progressBar.style.width = "0%"; // Reset progress bar
            isStreaming = false;
        } catch (error) {
            console.error('Failed to stop streaming:', error);
            alert('Failed to stop streaming. Please refresh page and check your connection to OBS Studio');
        }
    } else {
        // Start Streaming
        try {
            await obs.call('StartStream');
            console.log('Started Streaming');
            sendStreamingStatus(true);
            startStreamButton.style.display = "none";
            stopStreamButton.style.display = "block";
            textLabelRecord.textContent = "Stop Streaming";
            progressBar.style.visibility = "visible"; // Show progress bar
            isStreaming = true;
        } catch (error) {
            console.error('Failed to start streaming:', error);
            alert('Failed to start streaming. Please refresh page and check you are connected to OBS Studio');
        }
    }
}

async function updateStreamingButton() {
    try {
        const response = await obs.call("GetStreamStatus");
        isStreaming = response.outputActive;
        console.log(response);
        console.log(isStreaming);
        if(isStreaming){
            sendStreamingStatus(true);
        }
        else{
            sendStreamingStatus(false);
        }
        
        const startStreamButton = document.getElementById('startStream');
        const stopStreamButton = document.getElementById('stopStream');
        const textLabelRecord = document.getElementById("text-label-stream");
        const progressBar = document.getElementById("progress-bar2");
        if (isStreaming) {
            startStreamButton.style.display = 'none';
            stopStreamButton.style.display = 'block';
            textLabelRecord.textContent = 'Stop Streaming';
            progressBar.style.visibility = "visible"; 
        } else {
            startStreamButton.style.display = 'block';
            stopStreamButton.style.display = 'none';
            textLabelRecord.textContent = 'Start Streaming';
            progressBar.style.visibility = "hidden"; 
        }
    } catch (error) {
        console.error('Failed to get streaming status:', error);
    }
}

function sendStreamingStatus(status) {
    fetch('/update_streaming_status/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is sent with the request
        },
        body: JSON.stringify({is_streaming: status})
    }).then(response => {
        if (!response.ok) {
            console.error('Failed to update streaming status on server');
        }
    }).catch(error => {
        console.error('Error in sending streaming status:', error);
    });
}

// Function to get the CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function aiProcessing(){
    window.location.href = '/ai_process/';
}

function toggleDropdown() {
    document.getElementById("dropdown-content").classList.toggle("show");
}

function selectOption(option) {
    const dropdownLabel = document.getElementById("dropdown-label").children[0];
    if (dropdownLabel) {
        dropdownLabel.textContent = option;
    } else {
        console.error('Dropdown label element not found.');
    }
    document.getElementById("dropdown-content").classList.remove("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.custom-dropdown-label') && !event.target.matches('.custom-dropdown-label *')) {
        const dropdowns = document.getElementsByClassName("dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
            const openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

// Pass the latest file path to JavaScript
function playLatestRecording() {
    fetch('/get_latest_mp4_filepath/', {
      method: 'GET' // Use GET to retrieve data
    })
    .then(response => response.json())
    .then(data => {
      const latestFilePath = data.latest_file;
      if (latestFilePath) {
        console.log(latestFilePath);
        const videoElement = document.getElementById("videoPlayer");
        console.log(videoElement);
        videoElement.src = latestFilePath; // Set the src attribute to the media URL
        console.log("video source: " + videoElement.src);
        videoPlayer.load();
        videoElement.play();
        console.log("video source play: " + videoElement.play());
      } else {
        console.error("No recording found");
      }
    })
    .catch(error => {
      console.error("Error fetching latest recording:", error);
    });
}


// Function to handle file selection
function chooseFileToPlay() {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'video/mp4'; // Accept only MP4 files

    // Event listener for when a file is selected
    fileInput.addEventListener('change', function(event) {
        const selectedFile = event.target.files[0];
        const videoPlayer = document.getElementById('videoPlayer');
        
        // Check if a file is selected
        if (selectedFile) {
            const fileURL = URL.createObjectURL(selectedFile);
            // Update the src attribute of the video element with the selected file's URL
            videoPlayer.src = fileURL;

            // Load and play the video
            videoPlayer.load();
            videoPlayer.play();
        }
    });

    // Trigger the file input click event
    fileInput.click();
}

function showSettings(){
    console.log("clicked settings icon");
    const settings = document.getElementById('settings');
    if (settings.style.display === 'none' || settings.style.display === '') {
        settings.style.display = 'block';
    } else {
        settings.style.display = 'none';
    }
}

document.addEventListener('click', function(event) {
    const gearIcon = document.getElementById('gear-icon');
    const settings = document.getElementById('settings');
    if (!gearIcon.contains(event.target)) {
        settings.style.display = 'none';
    }
});

// Function to request full screen mode
function requestFullScreen() {
    const elem = document.documentElement;
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.mozRequestFullScreen) { /* Firefox */
        elem.mozRequestFullScreen();
    } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
        elem.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
    } else if (elem.msRequestFullscreen) { /* IE/Edge */
        elem.msRequestFullscreen();
    }
}

// Function to request exit full screen mode
function exitFullScreen() {
    const elem = document;
    if (elem.exitFullscreen) {
        elem.exitFullscreen();
    } else if (elem.mozCancelFullScreen) { /* Firefox */
        elem.mozCancelFullScreen();
    } else if (elem.webkitExitFullscreen) { /* Chrome, Safari and Opera */
        elem.webkitExitFullscreen();
    } else if (elem.msExitFullscreen) { /* IE/Edge */
        elem.msExitFullscreen();
    }
}

document.addEventListener("DOMContentLoaded", function() {
// Assuming a button with ID "fullscreenButton" triggers full screen mode
    const fullscreenButton = document.getElementById("fullscreenButton");
    const fullscreenExitButton = document.getElementById("fullscreenExitButton");

    if (fullscreenButton) {
        fullscreenButton.addEventListener("click", function() {
            fullscreenButton.style.display = 'none'
            fullscreenExitButton.style.display = 'block'
            requestFullScreen();
        });  
    }

    if (fullscreenExitButton) {
        fullscreenExitButton.addEventListener("click", function() {
            fullscreenButton.style.display = 'block'
            fullscreenExitButton.style.display = 'none'
            exitFullScreen();
        });  
    }
});