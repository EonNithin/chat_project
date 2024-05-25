// Connect to OBS WebSocket server
const obs = new OBSWebSocket();
let isConnected = false;
let isRecording = false;
let isStreaming = false;

async function connectToOBS() {
    try {
        await obs.connect('ws://0.0.0.0:4455', '654321'); // Connect OBS
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
window.addEventListener("beforeunload", async () => {
    await disconnectFromOBS();
});

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
            startRecordButton.style.display = "block";
            stopRecordButton.style.display = "none";
            textLabelRecord.textContent = "Start Recording";
            progressBar.style.visibility = "hidden"; // Hide progress bar
            progressBar.style.width = "0%"; // Reset progress bar
            isRecording = false;
        } catch (error) {
            console.error('Failed to stop recording:', error);
            alert('Failed to stop recording. Please refresh page and check your connection to OBS Studio');
        }
    } else {
        // Start recording
        try {
            await obs.call('StartRecord');
            console.log('Started recording');
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

async function toggleStreaming(){
    const startStreamButton = document.getElementById("startStream");
    const stopStreamButton = document.getElementById("stopStream");
    const textLabelRecord = document.getElementById("text-label-stream");
    const progressBar = document.getElementById("progress-bar2");

    if (isStreaming) {
        // Stop recording
        try {
            await obs.call('StopStream');
            console.log('Stopped Streaming');
            startStreamButton.style.display = "block";
            stopStreamButton.style.display = "none";
            textLabelRecord.textContent = "Start Recording";
            progressBar.style.visibility = "hidden"; // Hide progress bar
            progressBar.style.width = "0%"; // Reset progress bar
            isStreaming = false;
        } catch (error) {
            console.error('Failed to stop streaming:', error);
            alert('Failed to stop streaming. Please refresh page and check your connection to OBS Studio');
        }
    } else {
        // Start recording
        try {
            await obs.call('StartStream');
            console.log('Started Streaming');
            startStreamButton.style.display = "none";
            stopStreamButton.style.display = "block";
            textLabelRecord.textContent = "Stop Recording";
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
