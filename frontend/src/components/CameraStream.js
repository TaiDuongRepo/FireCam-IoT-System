import React, { useEffect, useRef } from 'react';

const CameraStream = () => {
  const videoRef = useRef(null);

  useEffect(() => {
    const startCamera = async () => {
      const video = videoRef.current;
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      video.srcObject = stream;

      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');

      const captureFrame = () => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(async (blob) => {
          const formData = new FormData();
          formData.append('file', blob, 'frame.jpg');

          await fetch("/upload_frame", {
            method: "POST",
            body: formData
          });
        }, 'image/jpeg');

        requestAnimationFrame(captureFrame);
      };
      captureFrame();
    };

    startCamera();
  }, []);

  return (
    <div>
      <p>TaiDuong DevOps</p>
      <h1>Stream Camera Feed to Server</h1>
      <video ref={videoRef} autoPlay playsInline></video>
    </div>
  );
};

export default CameraStream;