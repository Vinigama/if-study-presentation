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
            alertConfirm('success','Tem certeza que deseja excluir este conteúdo?')
        }
		else{
			$('#apuracao').submit()
		}	
	}
		
    });

    $('input:radio[name=opcao]').on('click', function(){
        if ($('input:radio[name=opcao]:checked').val() == 'aguardando_edicao'){
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
    }).then((result) => {
      /* Read more about isConfirmed, isDenied below */
      if (result.isConfirmed) {
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