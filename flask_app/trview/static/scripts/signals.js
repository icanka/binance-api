console.log("signals.js");
selectElementValue = document.getElementById("inputStatus").value;
console.log("selectElementValue: " + selectElementValue);

// check if selectElementValue is something other than "Select a table"
if (selectElementValue === "Select Table") {
  tableName = "webhooks";
} else {
  tableName = selectElementValue;
}

// When the page is loaded partially with ajax, the datatable is not initialized
if (typeof datatable !== "undefined") {
  console.log("datatable defined, destroying datatable");
  datatable.destroy(); // Destroy the previous table
  datatable.off("column-visibility.dt", columnVisibilityHandler);
  console.log("setting signalsTableInitialized to false");
  signalsTableInitialized = false;
}

console.log("Initializing datatable with table: " + tableName);
fetchTableColumnsAndInitialize(tableName);

selectElement = document.getElementById("inputStatus");
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
