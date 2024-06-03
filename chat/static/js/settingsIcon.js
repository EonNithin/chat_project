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