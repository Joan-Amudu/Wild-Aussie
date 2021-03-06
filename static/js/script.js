/*
    jQuery for MaterializeCSS initialization
*/

$(document).ready(function(){
    
    $('.sidenav').sidenav({edge: "right"});
    $('.modal').modal(); 
    $('.tooltipped').tooltip();
    $('.parallax').parallax();
    $('.dropdown-trigger').dropdown();
    $('select').formSelect();
    $('.tabs').tabs();    
    $('.datepicker').datepicker({
        format: "dd mmmm, yyyy",
        yearRange: 3,
        showClearBtn: true,
        i18n: {
            done: "Select"
        }

    });


  });
/*
30 Seconds Time out function for flash messages
*/
  setTimeout(function() {
    $('#flashmessage').fadeOut('fast');
}, 30000);