console.log('This is a popup!');

//simulates a scenario such that the loading screen will show for test purposes, remove later
setTimeout(function() {
    document.getElementById('loader-container').style.display = 'none';
    document.getElementById('chart-heading').style.display = 'block';
    document.getElementById('chartContainer').style.display = 'block';
}, 2000); 