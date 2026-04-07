let fieldCount = 1;
const MAX_FIELDS = 5;

function AddField() {
  if (fieldCount >= MAX_FIELDS) {
    showError("formError", "Максимальное количество оценок: 5");
    return;
  }

  fieldCount++;
  const currentIndex = fieldCount;
  const container = document.getElementById("fieldContainer");
  const newDiv = document.createElement("div");
  const deleteButton = document.createElement("button");
  const newInput = document.createElement("input");

  newDiv.id = "field" + currentIndex;
  newDiv.className = "ratingContainer";

  deleteButton.id = "deleteCriteria" + currentIndex;
  deleteButton.type = "button";
  deleteButton.textContent = "Удалить оценку";
  deleteButton.className = "btn btn-danger submit-button";
  deleteButton.onclick = function () {
    DeleteField(currentIndex);
  };

  newInput.type = "text";
  newInput.name = "field" + currentIndex;
  newInput.id = "criteria" + currentIndex;
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
  console.log(fieldToRemove);
  if (fieldToRemove) {
    fieldToRemove.remove();
    fieldCount--;
    RenumberFields();
  }

  clearErrors("formError");
}

function RenumberFields() {
  const container = document.getElementById("fieldContainer");
  const fields = container.querySelectorAll(".ratingContainer");
  let newIndex = 1;

  fields.forEach((field) => {
    const currentIndex = newIndex;
    field.id = "field" + currentIndex;

    const input = field.querySelector("input");
    if (input) {
      input.name = "field" + currentIndex;
      input.id = "criteria" + currentIndex;
    }

    const button = field.querySelector("button");
    if (button) {
      button.id = "deleteCriteria" + currentIndex;
      button.onclick = function () {
        DeleteField(currentIndex);
      };
    }

    newIndex++;
  });
  fieldCount = fields.length;
}
