// document.addEventListener('DOMContentLoaded', e => {
//     htmx.logAll();
//     let as = document.querySelectorAll('a');
//     as.forEach(a => {
//         a.addEventListener('click', ee => {
//             ee.preventDefault();
//         })
//     })
// })

// htmx.logAll();

// Dynamic HTML forms based on dropdown menu
$(document).on("change", "#resource_type", function() {
    var resource_type = $(this).val();
    $(".resource_type_input").hide("fast", function() {
        $("#resource_type_" + resource_type).show("slow");
    });
});