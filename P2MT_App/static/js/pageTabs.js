// Tabs for pages
// Based on example here: https://www.w3schools.com/w3css/w3css_tabulators.asp
// Requires HTML elements defined as in these examples:
// 
// <div class="w3-bar w3-blue">
// <button class="w3-bar-item w3-button tablink w3-black" onclick="openTab(event, 'StudentInfoTab')">StudentInfo</button>
// <button class="w3-bar-item w3-button tablink" onclick="openTab(event, 'StaffInfoTab')">Staff Info</button></div>
// 
// <div class="infoTab" id="StudentInfoTab">
// <div class="infoTab" id="StaffInfoTab" style="display:none">
// 

function openTab(evt, infoTabName) {
    var i, x, tablinks;
    x = document.getElementsByClassName("infoTab");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < x.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" w3-black", "");
    }
    document.getElementById(infoTabName).style.display = "block";
    evt.currentTarget.className += " w3-black";
}