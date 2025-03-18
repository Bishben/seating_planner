document.addEventListener("DOMContentLoaded", function () {
  console.log("connected");
  const container = document.getElementById("exam-container");
  const eventSelect = document.getElementById("id_event");
  var currentEventID = eventSelect.value;
  const room = document.getElementById("id_number");
  const examDataField = document.getElementById("id_exam_data");
  const form = document.querySelector("form");

  let examOptionsCache = []; // Cache exam options for efficiency

  if (!container || !eventSelect || !form || !examDataField) return; // Prevent errors

  /**
   * Collects all selected exams from the dynamically generated
   * exam fields, converts the data into JSON format, and stores
   * it in the `exam_data` [hidden] attribute of the `ExamRoom` object.
   *
   * Each collected exam entry includes:
   * - `exam_id`: The ID of the selected exam.
   * - `roll_start`: The starting roll number for that exam.
   * - `roll_end`: The ending roll number for that exam.
   *
   * The resulting JSON structure looks like:
   * [
   *   { "exam_id": 1, "roll_start": 1001, "roll_end": 1020 },
   *   { "exam_id": 2, "roll_start": 2001, "roll_end": 2025 }
   * ]
   *
   * This function is triggered when the user clicks on:
   * - The "Save" button
   * - The "Add Another" button
   * - The "Continue" button
   *
   * If no valid exam data is provided (e.g., missing roll numbers),
   * that entry is ignored to ensure only complete data is saved.
   */
  function collectExamData() {
    let exams = [];
    // Selects and Iterates through all existing exam entries
    document.querySelectorAll(".exam-entry").forEach((div) => {
      const examId = div.querySelector(".exam-select").value;
      const rollStart = div.querySelector("input[name='roll_start']").value;
      const rollEnd = div.querySelector("input[name='roll_end']").value;
      // Only Add if All 3 attributes exist
      if (examId && rollStart && rollEnd) {
        exams.push({
          exam_id: parseInt(examId),
          roll_start: parseInt(rollStart),
          roll_end: parseInt(rollEnd),
        });
      }
    });
    examDataField.value = JSON.stringify(exams);
  }

  /**
   * Event Listener: Handles form submission for saving exam data.
   *
   * This listener is attached to the following buttons:
   * - "Save"
   * - "Add Another"
   * - "Continue"
   *
   * When any of these buttons are clicked:
   * 1. The `collectExamData()` function is called to gather the
   *    selected exam data and convert it into JSON format.
   * 2. The JSON data is stored in the `exam_data` field.
   * 3. An alert displays the collected JSON data for confirmation.
   * 4. The JSON data is also logged in the console for debugging.
   *
   * Purpose: Ensures exam data is properly collected and saved
   * before the form submission occurs.
   */
  document
    .querySelectorAll(
      "[name='_save'], [name='_addanother'], [name='_continue']"
    )
    .forEach((button) => {
      button.addEventListener("click", function () {
        collectExamData(); // Update JSON before saving
      });
    });

  /**
   * Fetches available exam options for a given event.
   *
   * @param {string} eventId - The ID of the selected event.
   * @returns {Promise<Array>} A promise that resolves to an array of exam options.
   *
   * The function performs the following steps:
   * 1. Sends a GET request to fetch exams linked to the provided `eventId`.
   * 2. If successful, it returns the JSON response containing exam details.
   * 3. If an error occurs during the fetch, it logs the error to the console
   *    and returns an empty array to prevent breaking the code flow.
   *
   * Purpose: Provides exam options for populating the dropdown in the UI.
   */
  async function fetchExamOptions(eventId) {
    try {
      const examResponse = await fetch(
        `http://127.0.0.1:8000/admin/home_page/examroom/get_exams/?event_id=${eventId}`
      );
      examOptionsCache = await examResponse.json();
    } catch (error) {
      console.error("Error fetching exams:", error);
    }
  }

  /**
   * Adds a new exam entry field to the container.
   *
   * This function dynamically creates a new exam entry element with the following:
   * - A dropdown (`<select>`) populated with exam options.
   * - Two input fields for `roll_start` and `roll_end`.
   * - A button to either add or remove the exam entry.
   *
   * If an `existingExam` is provided, the entry is pre-filled with its data
   * Use Case: `loadExistingExamData()`
   *
   * API Endpoint:
   * - GET `/admin/home_page/examroom/get_exams/?exam_id=${existingExam.exam_id}`
   *
   * Parameters:
   * @param {Array} examOptions - List of available exams to populate the dropdown.
   * @param {Object} [existingExam=null] - Optional object containing existing exam data
   *    (e.g., { exam_id: 1, roll_start: 100, roll_end: 200 }) to pre-fill the fields.
   *
   * Purpose: Dynamically adds an exam entry for user interaction, either pre-filled
   * with existing data or empty for new entries.
   */
  async function addExamField(examOptions, existingExam = null) {
    /* REMOVE PREVIOUSLY ADDED EXAM ENTRY FROM CACHE */
    if (container.children.length > 0) {
      const selectedExam = document.querySelector(
        ".exam-entry:last-child .exam-select"
      );

      const latestAddedExamId = selectedExam.value;

      examOptionsCache = examOptionsCache.filter(
        (exam) => exam.id != latestAddedExamId
      );

      examOptions = examOptionsCache;
    }

    /* DISABLE PREVIOUS FIELD */
    const lastEntry = document.querySelector(".exam-entry:last-child");
    if (lastEntry) {
      // Disabling Input
      lastEntry.querySelector(".exam-select").disabled = true;
      lastEntry.querySelector("input[name='roll_start']").disabled = true;
      lastEntry.querySelector("input[name='roll_end']").disabled = true;

      // Grey Out Input
      lastEntry.querySelector(".exam-select").classList.add("disabled-field");
      lastEntry
        .querySelector("input[name='roll_start']")
        .classList.add("disabled-field");
      lastEntry
        .querySelector("input[name='roll_end']")
        .classList.add("disabled-field");
    }

    /* CREATE NEW EXAM ENTRY */
    const div = document.createElement("div");
    div.classList.add("exam-entry");

    // Initiate / Open Select tag
    let selectHTML = `<select name="exam_choice" class="exam-select"><option value="">Select Exam</option>`;

    let examData;
    if (existingExam) {
      try {
        // Fetches Exam Details
        const examResponse = await fetch(
          `http://127.0.0.1:8000/admin/home_page/examroom/get_exams/?exam_id=${existingExam.exam_id}`
        );
        examData = await examResponse.json();
        // Replaces Select intiation with exisiting exam
        selectHTML = `<select name="exam_choice" class="exam-select"><option value="${existingExam.exam_id}">${examData[0].branch__year}${examData[0].branch__name} - ${examData[0].subject__code}</option>`;
      } catch (error) {
        console.error("Cannot resolve Existing Exam Data:", error);
      }
    }

    // Add all other exam options
    examOptions.forEach((exam) => {
      selectHTML += `<option value="${exam.id}">${exam.branch__year}${exam.branch__name} - ${exam.subject__code}</option>`;
    });
    selectHTML += `</select>`;

    // Initiate other fields
    div.innerHTML = `
      ${selectHTML}
      <input type="number" name="roll_start" placeholder="Start Roll">
      <input type="number" name="roll_end" placeholder="End Roll">
      <button type="button" class="button add-exam-btn">➕ Add Exam</button>
    `;

    if (existingExam) {
      // Replace fields with values if exam exists
      div.innerHTML = `
          ${selectHTML}
          <input type="number" name="roll_start" value=${existingExam.roll_start}>
          <input type="number" name="roll_end" value=${existingExam.roll_end}>
          <button type="button" class="button remove-exam-btn">❌ Remove</button>
        `;
    }

    container.appendChild(div);
    // Initialize Select2
    $(div).find(".exam-select").select2({
      width: "30%", // Ensures width of all fields are equal
    });

    if (examOptionsCache.length === 0) {
      const addButton = document.querySelector(".add-exam-btn");
      addButton.textContent = "All Exams Added";
      addButton.disabled = true;
    }
  }

  /**
   * Loads existing exam data for the selected event and room.
   *
   * This function fetches data from the server and populates the exam container
   * with existing exam entries if available. If no existing data is found,
   * it initializes the container with a new exam field.
   *
   * Preconditions:
   * - `eventSelect` and `room` must have valid values, i.e. Object must already exist.
   * - The `container` element should exist in the DOM.
   *
   * API Endpoint:
   * - GET `/admin/home_page/examroom/get_exam_room/?event_id={eventId}&room={room_num}`
   *
   * Potential Errors:
   * - Network errors during data fetch.
   * - Invalid or empty response data.
   */
  async function loadExistingExamData() {
    const eventId = eventSelect.value;
    const room_num = room.value;
    let examData = [];

    if (!eventId || !room_num) return;

    try {
      // Fetches ExamRoom Object if it exists
      const examRoomResponse = await fetch(
        `http://127.0.0.1:8000/admin/home_page/examroom/get_exam_room/?event_id=${eventId}&room=${room_num}`
      );
      const examRoomData = await examRoomResponse.json();

      // Extracts Exam data from JSON if it exists
      if (examRoomData.length > 0) examData = examRoomData[0].exam_data;
    } catch (error) {
      console.error("Failed to fetch Existing Exam Data: ", error);
    }

    await fetchExamOptions(eventId);

    container.innerHTML = "";
    for (const exam of examData) {
      await addExamField(examOptionsCache, exam);
    }
    await addExamField(examOptionsCache);
  }

  loadExistingExamData(); // calling function to Load All Exam entries if available

  /**
   * Event Listener: Listens for the "change" in event on the event selection dropdown.
   *
   * Triggered when the user selects a different event. Performs the following steps:
   * 1. Prompts the user for confirmation before clearing existing exam entries.
   *    - If confirmed, clears the exam container and fetches new exam options.
   *    - If declined, reverts the dropdown to its previous value.
   * 2. Calls `addExamField()` to add an empty exam field for the new event's options.
   *
   * Purpose: Ensures that switching events resets the exam entries while allowing the user
   * to cancel the change if needed.
   */
  eventSelect.addEventListener("change", async () => {
    if (container.children.length > 1) {
      // Creating a PopUp elemnt for Warning / Confirmation
      const confirmationBox = document.createElement("div");
      confirmationBox.classList.add("select2-confirmation");
      confirmationBox.innerHTML = `
      <p>Changing the event will remove all existing exam entries. Continue?</p>
      <button type="button" class="confirm-btn">Yes</button>
      <button type="button" class="cancel-btn">No</button>
    `;

      // Append to body or directly after the Select2 element
      document.body.appendChild(confirmationBox);

      // Position it near the Select2 dropdown
      const rect = eventSelect.getBoundingClientRect();
      confirmationBox.style.top = `${rect.bottom + window.scrollY}px`;
      confirmationBox.style.left = `${rect.left + window.scrollX}px`;

      // If "Yes" is clicked, i.e. User confirms change
      confirmationBox
        .querySelector(".confirm-btn")
        .addEventListener("click", async () => {
          container.innerHTML = "";
          const eventId = eventSelect.value;
          examOptionsCache = [];
          await fetchExamOptions(eventId);
          addExamField(examOptionsCache);
          confirmationBox.remove();
        });

      // If "No" is clicked, i.e. User declines change
      confirmationBox
        .querySelector(".cancel-btn")
        .addEventListener("click", () => {
          $(eventSelect).val(currentEventID).trigger("change"); // Reset the Select2 value
          confirmationBox.remove();
        });
    } else {
      container.innerHTML = "";
      const eventId = eventSelect.value;
      examOptionsCache = [];
      await fetchExamOptions(eventId);
      addExamField(examOptionsCache);
    }

    currentEventID = eventSelect.value;
  });

  /**
   * Event listener for click events inside the exam entry container, i.e. `❌ Remove` & `➕ Add Exam`
   *
   * - If the clicked element is an "Add Exam" button:
   *   - Ensures an event is selected before proceeding.
   *   - Fetches available exam options for the selected event.
   *   - Calls `addExamField()` to create a new exam entry with the fetched options.
   *   - Changes the clicked button to a "Remove" button to allow deletion.
   *
   * - If the clicked element is a "Remove" button:
   *   - Removes the corresponding `.exam-entry` element from the container.
   *
   * This listener efficiently handles adding and removing exam fields in the UI.
   */
  container.addEventListener("click", (event) => {
    if (event.target.classList.contains("add-exam-btn")) {
      const eventId = eventSelect.value;
      if (!eventId) {
        alert("Please select an event first.");
        return;
      }

      const latestExamField = container.lastElementChild;
      if (latestExamField) {
        const selectedExam =
          latestExamField.querySelector(".exam-select").value;

        if (!selectedExam) {
          alert("Please Select an Exam before adding.");
          return;
        }

        const rollStart = latestExamField.querySelector(
          '[name="roll_start"]'
        ).value;

        const rollEnd =
          latestExamField.querySelector('[name="roll_end"]').value;

        if (!rollStart || !rollEnd) {
          alert(
            "Please enter both Roll Start and Roll End before adding the exam."
          );
          return;
        }
      }

      addExamField(examOptionsCache);

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
