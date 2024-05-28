function aiChatPage(){
    window.location.href = '/ai_chatpage/';
}

function aiProcessLatestRecordedFile(){
    window.location.href = '/ai_response/';
}

function chooseFileToAIProcess() {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'audio/mp3'; // Accept only MP3 files
    
    // Event listener for when a file is selected
    fileInput.addEventListener('change', function(event) {
        const selectedFile = event.target.files[0];
        
        // Check if a file is selected
        if (selectedFile) {
            const fileURL = URL.createObjectURL(selectedFile);
            // Process the file as needed
            console.log('Selected file:', selectedFile.name);
            // Perform any additional processing or uploading here
        }
    });
    
    // Trigger the file input click event
    fileInput.click();
}