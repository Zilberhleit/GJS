let fieldCount = 1;
const MAX_FIELDS = 5;

function AddField() {
  if (fieldCount >= MAX_FIELDS) {
    showError("formError", "Максимальное количество оценок: 5");
    return;
  }

  fieldCount++;
  const container = document.getElementById("fieldContainer");
  const newDiv = document.createElement("div");
  const deleteButton = document.createElement("button");
  const newInput = document.createElement("input");

  newDiv.id = "field" + fieldCount;
  newDiv.className = "ratingContainer";

  deleteButton.id = "deleteCriteria" + fieldCount;
  deleteButton.type = "button";
  deleteButton.textContent = "Удалить оценку";
  deleteButton.className = "btn btn-danger submit-button";
  deleteButton.onclick = function () {
    DeleteField(fieldCount);
  };

  newInput.type = "text";
  newInput.name = "field" + fieldCount;
  newInput.id = "criteria" + fieldCount;
  newInput.placeholder = "Ваша оценка";
  newInput.value = "Общая оценка";
  newInput.required = true;
  newInput.className = "form-input";

  newDiv.appendChild(newInput);
  newDiv.appendChild(deleteButton);
  container.appendChild(newDiv);
  clearErrors("formError");
}

function DeleteField(fieldIndex) {
  if (fieldCount <= 1) {
    showError("formError", "Должна быть минимум одна оценка");
    return;
  }

  const fieldToRemove = document.getElementById("field" + fieldIndex);

  if (fieldToRemove) {
    fieldToRemove.remove();
    fieldCount--;
  }

  clearErrors("formError");
}
