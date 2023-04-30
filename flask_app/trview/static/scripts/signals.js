// $(function () {
//   $("#signals_table")
//     .DataTable({
//       responsive: true,
//       lengthChange: false,
//       autoWidth: false,
//       paging: true,
//       buttons: ["copy", "csv", "excel", "pdf", "print", "colvis"],
//     })
//     .buttons()
//     .container()
//     .appendTo("#signals_table_wrapper .col-md-6:eq(0)");

//   // $('#example2').DataTable({
//   //     "paging": true,
//   //     "lengthChange": false,
//   //     "searching": false,
//   //     "ordering": true,
//   //     "info": true,
//   //     "autoWidth": false,
//   //     "responsive": true,
//   // });
// });
$(function () {
  $("#signals_table").DataTable({
    ajax: "/webhook/api/data/webhooks",
    processing: true,
    serverSide: true,
    columns: [
      //{ data: "id" },
      { data: "created" },
      { data: "ticker", searchable: false },
      { data: "strategy_action" },
      { data: "market_position", searchable: false },
      { data: "price" },
      { data: "contracts" },
      { data: "position_size" },
      { data: "market_position_size" },
      { data: "order_id", searchable: false },
      { data: "strategy_name" },
    ],
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
});

console.log("Connecting to " + "ws://" + window.location.host);
console.log("socket: " + socket);
if (typeof socket === "undefined") {
  console.log("socket undefined");
  var socket = io.connect(window.location.host);

  // Set up websocket connection.
  // When the connection is open, send a message to the server
  socket.on("connect", function () {
    // wait 5 seconds before sending the message
    console.log("connected");
    console.log("socket id: " + socket.id);
    socket.emit("client_connected");
  });

  socket.on("server_con_ack", function (data) {
    console.log("received server_con_ack");
  });

  // When a messaage is received from the server update the table
  //let dat = JSON.parse(data.data);
  //$("#signals_table").DataTable().ajax.reload();

  socket.on("update_table", function (data) {
    console.log("received update_table");
    $("#signals_table").DataTable().ajax.reload();
    console.log("table reloaded: " + data);
  });

  socket.on("disconnect", () => {
    console.log("disconnected");
  });

  socket.on("disconnect", (reason) => {
    console.log("disconnect");
    if (reason === "io server disconnect") {
      // the disconnection was initiated by the server, you need to reconnect manually
      console.log("io server disconnect");
      socket.connect();
    }
    // else the socket will automatically try to reconnect
  });

  socket.on("connect_error", (error) => {
    console.log("connect_error");
    console.log(error);
  });
  socket.io.on("reconnect_attempt", () => {
    console.log("reconnect_attempt");
  });

  socket.io.on("reconnect", () => {
    console.log("reconnect");
    console.log("socket id: " + socket.id);
  });
} else {
  console.log("socket already defined");
}
