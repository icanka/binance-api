
// --------------- DATATABLES ----------------
// Signals page related variables
let datatable = null;
let selectElement = null;
let cols = null;
let signalsTableInitialized = false;
let hiddenColumns = null;
let col = null;

function columnVisibilityHandler(e, settings, column, state) {
    // If the column is hidden, set the column's searchable property to false.
    console.log(cols);
    if (state == false) {
      console.log("column is not visible");
      aoColumn = settings.aoColumns.at(column);
      aoColumn.bSearchable = false;
    }
    // If the column is visible set the column's searchable property to its' original value.
    else if (state == true) {
      console.log("column is visible");
      aoColumn = settings.aoColumns.at(column);
      aoColumn.bSearchable = cols[column].searchable;
    }
    console.log("invalidating rows");
    datatable.rows().invalidate();
  }
  
  function initSignalsTable(columns, tableName) {
    cols = columns;
    // access the columns variable in the promise
    datatable = $("#signals_table").DataTable({
      ajax: "/webhook/api/data/" + tableName,
      processing: true,
      serverSide: true,
      destroy: true,
      columns: columns,
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
      searchDelay: 2000,
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
                    table_name: tableName,
                    //columns: visibleCols.join(","),
                  },
                  success: function (data) {
                    let blob = new Blob([data], {
                      type: "text/csv;charset=utf-8;",
                    });
                    saveAs(blob, tableName + ".csv");
                  },
                });
              },
            },
          ],
        },
        "colvis",
      ],
    });
  
    datatable.on("column-visibility.dt", columnVisibilityHandler);
  }
  
  function replaceTableHeader(columns) {
    let signalsTable = $("#signals_table");
    signalsTable.find("thead, tfoot").remove();
  
    const thead = $("<thead>");
    const tfoot = $("<tfoot>");
    const tr = $("<tr>");
  
    columns.forEach((column) => {
      const th = $("<th>", {
        text: column.data,
      });
      tr.append(th);
    });
  
    thead.append(tr);
    tfoot.append(tr.clone());
    console.log("Appending: " + thead);
    signalsTable.append(thead);
    signalsTable.append(tfoot);
  }
  
  function fetchTableColumnsAndInitialize(tableName) {
    fetch("/api/database/" + tableName)
      .then((response) => response.json())
      .then((data) => {
        const columns = data.map((columnName) => ({
          data: columnName,
          searchable: true,
          orderable: true,
        }));
  
        console.log(columns);
        replaceTableHeader(columns);
  
        $(function () {
          console.log("Initializing signals table");
          if (!signalsTableInitialized) {
            initSignalsTable(columns, tableName);
            signalsTableInitialized = true;
          }
        });
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
  
  function getHiddenColumns() {
    let hiddenColumns = [];
    datatable.columns().every(function () {
      let columnIndex = this.index();
      let visible = this.visible();
      if (!visible) {
        hiddenColumns.push(columnIndex);
      }
    });
    return hiddenColumns;
  }
  
  // ----- NOT USED -----
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
          console.log(aoColumn.data + " is not searchable");
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
    dt.on("column-visibility.dt", function (e, settings, column, state) {
      updateSearchableProperties(dt);
    });
    // First run
    updateSearchableProperties(dt);
  }
  
  // ----- NOT USED -----
  function getTableColumns(tableName) {
    // Send AJAX request to Flask server
    let columns = null;
    // Send AJAX request to Flask server, and return promise
    fetch("/api/database/" + tableName)
      .then((response) => response.json())
      .then((data) => {
        // Construct the columns variable
        columns = data.map((columnName) => ({
          data: columnName,
          searchable: true,
          orderable: true,
        }));
        return columns;
      });
  }
  