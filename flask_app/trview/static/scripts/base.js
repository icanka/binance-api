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

$(".nav-sidebar").on("expanded.lte.treeview", (event) => {
  $(event.target).find("a").addClass("nav-active");
});

$(".nav-sidebar").on("collapsed.lte.treeview", (event) => {
  $(event.target).find("a").removeClass("nav-active");
});

$(window).on("load.lte.treeview", (event) => { });

const CURRENTLY_ACTIVE_PAGE_MENU_ITEM =
  '.main-sidebar .nav-item > a.nav-link.active:not([href="#"])';
const SELECTOR_SIDEBAR_MENU_ITEM_NOT_EMPTY =
  '.main-sidebar .nav-item > a.nav-link:not([href="#"])';
const SELECTOR_SIDEBAR_MENU_ITEM = ".main-sidebar .nav-item > a.nav-link";

$(SELECTOR_SIDEBAR_MENU_ITEM).on("click", function (event) {
  console.log("sidebar menuitem clicked");
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

  console.log("Loading content");
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
  console.log("Content loaded");
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

// ----------- SOCKET IO ----------------

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
