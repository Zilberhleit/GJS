import React, { useState, useEffect, useRef } from "react";

const InvitePopup = ({ teamId, isOpen, onClose }) => {
  const [username, setUsername] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const suggestionsRef = useRef(null);

  useEffect(() => {
    if (username.length < 2) {
      setSuggestions([]);
      setShowSuggestions(false);
      return;
    }

    const searchUsers = async () => {
      try {
        const response = await fetch(
          "/api/search-users/?q=" + encodeURIComponent(username),
        );
        const data = await response.json();
        setSuggestions(data);
        setShowSuggestions(data.length > 0);
      } catch (error) {
        console.error("Ошибка поиска:" + error);
      }
    };

    const debounceTimer = setTimeout(searchUsers, 300);
    return () => clearTimeout(debounceTimer);
  }, [username]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response = await fetch(`/team/${teamId}/invite`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
            .value,
        },
        body: new URLSearchParams({ username }),
      });

      if (response.ok) {
        setUsername("");
        onClose();
      } else {
        const error = await response.text();
      }
    } catch (error) {
      console.error("Ошибка: " + error);
    } finally {
      setIsLoading(false);
    }
  };

  const selectUser = (selectedUser) => {
    setUsername(selectedUser);
    setShowSuggestions(false);
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        suggestionsRef.current &&
        !suggestionsRef.current.contains(event.target)
      ) {
        setShowSuggestions(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  if (!isOpen) return null;

  return (
    <div id="popup-invite" className="overlay active">
      <div className="popup" onClick={(e) => e.stopPropagation()}>
        <form onSubmit={handleSubmit} className="game-upload-form">
          <div className="form-content">
            <div className="form-group" ref={suggestionsRef}>
              <label htmlFor="username">Никнейм пользователя</label>
              <input
                type="text"
                id="username"
                name="username"
                className="form-input"
                placeholder="Введите никнейм"
                onChange={(e) => setUsername(e.target.value)}
                required
                autocomplete="off"
              />
              {showSuggestions && suggestions.length > 0 && (
                <div id="username-suggestions" className="suggestions-dropdown">
                  {suggestions.map((user) => (
                    <div
                      key={user.username}
                      className="suggestion-item"
                      onClick={() => selectUser(user.username)}
                    >
                      {user.username}
                    </div>
                  ))}
                </div>
              )}
            </div>
            <div className="form-actions">
              <a className="btn btn-secondary cancel-button" href="#">
                <span>Отмена</span>
              </a>
              <button type="submit" className="btn btn-primary submit-button">
                <span>
                  {isLoading ? "Отправка..." : "Отправить приглашение"}
                </span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default InvitePopup;
