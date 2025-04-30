/**
 * Dynamically updates the subject dropdown based on the selected branch in Django Admin.
 * Uses AJAX to fetch relevant subjects without refreshing the page.
 *
 * @fileoverview Documentation: 
 *
 */
document.addEventListener("DOMContentLoaded", function () {
  console.log("filter script loaded");
  const branchField = document.querySelector("#id_branch");
  const subjectField = document.querySelector("#id_subject");

  if (branchField && subjectField) {
    if (!branchField.value) {
      subjectField.innerHTML = "<option value=''>---------</option>";
    }

    branchField.addEventListener("change", function () {
      const branchId = branchField.value;
      subjectField.innerHTML = "<option value=''>---------</option>"; // Reset options

      if (branchId) {
        fetch(`/admin/home_page/exam/get_subjects/?branch_id=${branchId}`)
          .then((response) => response.json())
          .then((data) => {
            data.forEach((subject) => {
              let option = new Option(subject.code, subject.id);
              subjectField.add(option);
            });
          })
          .catch((error) => console.error("Error fetching subjects:", error));
      }
    });
  }
});
