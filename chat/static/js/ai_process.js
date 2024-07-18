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

// Function to format the summary text
function formatSummary(summary) {
    return summary.replace(/\n/g, '<br>');
}

// Function to format the quiz questions text
function formatQuizQuestions(quizQuestions) {
    let formattedQuestions = '';
    const questionBlocks = quizQuestions.split('\n\n'); // Split by double newlines for each question block
  
    questionBlocks.forEach((block) => {
      if (block.trim() !== '') {
        let formattedBlock = ''; // Initialize an empty string to store the formatted block
  
        const lines = block.split('\n'); // Split the block into lines
  
        lines.forEach((line) => {
          if (line.startsWith('Answer:')) { // Check if the line starts with "Answer:"
            formattedBlock += `<hr><strong>${line.trim()}</strong><hr>\n`; // Add bold formatting and newline
          } else {
            formattedBlock += `${line.trim()}\n`; // Add the line without formatting and newline
          }
        });
  
        formattedQuestions += `
          <div class="quiz-question">
            <p>${formattedBlock.replace(/\n/g, '<br>')}</p>
          </div>
        `;
      }
    });
    return formattedQuestions;
}

function aiProcessLatestRecordedFile() {
    const aiProcessLatestfile = document.getElementById('ai-process-latest-file');
    const mp3LatestFileIcon = document.getElementById('mp3-file-icon');
    const tabsContainer = document.getElementById('tabs-container');
    const myTabContent = document.getElementById('myTabContent');
    
    aiProcessLatestfile.style.display = 'none';
    mp3LatestFileIcon.style.display = 'block';

    startAnimation();

    // Fetch the latest MP3 file path
    fetch('/transcribe_mp3/')
        .then(response => response.json())
        .then(data => {
            stopAnimation();
            tabsContainer.style.display = 'block';
            myTabContent.style.display = 'block';

            console.log("entered transcribed_mp3 fetch")
            console.log(data)

            // Add summary and quiz questions to corresponding divs
            document.getElementById('transcription-content').innerHTML = formatSummary(data.transcribed_text);
            document.getElementById('class-summary-content').innerHTML = formatSummary(data.response_text);
        })
        .catch(error => {
            console.error('Error:', error)
            // Stop animation
            stopAnimation();
        });
}

function chooseFileToAIProcess() {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'audio/mp3'; // Accept only MP3 files
    
    const aiProcessLatestfile = document.getElementById('ai-process-latest-file');
    const mp3LatestFileIcon = document.getElementById('mp3-file-icon');
    const tabsContainer = document.getElementById('tabs-container');
    const myTabContent = document.getElementById('myTabContent');

    aiProcessLatestfile.style.display = 'none';
    mp3LatestFileIcon.style.display = 'block';

    // Event listener for when a file is selected
    fileInput.addEventListener('change', function(event) {
        const selectedFile = event.target.files[0];
        console.log("Selected file is:"+selectedFile)

        // Check if a file is selected
        if (selectedFile) {
            const formData = new FormData();
            formData.append('file', selectedFile);

            // Display the selected file name
            console.log('Selected file:', selectedFile.name);
            
            // Start animation
            startAnimation();
            tabsContainer.style.display = 'none';
            myTabContent.style.display = 'none';

            // Send the file data to the server
            fetch('/transcribe_selected_mp3/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                // Stop animation
                stopAnimation();
                tabsContainer.style.display = 'block';
                myTabContent.style.display = 'block';

                console.log(data)
                // Add summary and transcribed text corresponding divs
                document.getElementById('transcription-content').innerHTML = formatSummary(data.transcribed_text);
                document.getElementById('class-summary-content').innerHTML = formatSummary(data.response_text);
            })
            .catch(error => {
                console.error('Error:', error)
                // Stop animation
                stopAnimation();
            });
        }
    });
    
    // Trigger the file input click event
    fileInput.click();
}

const navLinks = document.querySelectorAll('.nav-link');

navLinks.forEach(link => {
  link.addEventListener('click', handleNavLinkClick);
});

function handleNavLinkClick(event) {
  // Remove active class from all links
  console.log("clicked navlink");
  navLinks.forEach(link => link.classList.remove('active'));
  
  // Add active class to clicked link
  event.target.classList.add('active');
}

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