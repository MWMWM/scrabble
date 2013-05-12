$(document).ready(function(){
    $('#id_how').bind('click', function(){
    var option = $('#id_how').val()
    if (option == 3){
        $('#id_where').show()
        $('label[for="id_where"]').show()
    }
    else{
        $('#id_where').hide()
        $('label[for="id_where"]').hide()
    }
})
})
