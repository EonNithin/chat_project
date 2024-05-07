 // Connect to OBS WebSocket server
 const obs = new OBSWebSocket();

 let isConnected = false;

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

 async function disconnectToOBS() {
     try {
         await obs.disconnect(); // disconnect OBS
         isConnected = false;
         console.log('Disconnected to OBS Studio');
     } catch (error) {
         console.error('Failed to disconnect to OBS Studio:', error);
     }
 }

 let isRecording = false;

 // Add event listener to a user-initiated event (e.g., click) to trigger full screen mode
 document.addEventListener("DOMContentLoaded", async () => {
     await connectToOBS(); // Automatically connect to OBS on page load
 });

 // Event listener for start recording button click
 document.getElementById('recordButton').addEventListener('click', () => {
     toggleRecording(); // Toggle recording state
 });

 document.getElementById('stopButton').addEventListener('click', () => {
     toggleRecording();
 }
 );

 // Function to toggle recording state
 function toggleRecording() {
     if (isRecording) {
         stopRecording();
     } else {
         startRecording();
     }
 }

 // Function to start recording in OBS
 async function startRecording() {
     try {
         await obs.call('StartRecord');
         console.log('Started recording');
         // Update button style
         document.getElementById('recordButton').style.display = 'none';
         document.getElementById('stopButton').style.display = 'block';  
         isRecording = true;
     } catch (error) {
         console.error('Failed to start recording:', error);
         alert('Failed to start recording, Please refresh page and check you are connected to OBS Studio');
     }
 }

 // Function to stop recording in OBS
 async function stopRecording() {
     try {
         await obs.call('StopRecord');
         // Redirect to a new page
         //window.location.href = 'http://127.0.0.1:8000/whisper_response/';
         // Open the URL in a new tab
     window.open('http://127.0.0.1:8000/whisper_response/', '_blank');

         console.log('Stopped recording');
         // Update button style
         document.getElementById('recordButton').style.display = 'block';
         document.getElementById('stopButton').style.display = 'none';
         isRecording = false;
     } catch (error) {
         console.error('Failed to stop recording:', error);
         alert('Failed to stop recording. Please refresh page and Check your connection to OBS Studio');
     }
 }
 
 async function updateRecordingButton() {
     try {
         const response = await obs.call("GetRecordStatus");
         isRecording = response.outputActive;
         console.log(response);
         console.log(isRecording);
         const recordButton = document.getElementById('recordButton');
         const stopButton = document.getElementById('stopButton');
         if (isRecording) {
             recordButton.style.display = 'none';
             stopButton.style.display = 'block';
         } else {
             recordButton.style.display = 'block';
             stopButton.style.display = 'none';
         }
     } catch (error) {
         console.error('Failed to get recording status:', error);
     }
 }
 
 let isStreaming = false;

 // Event listener for start stream button click
 document.getElementById('startStreamButton').addEventListener('click', async () => {
     toggleStreaming(); // Toggle streaming state
 });
 
 // Event listener for start stream button click
 document.getElementById('stopStreamButton').addEventListener('click', async () => {
     toggleStreaming(); // Toggle streaming state
 });

 // Function to toggle streaming state
 function toggleStreaming() {
     if (isStreaming) {
         stopStreaming();
     } else {    
         startStreaming();
     }
 }

 // Function to start streaming in OBS
 async function startStreaming() {
     try {
         await obs.call('StartStream');
         console.log('Started streaming');
         // Update button style
         document.getElementById('startStreamButton').style.display = 'none';
         document.getElementById('stopStreamButton').style.display = 'block';
         isStreaming = true;
     } catch (error) {
         console.error('Failed to start streaming:', error);
         alert('Failed to start streaming, Please refresh page and check you are connected to OBS Studio');
     }
 }

 // Function to stop streaming in OBS
 async function stopStreaming() {
     try {
         await obs.call('StopStream');
         console.log('Stopped streaming');
         // Update button style
         document.getElementById('startStreamButton').style.display = 'block';
         document.getElementById('stopStreamButton').style.display = 'none';
         isStreaming = false;
     } catch (error) {
         console.error('Failed to stop streaming:', error);
         alert('Failed to stop streaming, Please refresh page and check your connection to OBS Studio');
     }
 }

 async function updateStreamingButton() {
     try {
         const streamresponse = await obs.call("GetStreamStatus");
         isStreaming = streamresponse.outputActive;
         console.log(streamresponse);
         console.log(isStreaming);
         const startButton = document.getElementById('startStreamButton');
         const stopButton = document.getElementById('stopStreamButton');

         if (isStreaming) {
             startButton.style.display = 'none';
             stopButton.style.display = 'block';
         } else {
             startButton.style.display = 'block';
             stopButton.style.display = 'none';
         }
     } catch (error) {
         console.error('Failed to get streaming status:', error);
     }
 }

 // Get the file input element
 var fileInput = document.getElementById('fileInput');
 // Get the video player element
 var videoPlayer = document.getElementById('videoPlayer');

 // Listen for changes in the file input element
 fileInput.addEventListener('change', function() {
     // Get the selected file
     var file = fileInput.files[0];
     // Create a URL for the selected file
     var videoURL = URL.createObjectURL(file);
     // Set the source of the video player to the selected file
     videoPlayer.src = videoURL;
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
 if (fullscreenButton) {
     fullscreenButton.addEventListener("click", function() {
         requestFullScreen();
     });
 }

 // Assuming a button with ID "fullscreenExitButton" triggers exit full screen mode
 const fullscreenExitButton = document.getElementById("fullscreenExitButton");
 if (fullscreenExitButton) {
     fullscreenExitButton.addEventListener("click", function() {
         exitFullScreen();
     });
 }
 });