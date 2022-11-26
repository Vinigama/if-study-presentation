function buscar(elem){
    var value       = $(elem).val().toLowerCase();
    let conteudo    = $(elem).closest('.collapse').find('#conteudos h4');
    conteudo.filter(function() {
        $(this).closest('.linha').toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
}


