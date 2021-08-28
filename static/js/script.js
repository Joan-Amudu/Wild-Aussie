/*
    jQuery for MaterializeCSS initialization
*/

$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $('.modal').modal(); // Add Post Modal
    $('.tooltipped').tooltip();
    $('.parallax').parallax();
    $('.dropdown-trigger').dropdown();
    $('select').formSelect();
    $('.datepicker').datepicker({
        format: "dd mmmm, yyyy",
        yearRange: 3,
        showClearBtn: true,
        i18n: {
            done: "Select"
        }

    });
  });