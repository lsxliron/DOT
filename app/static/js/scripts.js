$(document).ready(function(){
    $('#rainDropdown ul li a').on('click', function(){
        $('#rainDropdownButton').html($(this).text() + '<span class="caret"></span>')
    });

    //CREATE DATE PICKERS
    $.each(['startDate', 'endDate'], function(i, d){
        $('#'+d).datetimepicker({
            format: 'MM-DD-YYYY',
            minDate: moment("01/01/1900", "MM-DD-YYYY"),
        })
    });




    //CREATE TIME PICKERs
    $.each(['startTime', 'endTime'], function(i, d){
        $('#'+d).datetimepicker({
            format:"hh:mm:ss"
        })
        .on('dp.change', function(){
            st = $('#startTimeInput').val()
            et = $('#endTimeInput').val()
            if (st && et){
                validDelta = validateTimeDelta(st,et)
                if (validDelta){
                    $('#startTimeInput').parent('div').addClass('has-success').removeClass('has-error')
                    $('#endTimeInput').parent('div').addClass('has-success').removeClass('has-error')
                }
                else{
                    if (!($('#startDateInput').val() != $('#endDateInput').val())){
                        $('#startTimeInput').parent('div').removeClass('has-success').addClass('has-error')
                        $('#endTimeInput').parent('div').removeClass('has-success').addClass('has-error')
                    }
                }
            }
        })
    });
    

     $('#startDate').on('dp.change', function(){
        minDateValue = $('#startDate').data("DateTimePicker").viewDate()
        minDateValue.format('mm-dd-yyyy')
        if (minDateValue){
            console.log(minDateValue.toDate())
            $('#endDate').data('DateTimePicker').minDate(minDateValue.toDate());
        }
    });
    
    $('#clearButton').on('click',clearForm)
}); //END DOCUMENT READY


function clearForm(){
    $('#locationInput').val('');
    $('#rainDropdownButton').html("All <span class='caret'></span>");
    $('#limitInput').val('');
    
    $('#startDateInput').val('')
    $('#startDateInput').parent('div').removeClass('has-error').removeClass('has-success')
    $('#endDateInput').val('')
    $('#endDateInput').parent('div').removeClass('has-error').removeClass('has-success')
    $('#startTimeInput').val('')
    $('#startTimeInput').parent('div').removeClass('has-error').removeClass('has-success')
    $('#endTimeInput').val('')
    $('#endTimeInput').parent('div').removeClass('has-error').removeClass('has-success')
}

function validateDatesDelta(sd, ed){
    startDate = moment(sd, 'mm/dd/yyyy');
    endDate = moment(ed, 'mm/dd/yyyy');
    if (endDate - startDate < 0)
        return false;
    return true;
}

function validateTimeDelta(st, et){
    startTime = moment(st, 'hh:mm:ss');
    endTime = moment(et, 'hh:mm:ss');
    if (endTime - startTime < 0)
        return false;
    return true;
}

