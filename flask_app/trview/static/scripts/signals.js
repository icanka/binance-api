console.log("signals.js");
let tableName = "webhooks";
// Send AJAX request to Flask server, and return promise
fetch("/api/database/" + tableName)
  .then((response) => response.json())
  .then((data) => {
    // Construct the columns variable
    const columns = data.map((columnName) => ({
      data: columnName,
      searchable: true,
      orderable: true,
    }));
    $(function () {
      initSignalsTable(columns);
    });
    console.log(columns);
  });
