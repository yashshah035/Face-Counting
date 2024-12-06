const video = document.getElementById('video');
const faceCountDisplay = document.getElementById('faceCount');
const startButton = document.getElementById('startButton');

startButton.addEventListener('click', async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
  } catch (err) {
    console.error("Error accessing camera:", err);
  }
});

video.addEventListener('play', () => {
  const canvas = document.createElement('canvas');
  const context = canvas.getContext('2d');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  function processFrame() {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/jpeg');
    fetch('/detect_faces', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ image: dataURL.split(',')[1] })
    })
    .then(response => response.json())
    .then(data => {
      faceCountDisplay.textContent = data.face_count;
    })
    .catch(error => console.error('Error:', error));
    requestAnimationFrame(processFrame);
  }
  requestAnimationFrame(processFrame);
});

