$('#input_search_text').focus()
$('#input_submit_text').bind('click',function () {
    var elem = $('#input_search_text')
    if (elem.val()==""){
        elem.focus()
    }else {
        $('#search_form').submit()
    }
})