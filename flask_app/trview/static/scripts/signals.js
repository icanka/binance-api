console.log("signals.js");
selectElementValue = document.getElementById("inputStatus").value;
console.log("selectElementValue: " + selectElementValue);

// check if selectElementValue is something other than "Select a table"
if (selectElementValue === "Select Table") {
  tableName = "webhooks";
}else{
  tableName = selectElementValue;
}
// Send AJAX request to Flask server, and return promise, this is an async operation
fetchTableColumnsAndInitialize(tableName);

const selectElement = document.getElementById("inputStatus");

// Event listener for the 'change' event
selectElement.addEventListener("change", (event) => {
  const selectedTable = event.target.value;
  // Handle the selected table here
  console.log("Reinitializing table with new table:", selectedTable);
  // Remove the previous event handler
  console.log("Removing previous event handler");
  datatable.off("column-visibility.dt", columnVisibilityHandler);
  console.log("Destroying previous table");
  datatable.destroy(); // Destroy the previous table
  // Reinitialize the table
  console.log("datatable destroyed");
  let tbody = datatable.table().body();
  tbody = $(tbody);
  console.log("Emptying tbody");
  tbody.empty();
  signalsTableInitialized = false;
  console.log("Emptying finished");
  if (!signalsTableInitialized) {
    console.log("Signals table not initialized yet, initializing now");
    fetchTableColumnsAndInitialize(selectedTable);
  }
});
