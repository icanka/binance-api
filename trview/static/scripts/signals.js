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
        ajax: '/webhook/api/data/webhooks',
        columns: [
            { data: 'created' },
            {data: 'ticker'},
            { data: 'strategy_action' },
            { data: 'market_position' },
            { data: 'price' },
            { data: 'strategy_name' }
        ],
        responsive: true,
        lengthChange: false,
        autoWidth: false,
        paging: true,
        buttons: ["copy", "csv", "excel", "pdf", "print", "colvis"],
    }).buttons().container().appendTo("#signals_table_wrapper .col-md-6:eq(0)");
});
