var checkbox = document.querySelector("input[id=openSidebarMenu]");
document.addEventListener('click', function (e) {
    e = e || window.event;
    var target = e.target || e.srcElement;
    if ((target.getAttribute("id") != "sidebarMenu" && target.getAttribute("id") != "openSidebarMenu") && document.getElementById("openSidebarMenu").checked == true) {
        document.getElementById("openSidebarMenu").checked = false;
        triggerEvent(checkbox, 'change');
        console.log("CHANGE")
    };
    if (target.getAttribute("id") == "openSidebarMenu" && document.getElementById("openSidebarMenu").checked == false) {
        document.getElementById("openSidebarMenu").checked = false;
        triggerEvent(checkbox, 'change');
        console.log("CHANGE")
    };
}, false);

function triggerEvent(element, eventName) {
    var manualEvent = document.createEvent("HTMLEvents");
    manualEvent.initEvent(eventName, false, true);
    element.dispatchEvent(manualEvent);
}

var div = document.createElement('div');
div.id = 'left-nav-cover';
document.getElementsByTagName('body')[0].appendChild(div);
checkbox.addEventListener('change', function () {
    if (this.checked) {
        div.innerHTML = "<div id='left-nav-cover-inner'></div>";
        console.log("CREATED")
    } else {
        div.removeChild(document.getElementById("left-nav-cover-inner"));
        console.log("REMOVED")
    }
});