document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("addRow").addEventListener("click", function () {
        let table = document.getElementById("editableTable").getElementsByTagName('tbody')[0];
        let newRow = table.insertRow();
        let colCount = document.getElementById("tableHeader").cells.length;

        for (let i = 0; i < colCount; i++) {
            let newCell = newRow.insertCell(i);
            newCell.contentEditable = "true";
            newCell.innerText = "Enter Data";
        }
    });

    document.getElementById("addColumn").addEventListener("click", function () {
        let table = document.getElementById("editableTable");
        let headerRow = document.getElementById("tableHeader");
        let newHeader = document.createElement("th");
        newHeader.innerText = "New Column";
        headerRow.appendChild(newHeader);

        let rows = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr");
        for (let row of rows) {
            let newCell = row.insertCell();
            newCell.contentEditable = "true";
            newCell.innerText = "Enter Data";
        }
    });

    document.getElementById("saveChanges").addEventListener("click", function () {
        let table = document.getElementById("editableTable");
        let data = [];
        let rows = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr");

        for (let row of rows) {
            let rowData = [];
            let cells = row.getElementsByTagName("td");
            for (let cell of cells) {
                rowData.push(cell.innerText);
            }
            data.push(rowData);
        }
    });
});