/*
# @name: main.js
# @version: 0.1
# @creation_date: 2022-04-07
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: JavaScript functions for various functions
# @acknowledgements:
*/

// Dynamic HTML forms based on dropdown menu
$("#resource_type").change(function() {
    var $ = jQuery.noConflict();
    var resource_type = $(this).val();
    $(".resource_type_input").hide("fast", function() {
        $("#resource_type_" + resource_type).show("slow");
    });
});

// Testing a couple of ways to expand text
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})
