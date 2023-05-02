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
      { data: "created", searchable: false },
      { data: "ticker" },
      { data: "strategy_action" },
      { data: "market_position", searchable: false },
      { data: "price", searchable: false },
      { data: "contracts", searchable: false },
      { data: "position_size", searchable: false },
      { data: "market_position_size", searchable: false },
      { data: "order_id", searchable: false },
      { data: "strategy_name"},
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
});
