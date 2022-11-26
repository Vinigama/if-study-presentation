$( document ).ready(function() {
    setTimeout(function() {
            $('.message').fadeOut('slow');
        }, 1500); 

    $('.enviar').on('click', function(e) {
        e.preventDefault();
        let check = $('input[name=opcao]:checked')
        if (check.val()){
        const csrftoken = getCookie('csrftoken');
        if(check.val() == 'excluir'){
            alertConfirm('success','Tem certeza que deseja excluir este perfil?')
        }
        else if(check.val() == 'silenciar'){
            let html = `
            <hr>         
                <div class="tempo">
                    <div class="form-check text-left mt-2">
                    <input class="form-check-input" type="radio" name="tempoOpcao" id="radioMedio" value="prazo_medio">
                    <label class="form-check-label h5" for="radioMedio">
                        15 Dias
                    </label>
                    <br>
                    <span class="text-muted">
                        Silenciar este perfil por 15 dias
                    </span>
                    </div>
            
                    <div class="form-check text-left mt-2">
                    <input class="form-check-input" type="radio" name="tempoOpcao" id="radioGrande" value="prazo_grande">
                    <label class="form-check-label h5" for="radioGrande">
                        30 Dias
                    </label>
                    <br>
                    <span class="text-muted">
                        Silenciar este perfil por 30 dias
                    </span>
                    </div>
                </div>
            `
            alertConfirm('success', "Escolha o tempo", null, null, html)
        }else{
            $('#apuracao').submit()
        }
    }  
    });

    $('input:radio[name=opcao]').on('click', function(){
        if ($('input:radio[name=opcao]:checked').val() == 'notificacao'){
            let text = `
            <div class="row text-area">
                <div class="col-md-12">
                    <div class="form-group">
                        <label class="h4">Enviar Notificação</label>
                        <textarea class="form-control" id="input-textarea" name="input-textarea" onkeyup="textArea(this)" placeholder="Envie uma notificação para o aluno" id="input-textarea" rows="3"></textarea>
                    </div>
                </div>
            </div>   
            `
            $('.form-group-text').empty().append(text)
            $('.enviar').prop('disabled', true)

        }
        else{
            $('.text-area').remove()
            $('.enviar').prop('disabled', false)
        }
    })

});

function textArea(elem){
    if ($(elem).val().length > 0) {
        $('.enviar').prop('disabled', false)
    }else{
        $('.enviar').prop('disabled', true)
    }
}

function alertConfirm(icon="success", title, confirmButtonText='Deletar', confirmButtonColor="#cc3f44", html=null) {
    return Swal.fire({
        title: title,
        showDenyButton: true,
        showCancelButton: false,
        confirmButtonText: confirmButtonText,
        denyButtonText: `Cancelar`,
        confirmButtonColor: confirmButtonColor,
        denyButtonColor: "#808080",
        confirmButtonText: 'Prosseguir',
        html: html,
        preConfirm: () => {
            if ($('.tempo').length != 0){
                const opcao = $('input:radio[name="tempoOpcao"]').is(':checked')
                let dados = $('input[name="tempoOpcao"]:checked').val()
                if (!opcao) {
                    Swal.showValidationMessage(`Selecione alguma das opções acima`)
                }
                return { opcao: dados}                
            }
        }
    }).then((result) => {
      /* Read more about isConfirmed, isDenied below */
      if (result.isConfirmed) {
            $('#apuracao').append(`<input type="hidden" name="opcaoTempo" value="${result.value.opcao}" class="mt-1">`)
            $('#apuracao').submit()
      }
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