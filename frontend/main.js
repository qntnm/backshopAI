const startButton = document.getElementById('start-button');
const stopButton = document.getElementById('stop-button');
const audioPlayback = document.getElementById('audio-playback');


let audioContext;
let micStreamAudioSourceNode;
let audioWorkletNode;
let audioChunks = [];

startButton.addEventListener('click', async () => {
  // Check if the browser supports the required APIs
  if (!window.AudioContext || 
      !window.MediaStreamAudioSourceNode || 
      !window.AudioWorkletNode) {
    alert('Your browser does not support the required APIs');
    return;
  }

  // Request access to the user's microphone
  const micStream = await navigator
      .mediaDevices
      .getUserMedia({ audio: true });
      
  mediaRecorder = new MediaRecorder(micStream);
  // Collect audio chunks
  mediaRecorder.ondataavailable = (event) => {
    if (event.data.size > 0) {
      audioChunks.push(event.data);
    }
  };
   // Start recording
   mediaRecorder.start();
   audioChunks = []; // Clear any previous data
   console.log('Recording started...');
   startButton.disabled = true;
   stopButton.disabled = false;

  // Create the microphone stream
  audioContext = new AudioContext();
  mediaStreamAudioSourceNode = audioContext
      .createMediaStreamSource(micStream);

  // Create and connect AudioWorkletNode 
  // for processing the audio stream
  await audioContext
      .audioWorklet
      .addModule("my-audio-processor.js");
  audioWorkletNode = new AudioWorkletNode(
      audioContext,
      'my-audio-processor');
  micStreamAudioSourceNode.connect(audioWorkletNode);
});

// stopButton.addEventListener('click', () => {
// //   // Close audio stream
// //   micStreamAudioSourceNode.disconnect();
// //   audioContext.close();
// });
stopButton.addEventListener('click', () => {
    try {
      if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        // Stop recording
        mediaRecorder.stop();

        mediaRecorder.onstop = () => {
          console.log('Recording stopped.');

          // Create a Blob from the audio chunks
          const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });

          // Generate a URL for playback
          const audioURL = URL.createObjectURL(audioBlob);
          audioPlayback.src = audioURL;

          // Optionally allow the user to download the recording
          const downloadLink = document.createElement('a');
          downloadLink.href = audioURL;
          downloadLink.download = 'recording.webm';
          downloadLink.textContent = 'Download Recording';
          document.body.appendChild(downloadLink);

          // Reset buttons
          startButton.disabled = false;
          stopButton.disabled = true;
        };

        // Close the audio context
        micStreamAudioSourceNode.disconnect();
        audioContext.close();
      }
    } catch (err) {
      console.error('Error stopping recording:', err);
    }
  });