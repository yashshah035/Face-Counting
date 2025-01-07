import React, { useEffect, useRef, useState } from "react";

const Camera = () => {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const [isCameraOn, setIsCameraOn] = useState(false);
    const [faceCount, setFaceCount] = useState(0);
    const ws = useRef(null);

    const startCamera = () => {
        setIsCameraOn(true);
        ws.current = new WebSocket("ws://localhost:8000/ws");

        ws.current.onmessage = (event) => {
            const blob = new Blob([event.data], { type: "image/jpeg" });
            const url = URL.createObjectURL(blob);
            videoRef.current.src = url;

            // Draw on canvas
            const ctx = canvasRef.current.getContext("2d");
            const img = new Image();
            img.onload = () => {
                ctx.drawImage(img, 0, 0, canvasRef.current.width, canvasRef.current.height);
            };
            img.src = url;
        };
    };

    const stopCamera = () => {
        setIsCameraOn(false);
        if (ws.current) {
            ws.current.close();
        }
    };

    return (
        <div>
            <h1>Face Detection</h1>
            <button onClick={startCamera} disabled={isCameraOn}>
                Open Camera
            </button>
            <button onClick={stopCamera} disabled={!isCameraOn}>
                Close Camera
            </button>
            <div>
                <video ref={videoRef} autoPlay style={{ display: "none" }} />
                <canvas ref={canvasRef} width="1280" height="720" />
            </div>
            <p>Number of Faces: {faceCount}</p>
        </div>
    );
};

export default Camera;