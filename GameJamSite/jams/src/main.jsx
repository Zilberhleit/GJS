import React from "react";
import ReactDOM from "react-dom/client";
import "./popup-invite.jsx";
import NotificationList from "./components/NotificationList";

console.log("React loaded");

const container = document.getElementById("react-notifications-root");

if (container) {
  const root = ReactDOM.createRoot(container);
  root.render(<NotificationList />);
}

//ReactDOM.createRoot(document.getElementById("react-root")).render(<App />);
window.dispatchEvent(new Event("react-loaded"));
