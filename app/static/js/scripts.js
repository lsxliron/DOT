$(document).ready(function(){
    $('#rainDropdown ul li a').on('click', function(){
        $('#rainDropdownButton').html($(this).text() + '<span class="caret"></span>')
        
    })
})