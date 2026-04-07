const title = document.getElementById("title");
const theme = document.getElementById("theme");

const dateStartInput = document.getElementById("date_start");
const dateEndInput = document.getElementById("date_end");
const dateRatingInput = document.getElementById("date_rating");
const container = document.getElementById("fieldContainer");

const createBtn = document.getElementById("createBtn");

function validateForm() {
  const isTitleValid = validateTitle();
  const isThemeValid = validateTheme();
  const isDatesValid = validateDateOrder();
  const isRatingsValid = validateAllRatingFields();

  if (isTitleValid && isThemeValid && isDatesValid && isRatingsValid) {
    createBtn.disabled = false;
  } else {
    createBtn.disabled = true;
  }
}

function validateTitle() {
  if (!title.value) return false;
  const value = title.value.trim();

  if (value.length < 3) {
    showError("formError", "Название должно быть не менее 3 символов");
    return false;
  }

  clearErrors("formError");
  return true;
}

function validateTheme() {
  if (!theme.value) return false;
  const value = theme.value.trim();

  if (value.length < 3) {
    showError("formError", "Тема очень коротка: не менее 3 символов");
    return false;
  }

  clearErrors("formError");
  return true;
}

function validateAllRatingFields() {
  const length = container.children.length;

  for (let i = 1; i <= length; i++) {
    if (!validateRatingField(i)) {
      showError("formError", "Оценка пустая, напишите ваш критерий оценки");
      return false;
    }
  }

  clearErrors("formError");
  return true;
}

function validateRatingField(fieldId) {
  const ratingContainer = document.getElementById("field" + fieldId);
  const field = ratingContainer.querySelector('input[type="text"');

  if (!field.value) return false;
  return true;
}

function checkDateFuture(dateString) {
  const date = new Date(dateString);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return date > today;
}

function validateDateOrder() {
  let errorMessage = "";

  if (!dateStartInput.value || !dateEndInput.value) {
    return false;
  }

  if (
    !checkDateFuture(dateStartInput.value) ||
    !checkDateFuture(dateEndInput.value)
  ) {
    return false;
  }

  const startValue = new Date(dateStartInput.value);
  const endValue = new Date(dateEndInput.value);

  if (startValue && endValue && endValue <= startValue) {
    console.log("validateDateOrders проблема с началом и концом");
    showError("formError", "Дата конца должна быть позже даты начала");
    return false;
  }

  if (dateRatingInput.value) {
    if (!checkDateFuture(dateRatingInput.value)) {
      return false;
    }
    const ratingValue = new Date(dateRatingInput.value);

    if (ratingValue <= startValue) {
      showError("formError", "Дата оценки должна быть позже даты начала");
      return false;
    }

    if (endValue <= ratingValue) {
      showError("formError", "Дата оценки должна быть раньше даты конца");
      return false;
    }
  }

  clearErrors("formError");
  return true;
}

function showError(elementId, message) {
  console.log("showError works");
  const errorElement = document.getElementById(elementId);
  if (errorElement) {
    errorElement.textContent = message;
    errorElement.classList.add("visible");
  }
}

function clearErrors(elementId) {
  const errorElement = document.getElementById(elementId);
  if (errorElement) {
    errorElement.textContent = "";
    errorElement.classList.remove("visible");
  }
}

dateStartInput.addEventListener("change", function () {
  validateDateOrder();
  validateForm();
});
dateEndInput.addEventListener("change", function () {
  validateDateOrder();
  validateForm();
});
dateRatingInput.addEventListener("change", function () {
  validateDateOrder();
  validateForm();
});
title.addEventListener("input", function () {
  validateTitle();
  validateForm();
});
theme.addEventListener("input", function () {
  validateTheme();
  validateForm();
});
container.addEventListener("input", function () {
  validateAllRatingFields();
  validateForm();
});

validateForm();
