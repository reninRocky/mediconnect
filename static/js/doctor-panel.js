const doctorId = window.__DOCTOR_ID__;
const notif = io("/notifications");

notif.on("connect", () => {
  notif.emit("join_doctor", { doctor_id: doctorId });
});

notif.on("call_request", () => {
  // simplest UX: reload to show pending list
  window.location.reload();
});

