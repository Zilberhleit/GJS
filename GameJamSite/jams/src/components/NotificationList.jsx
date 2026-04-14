import React, { useState, useEffect } from "react";
import "../../static/css/notifications.css";

function NotificationList() {
  const [notifications, setNotification] = useState([]);
  const [unreadCount, setUnreadCount] = useState([]);

  useEffect(() => {
    fetch("/api/notifications/")
      .then((res) => res.json())
      .then((data) => {
        setNotification(data.notifications);
        setUnreadCount(data.unread_count);
      });
  }, []);

  useEffect(() => {
    const socket = new WebSocket(
      "ws://" + window.location.host + "/ws/notifications/",
    );

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (
        data.type === "connection" ||
        data.message === "Connected to notification_all"
      ) {
        console.log("WebSocket connected:", data.message);
        return;
      }

      setNotification((prev) => [
        {
          id: data.notification_id,
          message: data.message,
          is_read: false,
          created_at: new Date().toISOString(),
          type: data.notification_type,
        },
        ...prev,
      ]);

      setUnreadCount((prev) => prev + 1);
    };

    return () => socket.close();
  }, []);

  const markAsRead = (id) => {
    fetch(`/api/notifications/${id}/read/`, { method: "POST" }).then(() => {
      setNotification((prev) =>
        prev.map((n) => (n.id === id ? { ...n, is_read: true } : n)),
      );
      setUnreadCount((prev) => Math.max(0, prev - 1));
    });
  };

  return (
    <div className="notification-list">
      <h2>Уведомления</h2>
      {notifications.length === 0 && <p>Нет уведомлений</p>}

      {notifications.map((notif) => {
        return (
          <div
            key={notif.id}
            className={`notification ${notif.is_read ? "read" : "unread"}`}
          >
            <p>{notif.message}</p>
            <small>{new Date(notif.created_at).toLocaleString()}</small>
            {!notif.is_read && (
              <button onClick={() => markAsRead(notif.id)}>Прочитано</button>
            )}
          </div>
        );
      })}
    </div>
  );
}

export default NotificationList;
