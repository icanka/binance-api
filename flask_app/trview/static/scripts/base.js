const APPLICATION_NAME = "Trview" // Find some cool name for the application
const currentPath = document.location.pathname;
const $currentLink = $('a[href="' + currentPath + '"]');
$currentLink.addClass('active');

const parentLink = $currentLink.parent().parent().siblings().filter('[href="#"]');
parentLink.addClass('active');
parentLink.parent().addClass('menu-is-opening menu-open');
console.log(document.location.pathname);

$('.nav-sidebar').on('expanded.lte.treeview', event => {
    console.log('The treeview was expanded');
    console.log(event.target)
    $(event.target).find('a').addClass('nav-active');
});

$('.nav-sidebar').on('collapsed.lte.treeview', event => {
    $(event.target).find('a').removeClass('nav-active');
});

$(window).on('load.lte.treeview', event => {
    console.log('The treeview initialized.');
    console.log(event.target)
});

const CURRENTLY_ACTIVE_PAGE_MENU_ITEM = '.main-sidebar .nav-item > a.nav-link.active:not([href="#"])';
const SELECTOR_SIDEBAR_MENU_ITEM_NOT_EMPTY = '.main-sidebar .nav-item > a.nav-link:not([href="#"])';
const SELECTOR_SIDEBAR_MENU_ITEM = '.main-sidebar .nav-item > a.nav-link';

$(SELECTOR_SIDEBAR_MENU_ITEM).on('click', function (event) {
    // Prevent the default behavior of the click event
    event.preventDefault();
    // Get the href attribute of the clicked link if it's not '#'
    const hrefValue = $(this).attr('href') !== '#' ? $(this).attr('href') : null;

    if (!hrefValue) {
        return;
    }
    // closest ul with class nav-treeview, our parent.
    //const navTreeview = $(event.target).closest('li.menu-is-opening')
    //console.log(navTreeview);
    //const childLinks = navTreeview.find('a[href="#"]')
    //childLinks.addClass('active')

    const newTitle = ($(this).text().trim())
    const links = $('ul.nav-sidebar').find('a:not([href="#"])');
    const menuLinks = $('ul.nav-sidebar').find('a[href="#"]');
    //console.log(menuLinks);
    menuLinks.removeClass('active')
    links.removeClass('active');
    $(this).addClass('active');
    const parentLink = $(this).parent().parent().siblings().filter('[href="#"]');
    //console.log(parentLink)
    parentLink.addClass('active');

    //$(this).addClass('active').parent().siblings().find('a.nav-link').removeClass('active');
    let url = hrefValue
    // Use the history api to modify the URL in the browser
    console.log('Modifiying the URL');
    let stateObj = { flag: 'dynamic' }
    console.log('pushing state');
    history.pushState(stateObj, null, url);
    console.log(history.length);
    console.log(hrefValue);

    $.ajax({
        url: hrefValue,
        type: 'POST',
        data: { href: hrefValue },
        success: function (data) {
            // load the content and change the page title.
            $('.content-wrapper').html(data);
            document.title = `${newTitle} - ${APPLICATION_NAME}`
            console.log('SUCCESS')
            //console.log(data)
        },
        error: function (xhr, status, error) {
            // Handle errors by logging to the console and displaying a message to the user.
            console.log("Error loading content from URL: " + document.location);
            console.log("Error message: " + error);
            $('.content-wrapper').html("<p>Sorry, there was an error loading this page.</p>");
        }
    });
});

// Listen for popstate events (i.e. back/forward buttons)
window.addEventListener('popstate', function (event) {
    // Use an AJAX request to load the content from the current URL

    console.log("Popstate event detected")
    const state = event.state;
    console.log(state)
    console.log(state.flag)
    // Check if the popped state was added by our code
    console.log("checking the state")
    if (state && state.flag === 'dynamic') {
        event.preventDefault();
        // Get the URL from the popped state object
        console.log("page was loaded dynamically")
        const hrefValue = document.location.pathname;

        // remove all active links
        const links = $('ul.nav-sidebar').find('a:not([href="#"])');
        const menuLinks = $('ul.nav-sidebar').find('a[href="#"]');
        menuLinks.removeClass('active')
        links.removeClass('active nav-active');
        // links.blur();

        // add active link to poppped state.
        const currentPath = document.location.pathname;
        const $currentLink = $('a[href="' + currentPath + '"]');
        $currentLink.addClass('active');

        const parentLinkli = $currentLink.parent().parent().parent();
        const parentLink = $currentLink.parent().parent().siblings().filter('[href="#"]');
        console.log(parentLink)
        if (!parentLinkli.hasClass('menu-open')) { parentLink.trigger('click') }
        //parentLink.click();
        parentLink.addClass('active');
        //parentLink.parent().addClass('menu-is-opening menu-open');

        console.log(`Our URL is: ${hrefValue}`)
        // Load the popped state partially again.
        $.ajax({
            url: hrefValue,
            type: 'POST',
            data: { href: hrefValue },
            success: function (data) {
                // Load the content and change the title.
                $('.content-wrapper').html(data);
                let newTitle = $(`a[href="${hrefValue}"]`).text().trim()
                console.log(`setting page title to ${newTitle}`);
                document.title = `${newTitle} - ${APPLICATION_NAME}`
                //console.log(data)
            },
            error: function (xhr, status, error) {
                // Handle errors by logging to the console and displaying a message to the user.
                console.log("Error loading content from URL: " + document.location);
                console.log("Error message: " + error);
                $('.content-wrapper').html("<p>Sorry, there was an error loading this page.</p>");
            }
        });
    }
    console.log(document.location)
});


let title = $(CURRENTLY_ACTIVE_PAGE_MENU_ITEM).text().trim()
console.log(title)
console.log(`NEW TITLE ${title}`)
if (title !== '') document.title = `${title} - ${APPLICATION_NAME}`

console.log("Connecting to " + "ws://" + window.location.host);
if (typeof socket === "undefined") {
  console.log("socket undefined");
  const socket = io.connect(window.location.host);

  // Set up websocket connection.
  // When the connection is open, send a message to the server
  socket.on("connect", function () {
    // wait 5 seconds before sending the message
    console.log("connected");
    console.log("socket id: " + socket.id);
    //socket.emit("client_connected");
  });

  //socket.on("server_con_ack", function (data) {
  //  console.log("received server_con_ack");
  //});

  // When a messaage is received from the server update the table
  //let dat = JSON.parse(data.data);
  //$("#signals_table").DataTable().ajax.reload();

  //socket.on("update_table", function (data) {
  //  console.log("received update_table");
  //  $("#signals_table").DataTable().ajax.reload();
  //  console.log("table reloaded: " + data);
  //});

  socket.on("disconnect", () => {
    console.log("disconnected");
  });

  socket.on("disconnect", (reason) => {
    console.log("Websocket connection closed: Reason: " + reason);
    if (reason === "io server disconnect") {
      // the disconnection was initiated by the server, you need to reconnect manually
      console.log("io server disconnect");
      //socket.connect();
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