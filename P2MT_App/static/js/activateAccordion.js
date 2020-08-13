function activateAccordion(data_id) {
    var x = document.querySelectorAll("[data-identifier=" + data_id + "]");
    for (i = 0; i < x.length; i++) {
        if (x[i].style.visibility == "collapse") {
            x[i].style.visibility = "visible";
        } else {
            x[i].style.visibility = "collapse";
        }
    }
}