const APPLICATION_NAME = "Trview"; // TODO: Find some cool name for the application
const currentPath = document.location.pathname;
const $currentLink = $('a[href="' + currentPath + '"]');
$currentLink.addClass("active");
const parentLink = $currentLink
  .parent()
  .parent()
  .siblings()
  .filter('[href="#"]');
parentLink.addClass("active");
parentLink.parent().addClass("menu-is-opening menu-open");

// Signals page related variables
let datatable = null;
let hiddenColumns = null;
let col = null;
// const columns = [
//   { data: "ticker", searchable: true, orderable: true },
//   { data: "created", searchable: false, orderable: false },
//   { data: "strategy_action", searchable: true, orderable: false },
//   { data: "market_position", searchable: false, orderable: true },
//   { data: "price", searchable: false, orderable: true },
//   { data: "contracts", searchable: false, orderable: true },
//   { data: "position_size", searchable: false, orderable: true },
//   { data: "market_position_size", searchable: false, orderable: true },
//   { data: "order_id", searchable: false, orderable: false },
//   { data: "strategy_name", searchable: true, orderable: false },
// ];
// end

$(".nav-sidebar").on("expanded.lte.treeview", (event) => {
  $(event.target).find("a").addClass("nav-active");
});

$(".nav-sidebar").on("collapsed.lte.treeview", (event) => {
  $(event.target).find("a").removeClass("nav-active");
});

$(window).on("load.lte.treeview", (event) => {});

const CURRENTLY_ACTIVE_PAGE_MENU_ITEM =
  '.main-sidebar .nav-item > a.nav-link.active:not([href="#"])';
const SELECTOR_SIDEBAR_MENU_ITEM_NOT_EMPTY =
  '.main-sidebar .nav-item > a.nav-link:not([href="#"])';
const SELECTOR_SIDEBAR_MENU_ITEM = ".main-sidebar .nav-item > a.nav-link";

$(SELECTOR_SIDEBAR_MENU_ITEM).on("click", function (event) {
  // Prevent the default behavior of the click event
  event.preventDefault();
  // Get the href attribute of the clicked link if it's not '#'
  const hrefValue = $(this).attr("href") !== "#" ? $(this).attr("href") : null;

  if (!hrefValue) {
    return;
  }

  const newTitle = $(this).text().trim();
  const links = $("ul.nav-sidebar").find('a:not([href="#"])');
  const menuLinks = $("ul.nav-sidebar").find('a[href="#"]');
  menuLinks.removeClass("active");
  links.removeClass("active");
  $(this).addClass("active");
  const parentLink = $(this).parent().parent().siblings().filter('[href="#"]');
  parentLink.addClass("active");

  let url = hrefValue;
  // Use the history api to modify the URL in the browser
  let stateObj = { flag: "dynamic" };
  history.pushState(stateObj, null, url);

  $.ajax({
    url: hrefValue,
    type: "POST",
    data: { href: hrefValue },
    success: function (data) {
      // load the content and change the page title.
      $(".content-wrapper").html(data);
      document.title = `${newTitle} - ${APPLICATION_NAME}`;
    },
    error: function (xhr, status, error) {
      // Handle errors by logging to the console and displaying a message to the user.
      $(".content-wrapper").html(
        "<p>Sorry, there was an error loading this page.</p>"
      );
    },
  });
});

// Listen for popstate events (i.e. back/forward buttons)
window.addEventListener("popstate", function (event) {
  // Use an AJAX request to load the content from the current URL

  const state = event.state;
  // Check if the popped state was added by our code
  if (state && state.flag === "dynamic") {
    event.preventDefault();
    // Get the URL from the popped state object
    const hrefValue = document.location.pathname;

    // remove all active links
    const links = $("ul.nav-sidebar").find('a:not([href="#"])');
    const menuLinks = $("ul.nav-sidebar").find('a[href="#"]');
    menuLinks.removeClass("active");
    links.removeClass("active nav-active");

    // add active link to poppped state.
    const currentPath = document.location.pathname;
    const $currentLink = $('a[href="' + currentPath + '"]');
    $currentLink.addClass("active");

    const parentLinkli = $currentLink.parent().parent().parent();
    const parentLink = $currentLink
      .parent()
      .parent()
      .siblings()
      .filter('[href="#"]');
    if (!parentLinkli.hasClass("menu-open")) {
      parentLink.trigger("click");
    }
    parentLink.addClass("active");

    // Load the popped state partially again.
    $.ajax({
      url: hrefValue,
      type: "POST",
      data: { href: hrefValue },
      success: function (data) {
        // Load the content and change the title.
        $(".content-wrapper").html(data);
        let newTitle = $(`a[href="${hrefValue}"]`).text().trim();
        document.title = `${newTitle} - ${APPLICATION_NAME}`;
      },
      error: function (xhr, status, error) {
        // Handle errors by logging to the console and displaying a message to the user.
        $(".content-wrapper").html(
          "<p>Sorry, there was an error loading this page.</p>"
        );
      },
    });
  }
});

let title = $(CURRENTLY_ACTIVE_PAGE_MENU_ITEM).text().trim();
if (title !== "") document.title = `${title} - ${APPLICATION_NAME}`;

const namespaceSockets = ["webhook_signal"];

namespaceSockets.forEach((socket) => {
  if (typeof window[socket] === "undefined") {
    console.log("Namespace socket undefined: ", socket);
    window[socket] = io.connect(window.location.host + "/" + socket);
    let _socket = window[socket];
    _socket.on("connect", function () {
      console.log(socket + " connected");
    });
    _socket.on("disconnect", () => {
      console.log(socket + " disconnected");
    });
    _socket.on("disconnect", (reason) => {
      console.log(_socket + ": connection closed: reason: " + reason);
      if (reason === "io server disconnect") {
        // the disconnection was initiated by the server, you need to reconnect manually
        console.log(_socket + ": io server disconnect");
      }
    });
    _socket.on("connect_error", (error) => {
      console.log(_socket + ": connect_error: " + error);
    });
    _socket.io.on("reconnect_attempt", () => {
      console.log(_socket + ": reconnect_attempt");
    });
    _socket.io.on("reconnect", () => {
      console.log(_socket + ": reconnected");
    });
    _socket.on("update_table", function (data) {
      console.log("received update_table event");
      $("#signals_table").DataTable().ajax.reload(); // reload table
      console.log("table #signals_table reloaded: " + data);
    });
  } else {
    console.log("Namespace socket already defined: ", socket);
  }
});

if (typeof rootSocket === "undefined") {
  console.log("rootSocket undefined");
  const rootSocket = io.connect(window.location.host);

  // Set up websocket connection.
  // When the connection is open, send a message to the server
  rootSocket.on("connect", function () {
    // wait 5 seconds before sending the message
    console.log("rootSocket connected");
    //socket.emit("client_connected");
  });

  // When a messaage is received from the server update the table
  //let dat = JSON.parse(data.data);
  //$("#signals_table").DataTable().ajax.reload();

  //socket.on("update_table", function (data) {
  //  console.log("received update_table");
  //  $("#signals_table").DataTable().ajax.reload();
  //  console.log("table reloaded: " + data);
  //});

  rootSocket.on("disconnect", () => {
    console.log("rootSocket disconnected");
  });

  rootSocket.on("disconnect", (reason) => {
    console.log("rootSocket connection closed: Reason: " + reason);
    if (reason === "io server disconnect") {
      // the disconnection was initiated by the server, you need to reconnect manually
      console.log("io server disconnect");
      //socket.connect();
    }
    // else the socket will automatically try to reconnect
  });

  rootSocket.on("connect_error", (error) => {
    console.log("connect_error");
    console.log(error);
  });
  rootSocket.io.on("reconnect_attempt", () => {
    console.log("rootSocket reconnect_attempt");
  });

  rootSocket.io.on("reconnect", () => {
    console.log("rootSocket reconnected");
    console.log("rootSocket id: " + rootSocket.id);
  });
} else {
  console.log("rootSocket already defined");
}

// Signals related functions

// function getTableColumns(tableName) {
//   // Send AJAX request to Flask server
//   let columns = null;
//   // Send AJAX request to Flask server, and return promise
//   fetch("/api/database/" + tableName)
//     .then((response) => response.json())
//     .then((data) => {
//       // Construct the columns variable
//       columns = data.map((columnName) => ({
//         data: columnName,
//         searchable: true,
//         orderable: true,
//       }));
//       return columns;
//       console.log(columns);
//     });
// }

function initSignalsTable(columns) {
  console.log("initSignalsTable");
   // access the columns variable in the promise
  datatable = $("#signals_table").DataTable({
    ajax: "/webhook/api/data/webhooks",
    processing: true,
    serverSide: true,
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
    console.log("invalidating rows");
    datatable.rows().invalidate();
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


const selectElement = document.getElementById('inputStatus');

// Event listener for the 'change' event
selectElement.addEventListener('change', (event) => {
  const selectedTable = event.target.value;
  // Handle the selected table here
  console.log('Selected table:', selectedTable);
});
// END - Signals related functions
