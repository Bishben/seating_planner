document.addEventListener("DOMContentLoaded", function () {
  console.log("✅ JavaScript Loaded!");

  let branchField = document.querySelector("#id_branch");
  let subjectField = document.querySelector("#id_subject");

  if (!branchField || !subjectField) {
    console.error("❌ Branch or Subject field not found.");
    return;
  }

  function updateSubjects(branchId) {
    if (!branchId) {
      console.warn("⚠️ No branch selected. Clearing subjects.");
      subjectField.innerHTML = "<option value=''>---------</option>";
      return;
    }

    fetch(`/admin/get_subjects_by_branch/?branch_id=${branchId}`)
      .then((response) => response.json())
      .then((data) => {
        console.log("✅ Subjects received:", data);

        subjectField.innerHTML = "<option value=''>---------</option>";

        data.subjects.forEach((subject) => {
          let option = document.createElement("option");
          option.value = subject.id;
          option.textContent = subject.code;
          subjectField.appendChild(option);
        });
      })
      .catch((error) => console.error("❌ Error fetching subjects:", error));
  }

  branchField.addEventListener("change", function () {
    let selectedBranch = branchField.value;
    updateSubjects(selectedBranch);
  });

  // If a branch is already selected (e.g., when editing an Exam), load its subjects
  if (branchField.value) {
    updateSubjects(branchField.value);
  }
});
