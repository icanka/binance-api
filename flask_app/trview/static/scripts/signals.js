

console.log("signals.js");
$(function () {
  datatable = $("#signals_table").DataTable({
    ajax: "/webhook/api/data/webhooks",
    processing: true,
    serverSide: true,
    columns: _columns,
    responsive: true,
    lengthChange: true,
    lengthMenu: [
      [10, 25, 50, 100, 500],
      [10, 25, 50, 100, 500],
    ],
    dom:
      "<'row'<'col-sm-12 col-md-2'l><'col-sm-12 col-md-6'B><'col-sm-12 col-md-4'f>>" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
    autoWidth: false,
    searching: true,
    deferRender: true,
    searchDelay: 5000,
    paging: true,
    buttons: [
      { extend: "copy", exportOptions: { columns: [":visible"] } },
      { extend: "csv", exportOptions: { columns: [":visible"] } },
      { extend: "excel", exportOptions: { columns: [":visible"] } },
      { extend: "pdf", exportOptions: { columns: [":visible"] } },
      { extend: "print", exportOptions: { columns: [":visible"] } },
      {
        extend: "collection",
        text: "Export All Data",
        collectionLayout: "dropdown",
        buttons: [
          {
            text: "CSV",
            action: function () {
              let visibleCols = $("#signals_table")
                .DataTable()
                .columns(":visible")
                .indexes()
                .toArray();
              $.ajax({
                url: "/webhook/api/export",
                type: "GET",
                dataType: "text",
                data: {
                  format: "csv",
                  table_name: "webhooks",
                  //columns: visibleCols.join(","),
                },
                success: function (data) {
                  let blob = new Blob([data], {
                    type: "text/csv;charset=utf-8;",
                  });
                  saveAs(blob, "signals.csv");
                },
              });
            },
          },
        ],
      },
      "colvis",
    ],
  });

//  datatable.on("search.dt", function () {
//    console.log("search.dt");
//    hiddenColumnsIndexes = getHiddenColumns();
//    console.log(hiddenColumns);
//    console.log(datatable.settings()[0].aoData);
//  });

  datatable.on("column-visibility.dt", function (e, settings, column, state) {
    // If the column is hidden, set the column's searchable property to false.
    if (state == false) {
      console.log("column is not visible");
      aoColumn = settings.aoColumns.at(column);
      aoColumn.bSearchable = false;
    }
    // If the column is visible set the column's searchable property to its' original value.
    else if (state == true) {
      console.log("column is visible");
      aoColumn = settings.aoColumns.at(column);
      aoColumn.bSearchable = columns[column].searchable;
    }
    console.log("invalidating rows")
    datatable.rows().invalidate();
  });
});


// Hack to only search through visible columns.
// Developed on 1.10.18 DataTables version.
function searchOnlyVisibleColumns(dt) {
  let updateSearchableProperties = function (dt) {
    // These columns are never searchable (customize to your needs)
    //var notSearchableColumns = [
    //    "order", "active", "visible", "required", "edit"
    //];
    var hiddenColumnsIndexes = getHiddenColumns();

    //var visibleColumnsIndexes = [];
    // Get indexes of all visible columns
    //dt.columns(":visible").every(function(colIdx) {
    //    visibleColumnsIndexes.push(colIdx);
    //});

    // Modify <a href="//legacy.datatables.net/ref#bSearchable">bSearchable</a> property in DataTable.settings.aoColumns[]
    let settings = dt.settings()[0];
    settings.aoColumns.forEach(function (aoColumn) {
      let notSearchable = hiddenColumns.indexOf(aoColumn.idx) != -1;

      if (notSearchable) {
        console.log(aoColumn.data + " is not searchable")
        aoColumn.bSearchable = false;
      }
    });

    // Invalidate all rows
    // This will cause to regenerate _aFilterData and _sFilterRow in DataTable.settings.aoData[]
    // _sFilterRow is used when searching the table
    dt.rows().invalidate();

    // (Optional) simulate search input change to re-filter rows using new columns settings
    //settings.oPreviousSearch.sSearch = "";
    //var $table = $(dt.containers()[0]);
    //var $input = $table.find('input[type=search]');
    //$input.keyup();
  };

  // Run on column visibility change
  dt.on('column-visibility.dt', function (e, settings, column, state) {
    updateSearchableProperties(dt);
  });
  // First run
  updateSearchableProperties(dt);
}
