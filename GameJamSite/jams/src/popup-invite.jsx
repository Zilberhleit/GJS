import React from "react";
import ReactDOM from "react-dom/client";
import InvitePopup from "./components/InvitePopup";

window.openInvitePopup = (teamId) => {
  console.log("openPopup called with id:" + teamId);
  let container = document.getElementById("react-popup-container");

  if (!container) {
    container = document.createElement("div");
    container.id = "react-popup-container";
    document.body.appendChild(container);
  }

  const closePopup = () => {
    const root = ReactDOM.createRoot(container);
    root.unmount();
    container.style.display = "none";
  };

  const root = ReactDOM.createRoot(container);
  container.style.display = "block";

  root.render(
    <InvitePopup teamId={teamId} isOpen={true} onClose={closePopup} />,
  );
};
