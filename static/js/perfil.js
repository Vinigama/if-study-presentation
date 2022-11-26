$( document ).ready(function() {
    setTimeout(function() {
        $('.message').fadeOut('slow');
    }, 1500); 

    configuraBotoesMenu()
});


// Faz o set up das opções existentes na aba do canto direito do perfil
function configuraBotoesMenu() {
    perfil_id   = $('.perfil-id').attr('data')
    
    // Verifica se o perfil é do próprio usuário
    $.get(`../../is_owner/${perfil_id}`, function(data) {
      if (data.is_owner) {
            request_url = $('.perfil-id').attr('data-url');
            $('.perfil-menu').
                append(`
                <a href="${request_url}">
                    <button  class="btn bg-cinza-escuro btn-secondary text-dark form-control">
                        <i class="fa fa-edit text-dark" aria-hidden="true"></i> Editar
                    </button>
                </a>
                `)
        }else{
            $('.perfil-menu').
            append(`
                <button class="btn bg-cinza-escuro btn-secondary text-dark form-control" onclick="sinalizar_perfil(this)">
                    <i class="fa fa-flag text-dark" aria-hidden="true"></i> Sinalizar
                </button>
            `)
        }

    });
  }

function sinalizar_perfil(){
    return Swal.fire({
      title: 'Denunciar Perfil',
      showDenyButton: true,
      width: '600px',
      heightAuto: false,
      html: `
      <hr>
      <div class="form-check text-left">
        <input class="form-check-input" type="radio" name="denunciaPerfil" id="radioNome" value="sinalizacoes_nome">
        <label class="form-check-label h5" for="radioNome">
          Nome falso
        </label>
        <br>
        <span class="text-muted">
            Este perfil possui um nome falso
        </span>
      </div>
  
      <div class="form-check text-left mt-2">
        <input class="form-check-input" type="radio" name="denunciaPerfil" id="radioFoto" value="sinalizacoes_foto">
        <label class="form-check-label h5" for="radioFoto">
          Foto de perfil
        </label>
        <br>
        <span class="text-muted">
          Este usuário utiliza uma foto de perfil inadequada
        </span>
      </div>

      <div class="form-check text-left mt-2">
        <input class="form-check-input" type="radio" name="denunciaPerfil" id="radioCondutas" value="sinalizacoes_condutas">
        <label class="form-check-label h5" for="radioCondutas">
          Assédio ou bullying
        </label>
        <br>
        <span class="text-muted">
          Por meio dos comentários este usuário faz condutas de bullying/assédio
        </span>
      </div>
  
      <div class="form-check text-left mt-2">
        <input class="form-check-input" type="radio" name="denunciaPerfil" id="radioDescricao" value="sinalizacoes_descricao">
        <label class="form-check-label h5" for="radioDescricao">
          Descrição do perfil
        </label>
        <br>
        <span class="text-muted">
          Este usuário possui uma descrição negativa
        </span>
      </div>
      `,
      showCancelButton: false,
      confirmButtonText: 'Prosseguir',
      denyButtonText: `Cancelar`,
      preConfirm: () => {
        const opcao = $('input:radio[name="denunciaPerfil"]').is(':checked')
        let dados = $('input[name="denunciaPerfil"]:checked').val()
        if (!opcao) {
          Swal.showValidationMessage(`Selecione alguma das opções acima`)
        }
        return { opcao: dados}
      }
    }).then((result) => {
      /* Read more about isConfirmed, isDenied below */
      if (result.isConfirmed) {
        const csrftoken             = getCookie('csrftoken');
        const request_url_denunciar = $('#perfil-sinalizar').attr('data-url')

        $.ajax({
          url: request_url_denunciar,
          type: "POST",
          headers: {'X-CSRFToken': csrftoken},
          dataType:'json',
          data: {'opcao': result.value.opcao},
          success: function(data) {
            alerta("success", "Sinalização enviada aos Administradores", "Espere a avaliação dos Administradores para a conclusão da sinalização") 
          },
          error: function(xhr) {
              var err = JSON.parse(xhr.responseText); 
              if(xhr.status == 403){
                alerta("error", "Erro na hora de sinalizar", err.msg)
              }
          }
        });
      }
    })  
}

// Modal de alerta 
function alerta(icon="success", title, text){
  return Swal.fire({
    icon: icon,
    title: title,
    text: text,
    heightAuto: false,
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