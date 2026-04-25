import React, { useState, useEffect } from "react";
import { getCookie, getCsrfToken, isAuthenticated } from "../utils/cookies";
import "../styles/notification.css";

function NotificationList() {
  const [notifications, setNotification] = useState([]);
  const [unreadCount, setUnreadCount] = useState([]);
  const [loading, setLoading] = useState({});

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
      const notification = {
        id: data.notification_id,
        message: data.message,
        is_read: data.is_read,
        created_at: new Date().toISOString(),
        type: data.notification_type,
      };

      if (data.notification_type == "team_invite" && data.team_id) {
        notification.team_id = data.team_id;
      }

      setNotification((prev) => [notification, ...prev]);
      setUnreadCount((prev) => prev + 1);
    };

    return () => socket.close();
  }, []);

  const markAsRead = (id) => {
    fetch(`/api/notifications/${id}/read/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCsrfToken(),
      },
    })
      .then(() => {
        setNotification((prev) =>
          prev.map((n) => (n.id === id ? { ...n, is_read: true } : n)),
        );
        setUnreadCount((prev) => Math.max(0, prev - 1));
      })
      .catch((error) => console.log("mark read: ", error));
  };

  const acceptInvitation = (notificationId, teamId) => {
    setLoading((prev) => ({ ...prev, [notificationId]: true }));

    const csrftoken = getCsrfToken();

    fetch(`/api/notifications/${teamId}/accept/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status == "ok") {
          markAsRead(notificationId);
          location.reload();
        } else {
          console.error(data.error || "Ошибка при принятии приглашения");
        }
      })
      .catch((error) => console.error(error))
      .finally(() => {
        setLoading((prev) => ({ ...prev, [notificationId]: false }));
      });
  };

  const rejectInvitation = (notificationId, teamId) => {
    setLoading((prev) => ({ ...prev, [notificationId]: true }));
    const csrftoken = getCsrfToken();

    fetch(`/api/notifications/${teamId}/reject/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status == "ok") {
          markAsRead(notificationId);
          location.reload();
        } else {
          console.error(data.error || "Ошибка при принятии приглашения");
        }
      })
      .catch((error) => console.error(error))
      .finally(() => {
        setLoading((prev) => ({ ...prev, [notificationId]: false }));
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
            className={`notification-${notif.is_read ? "read" : "unread"}`}
          >
            <div className="message-container">
              <p>{notif.message}</p>

              {!notif.is_read && (
                <button
                  className="read-btn"
                  onClick={() => markAsRead(notif.id)}
                >
                  Прочитано
                </button>
              )}

              {notif.type == "team_invite" && !notif.is_read && (
                <div className="invite-actions">
                  <button
                    className="accept-btn"
                    onClick={() => acceptInvitation(notif.id, notif.team_id)}
                    disabled={loading[notif.id]}
                  >
                    {loading[notif.id] ? "Загрузка..." : "Принять"}
                  </button>
                  <button
                    className="reject-btn"
                    onClick={() => rejectInvitation(notif.id, notif.team_id)}
                    disabled={loading[notif.id]}
                  >
                    Отклонить
                  </button>
                </div>
              )}
            </div>
            <small className="date-text">
              {new Date(notif.created_at).toLocaleString()}
            </small>
          </div>
        );
      })}
    </div>
  );
}

export default NotificationList;
