const roomId = window.__ROOM_ID__;
const isPolite = Boolean(window.__POLITE__);
const iceServers = Array.isArray(window.__ICE_SERVERS__)
  ? window.__ICE_SERVERS__
  : [{ urls: "stun:stun.l.google.com:19302" }];
const statusEl = document.getElementById("callStatus");
const btnStart = document.getElementById("btnStart");
const btnHangup = document.getElementById("btnHangup");
const localVideo = document.getElementById("localVideo");
const remoteVideo = document.getElementById("remoteVideo");

const socket = io("/video");

let pc = null;
let localStream = null;
let makingOffer = false;
let ignoreOffer = false;
let isStarted = false;
let pendingCandidates = [];
let remoteDescSet = false;

function setStatus(t) {
  if (statusEl) statusEl.textContent = t;
}

// Connect to socket and join room immediately
socket.on("connect", () => {
  console.log("Socket connected, joining room:", roomId);
  socket.emit("join_room", { room: roomId });
  setStatus("Connected to room. Click Start to begin.");
});

socket.on("disconnect", () => {
  setStatus("Disconnected from server.");
});

function createPC() {
  console.log("Creating peer connection");
  const peer = new RTCPeerConnection({
    iceServers,
  });

  peer.onicecandidate = (event) => {
    if (event.candidate) {
      console.log("Sending ICE candidate");
      socket.emit("ice-candidate", { room: roomId, candidate: event.candidate });
    }
  };

  peer.ontrack = (event) => {
    console.log("Received remote track");
    remoteVideo.srcObject = event.streams[0];
  };

  peer.onconnectionstatechange = () => {
    const st = peer.connectionState;
    console.log("Connection state:", st);
    if (st === "connected") setStatus("Connected! Video call active.");
    else if (st === "disconnected") setStatus("Disconnected (network change).");
    else if (st === "failed") setStatus("Connection failed. Try hang up + start again.");
    else if (st === "connecting") setStatus("Connecting to peer…");
    else if (st === "closed") setStatus("Connection closed.");
  };

  peer.oniceconnectionstatechange = () => {
    console.log("ICE connection state:", peer.iceConnectionState);
  };

  peer.onsignalingstatechange = () => {
    console.log("Signaling state:", peer.signalingState);
  };

  peer.onnegotiationneeded = async () => {
    try {
      console.log("Negotiation needed");
      makingOffer = true;
      const offer = await peer.createOffer();
      await peer.setLocalDescription(offer);
      console.log("Sending offer");
      socket.emit("offer", { room: roomId, offer: peer.localDescription });
      setStatus("Calling…");
    } catch (e) {
      setStatus(`Negotiation error: ${e}`);
      console.error("Negotiation error:", e);
    } finally {
      makingOffer = false;
    }
  };

  return peer;
}

async function startCall() {
  if (isStarted) {
    setStatus("Call already started.");
    return;
  }
  
  try {
    setStatus("Requesting camera and microphone…");
    console.log("Getting user media…");
    
    localStream = await navigator.mediaDevices.getUserMedia({ 
      video: { width: 640, height: 480 }, 
      audio: true 
    });
    
    localVideo.srcObject = localStream;
    console.log("Local stream obtained");

    pc = createPC();
    
    // Add all tracks to peer connection
    localStream.getTracks().forEach((track) => {
      console.log("Adding track:", track.kind);
      pc.addTrack(track, localStream);
    });

    isStarted = true;
    
    // If we have pending candidates, add them now
    if (pendingCandidates.length > 0 && remoteDescSet) {
      console.log("Adding pending ICE candidates");
      for (const candidate of pendingCandidates) {
        try {
          await pc.addIceCandidate(candidate);
        } catch (e) {
          console.error("Error adding pending candidate:", e);
        }
      }
      pendingCandidates = [];
    }

    setStatus("Ready. Waiting for peer to join…");
  } catch (e) {
    setStatus(`Error accessing camera/mic: ${e.message}`);
    console.error("getUserMedia error:", e);
  }
}

async function hangup() {
  console.log("Hanging up");
  
  try {
    socket.emit("end_call", { room: roomId });
  } catch (e) {
    console.error("Error sending end_call:", e);
  }

  if (pc) {
    pc.close();
    pc = null;
  }
  
  if (localStream) {
    localStream.getTracks().forEach((t) => t.stop());
    localStream = null;
  }
  
  localVideo.srcObject = null;
  remoteVideo.srcObject = null;
  makingOffer = false;
  ignoreOffer = false;
  isStarted = false;
  remoteDescSet = false;
  pendingCandidates = [];
  
  setStatus("Call ended. Click Start to begin again.");
}

// Handle incoming offer
socket.on("offer", async (data) => {
  console.log("Received offer", data);
  if (!data?.offer) return;

  try {
    // If we haven't started yet, auto-start
    if (!isStarted) {
      setStatus("Incoming call… Starting camera…");
      console.log("Auto-starting for incoming call");
      
      try {
        localStream = await navigator.mediaDevices.getUserMedia({ 
          video: { width: 640, height: 480 }, 
          audio: true 
        });
        localVideo.srcObject = localStream;
        
        pc = createPC();
        localStream.getTracks().forEach((track) => {
          pc.addTrack(track, localStream);
        });
        
        isStarted = true;
      } catch (e) {
        setStatus(`Error starting camera: ${e.message}`);
        console.error("Auto-start error:", e);
        return;
      }
    }

    const offerDesc = new RTCSessionDescription(data.offer);
    const offerCollision = makingOffer || pc.signalingState !== "stable";
    
    ignoreOffer = !isPolite && offerCollision;
    console.log("Offer collision:", offerCollision, "Ignoring:", ignoreOffer, "IsPolite:", isPolite);
    
    if (ignoreOffer) {
      console.log("Ignoring offer due to collision");
      return;
    }

    setStatus("Answering call…");
    await pc.setRemoteDescription(offerDesc);
    remoteDescSet = true;
    
    const answer = await pc.createAnswer();
    await pc.setLocalDescription(answer);
    
    console.log("Sending answer");
    socket.emit("answer", { room: roomId, answer: pc.localDescription });
    setStatus("Connecting…");
    
    // Process any pending candidates
    if (pendingCandidates.length > 0) {
      console.log("Processing pending candidates after answer");
      for (const candidate of pendingCandidates) {
        try {
          await pc.addIceCandidate(candidate);
        } catch (e) {
          console.error("Error adding pending candidate:", e);
        }
      }
      pendingCandidates = [];
    }
  } catch (e) {
    setStatus(`Error handling offer: ${e.message}`);
    console.error("Offer handling error:", e);
  }
});

// Handle incoming answer
socket.on("answer", async (data) => {
  console.log("Received answer", data);
  if (!data?.answer || !pc) return;
  
  try {
    const answerDesc = new RTCSessionDescription(data.answer);
    await pc.setRemoteDescription(answerDesc);
    remoteDescSet = true;
    console.log("Remote description set from answer");
    setStatus("Connected! Establishing video…");
    
    // Process any pending candidates
    if (pendingCandidates.length > 0) {
      console.log("Processing pending candidates");
      for (const candidate of pendingCandidates) {
        try {
          await pc.addIceCandidate(candidate);
        } catch (e) {
          console.error("Error adding pending candidate:", e);
        }
      }
      pendingCandidates = [];
    }
  } catch (e) {
    setStatus(`Error handling answer: ${e.message}`);
    console.error("Answer handling error:", e);
  }
});

// Handle ICE candidates
socket.on("ice-candidate", async (data) => {
  console.log("Received ICE candidate", data);
  if (!data?.candidate) return;
  
  try {
    const candidate = new RTCIceCandidate(data.candidate);
    
    // If we don't have a peer connection yet or remote description isn't set, queue it
    if (!pc || !remoteDescSet) {
      console.log("Queueing ICE candidate (no PC or remote desc not set)");
      pendingCandidates.push(candidate);
      return;
    }
    
    await pc.addIceCandidate(candidate);
    console.log("ICE candidate added");
  } catch (e) {
    console.error("Error adding ICE candidate:", e);
    // Don't show error to user for ICE failures, they often recover
  }
});

socket.on("end_call", async () => {
  console.log("Received end_call");
  await hangup();
});

// Event listeners
btnStart?.addEventListener("click", () => {
  console.log("Start button clicked");
  startCall().catch((e) => {
    setStatus(`Error: ${e.message}`);
    console.error("Start error:", e);
  });
});

btnHangup?.addEventListener("click", () => {
  console.log("Hangup button clicked");
  hangup().catch((e) => console.error("Hangup error:", e));
});

// Handle page unload
window.addEventListener("beforeunload", () => {
  try {
    if (localStream) {
      localStream.getTracks().forEach((t) => t.stop());
    }
    if (pc) {
      pc.close();
    }
    socket.emit("leave_room", { room: roomId });
  } catch (e) {
    console.error("Cleanup error:", e);
  }
});

// Handle errors
window.addEventListener("error", (e) => {
  console.error("Global error:", e);
});

console.log("Video.js loaded. Room:", roomId, "IsPolite:", isPolite);
