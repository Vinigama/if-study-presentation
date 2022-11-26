$( document ).ready(function() {
    setTimeout(function() {
            $('.message').fadeOut('slow');
        }, 1500);
});


function removerHistorico(){
    const request_url_delete = $("#solicita-exclusao-historico").attr("data-url");
    const csrftoken = getCookie('csrftoken');
    alertConfirm('success',
      'Você deseja apagar o seu histórico?',
      () => {
      $.ajax({
        url: request_url_delete,
        type: "POST",
        headers: {'X-CSRFToken': csrftoken},
        success: function(data) {
            var url = $("#url").attr("data-url");
            $('#conteudos').remove();
            document.location.href = url;
        },
        error: function(data) {
            if(data.status == 403){
                alerta("error", "Error", "Não possui conteúdos no seu histórico")
            }
        }
      });  
    });
}

function alerta(icon="success", title, text){
    return Swal.fire({
        heightAuto: false,
        title: title,
        icon: icon,
        text: text,
    })
  }

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function alertConfirm(icon="success", title, callback, params) {
return Swal.fire({
    heightAuto: false,
    title: title,
    showDenyButton: true,
    showCancelButton: false,
    confirmButtonText: 'Prosseguir',
    denyButtonText: `Cancelar`,
}).then((result) => {
    /* Read more about isConfirmed, isDenied below */
    if (result.isConfirmed) {
    return callback(params)
    }
})
}