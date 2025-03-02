document.addEventListener("DOMContentLoaded", function () {
  console.log("connected");
  const container = document.getElementById("exam-container");
  const eventSelect = document.getElementById("id_event");
  const form = document.querySelector("form"); // Get the admin form

  if (!container || !eventSelect || !form) return; // Prevent errors

  function collectExamData() {
    let exams = [];
    document.querySelectorAll(".exam-entry").forEach((div) => {
      const examId = div.querySelector(".exam-select").value;
      const rollStart = div.querySelector("input[name='roll_start']").value;
      const rollEnd = div.querySelector("input[name='roll_end']").value;
      if (examId && rollStart && rollEnd) {
        exams.push({
          exam_id: parseInt(examId),
          roll_start: parseInt(rollStart),
          roll_end: parseInt(rollEnd),
        });
      }
    });
    alert("Exam Data JSON: " + examDataField.value);
    examDataField.value = JSON.stringify(exams); // Set the hidden JSON field
  }

  form.addEventListener("submit", function () {
    collectExamData(); // Call the function just before form submission
  });

  function fetchExamOptions(eventId, callback) {
    fetch(
      `http://127.0.0.1:8000/admin/home_page/examroom/get_exams/?event_id=${eventId}`
    )
      .then((response) => response.json())
      .then((data) => callback(data))
      .catch((error) => console.error("Error fetching exams:", error));
  }

  eventSelect.addEventListener("change", () => {
    container.innerHTML = ""; // Clear old exams when event changes
    const eventId = eventSelect.value;
    fetchExamOptions(eventId, (examOptions) => {
      addExamField(examOptions); // Add the first exam field automatically
    });
  });

  function addExamField(examOptions) {
    const div = document.createElement("div");
    div.classList.add("exam-entry");

    let selectHTML = `<select name="exam_choice" class="exam-select"><option value="">Select Exam</option>`;
    examOptions.forEach((exam) => {
      selectHTML += `<option value="${exam.id}">${exam.branch__year}${exam.branch__name} - ${exam.subject__code}</option>`;
    });
    selectHTML += `</select>`;

    div.innerHTML = `
      ${selectHTML}
      <input type="number" name="roll_start" placeholder="Start Roll">
      <input type="number" name="roll_end" placeholder="End Roll">
      <button type="button" class="button add-exam-btn">➕ Add Exam</button>
    `;

    container.appendChild(div);
    $(div).find(".exam-select").select2(); // Reinitialize Select2
  }

  container.addEventListener("click", function (event) {
    if (event.target.classList.contains("add-exam-btn")) {
      console.log("Add Exam clicked!");
      const eventId = eventSelect.value;
      if (!eventId) {
        alert("Please select an event first.");
        return;
      }

      fetchExamOptions(eventId, (examOptions) => {
        const newExamDiv = document.createElement("div");
        newExamDiv.classList.add("exam-entry");

        let selectHTML = `<select name="exam_choice" class="exam-select"><option value="">Select Exam</option>`;
        examOptions.forEach((exam) => {
          selectHTML += `<option value="${exam.id}">${exam.branch__year}${exam.branch__name} - ${exam.subject__code}</option>`;
        });
        selectHTML += `</select>`;

        newExamDiv.innerHTML = `
          ${selectHTML}
          <input type="number" name="roll_start" placeholder="Start Roll">
          <input type="number" name="roll_end" placeholder="End Roll">
          <button type="button" class="button add-exam-btn">➕ Add Exam</button>
        `; // <button type="button" class="button remove-exam-btn">❌ Remove</button>

        container.appendChild(newExamDiv);
        $(newExamDiv).find(".exam-select").select2(); // Reinitialize Select2
      });

      // Change the previous "Add Exam" button to "Remove"
      event.target.textContent = "❌ Remove";
      event.target.classList.remove("add-exam-btn");
      event.target.classList.add("remove-exam-btn");
    }

    // Handle remove button clicks
    else if (event.target.classList.contains("remove-exam-btn")) {
      event.target.parentElement.remove();
    }
  });
});
