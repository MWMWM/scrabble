$(document).ready(function(){
    $('#id_how').change(function(){
    var option = $('#id_how').val();
    if (option == 3){
        $('#id_where').css('display', 'block');
        $('label[for="id_where"]').css('display', 'block');
    }
    else{
        $('label[for="id_where"]').css('display', 'none');
    }
});
});
