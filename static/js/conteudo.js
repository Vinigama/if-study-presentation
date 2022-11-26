$(document).ready(function() {  
    // Função que quando clica no botão dislike, aplica um visual interativo mostrando que foi clicado no button dislike
    $('.dislike-conteudo').click(function(){

      // adicionar no banco o dislike conteudo
      adicionarDislikeConteudo()  

      let botaoDislike   = $(this).find('.fa-thumbs-down');
      let botaoLike      = $('.like-conteudo').find('.fa-thumbs-up');
      $like              = $('.quantidade-like-conteudo');
      $dislike           = $('.quantidade-dislike-conteudo');

      botaoDislike.toggleClass('fas far');

      if(botaoLike.hasClass('fas')){
        botaoLike.toggleClass('fas far');
        $like.text(function(idx, txt) {
          return( (+txt == 0) ? 0 : (+txt - 1));
        });
      }
      
      if(botaoDislike.hasClass('far')){
        $dislike.text(function(idx, txt) {
          return( (+txt == 0) ? 0 : (+txt - 1));
        });
      }
      else{
        $dislike.text(function(idx, txt) {
          return +txt + 1;
        });
      }
    });

    // Função que quando clica no botão like, aplica um visual interativo mostrando que foi clicado no button like
    $('.like-conteudo').click(function(){

    // adicionar no banco o like conteudo
    adicionarLikeConteudo();

    let botaoLike         = $(this).find('.fa-thumbs-up');
    let botaoDislike      = $('.dislike-conteudo').find('.fa-thumbs-down');
    $like              = $('.quantidade-like-conteudo');
    $dislike           = $('.quantidade-dislike-conteudo');

    botaoLike.toggleClass('fas far');

    if(botaoDislike.hasClass('fas')){
      botaoDislike.toggleClass('fas far');
      $dislike.text(function(idx, txt) {
        return( (+txt == 0) ? 0 : (+txt - 1));
      });
    }

    if(botaoLike.hasClass('far')){
      $like.text(function(idx, txt) {
        return( (+txt == 0) ? 0 : (+txt - 1));
      });
    }
    else{
      $like.text(function(idx, txt) {
        return +txt + 1;
      });
    }
    });

    // Função que quando digita na barra de comentário, ativa o button enviar
    $("#input-comentario").keyup(function() {
      if($(this).val().length > 0){
        $('#enviar_comentario').prop('disabled', false);
      }else{
        $('#enviar_comentario').prop('disabled', true);
      }
    });

    // Após apertar enter no input comentário e realizado a função de envio do comentário
    $('#input-comentario').keydown(function(event) {
      if (event.keyCode == 13) {
        enviarComentario();
        event.preventDefault();
      }
    });

    $(".show-hide-btn").click(function() {
      var id = $(this).data("id");
      $("#half-" + id).toggle();//hide/show..
      $("#full-" + id).toggle();
    })

    configuraBotoesMenu();
}); 


// quando algo for digitado no input resposta, o botão de enviar será ativado
function respostaKeyUp(elem){
  let botao = $(elem).closest('.row').find('.enviar_resposta');
  if($(elem).val().length > 0){
    botao.prop('disabled', false);
  }else{
    botao.prop('disabled', true);
  }
}

// Quando apertar o botão enter no input resposta, será enviado para banco e adicionado um card resposta
function pressEnter(event, elem){
  let botao = $(elem).closest('.row').find('.enviar_resposta');
  if (event.keyCode == 13) {
    enviarResposta(botao);
    event.preventDefault();
  }
};

    
// Envio do comentário
function enviarComentario(){
  var char            = $('#input-comentario').val();
  let botaoEnviar     = $('#enviar_comentario');
  let inputComentario = $("#input-comentario");

  if(char.length > 255){
    var text = "O tamanho de caracteres excede o tamanho proposto";
    $('#input-comentario').val('');
    alertaComentario(text)
  }
  else if(char.length == 0){
    var text = "O input comentário está vázio";
    alertaComentario(text);
  }
  else{
    const usuario     = $('.usuario').attr('value');
    const comentario  = inputComentario.val();

    //Envio dos dados
    const csrftoken = getCookie('csrftoken');
    $.ajax({
      url: '../../post_comentario/',
      type: "POST",
      headers: {'X-CSRFToken': csrftoken},
      data: {
        'comentario': comentario,
        'conteudo': conteudoId,
      },
      success: function(data) {
        aumentarComentario();
        adicionarComentario(comentario, usuario, data.comentarioId, data.perfil, data.perfil_id);
        botaoEnviar.prop('disabled', true);
        inputComentario.val(""); 
      },
      error: function(data) {
        if(data.status == 403){
          var data = JSON.parse(data.responseText); 
          alerta("error", data.title, data.msg)
        }
      }
    });
  }
}

// Adicionar card comentário dinamicamente
function adicionarComentario(comentario, usuario, comentarioId, foto, perfil_id){
  var comentario = htmlEncode(comentario);
  var cardComentario = `
    <div class="card card-comentario ml-2 mt-4" value="` + comentarioId  + `">
      <div class="row ml-2">
          <img src="`+foto+`" alt="Foto de Perfil"  class="foto-perfil-comentario">
          <div class="col-md-11 col-sm-9">
              <div class="row justify-content-between">
                  <a href="../../../perfil/`+perfil_id+`">
                    <h5 class="card-title ml-3">` + usuario + `</h5>
                  </a>
                  <button  class="btn bg-cinza-escuro btn-secondary" onclick="deletarComentario(this, `+comentarioId+`); this.onclick=null;">
                    <i class="fa fa-trash text-dark" aria-hidden="true"></i>
                  </button>
              </div>
              
              <p class="card-text mb-2">
              ` + comentario + ` 
              </p>
              <div class="d-inline-flex">
                <div class="p-2">
                  <i class="far fa-thumbs-up like" onclick="likeComentario(this)" title="Gostei"></i>
                  <span class="quantidade-like-comentario" value="0">0</span>
                </div>
                <div class="p-2">
                  <i class="far fa-thumbs-down dislike" onclick="dislikeComentario(this)" title="Não gostei"></i>
                  <span class="quantidade-dislike-comentario" value="0">0</span>
                </div>
                <div class="p-2">
                  <h6 class="card-title responder" onclick="responder(this); this.onclick=null;">Responder</h6>
                </div>
              </div>
              <div class="resposta">
              </div>
              <div class="respostas mt-1 ml-3">
              </div>
        </div>
    </div>
  `;
  $('#secao-comentario').prepend(cardComentario);
};

// Modal de alerta de comentário
function alertaComentario(text){
  return Swal.fire({
    icon: 'error',
    title: 'Não foi possível enviar o comentário',
    text: text,
  })
}


// Função para vincular o like do conteúdo ao usuário
function adicionarLikeConteudo(){
  url   = 'post_like_conteudo'
  data  = {'conteudo_id': conteudoId}
  ajaxSend(data, url)
}

// Função para vincular o dislike do conteúdo ao usuário
function adicionarDislikeConteudo(){
  url   = "post_dislike_conteudo";
  data  = {'conteudo_id': conteudoId};
  ajaxSend(data, url)
}

// Função para adicionar o like no comentário
function likeComentario(elem){
  const comentario        = $(elem).closest('.card-comentario').attr('value');

  const botaoLike         = $(elem).closest('.d-inline-flex').find('.fa-thumbs-up');
  const botaoDislike      = $(elem).closest('.d-inline-flex').find('.fa-thumbs-down');

  const quantidadeLike    = $(elem).closest('.d-inline-flex').find('.quantidade-like-comentario');
  const quantidadeDislike = $(elem).closest('.d-inline-flex').find('.quantidade-dislike-comentario');

  // função para habilitar o visual do like e do dislike
  dinamicoLike(botaoLike, botaoDislike, quantidadeLike, quantidadeDislike);

  url   = 'post_like';
  data  =  {'comentario_id': comentario}

  // Vincular o usuário que clicou no like com o comentário
  ajaxSend(data, url);

};

// Função para adicionar o dislike no comentário
function dislikeComentario(elem){
  const comentario    = $(elem).closest('.card-comentario').attr('value');

  const botaoLike     = $(elem).closest('.d-inline-flex').find('.fa-thumbs-up');
  const botaoDislike  = $(elem).closest('.d-inline-flex').find('.fa-thumbs-down');

  const quantidadeLike    = $(elem).closest('.d-inline-flex').find('.quantidade-like-comentario');
  const quantidadeDislike = $(elem).closest('.d-inline-flex').find('.quantidade-dislike-comentario');

  // função para habilitar o visual do like e do dislike
  dinamicoDislike(botaoLike, botaoDislike, quantidadeLike, quantidadeDislike);

  url   = 'post_dislike';
  data  =  {'comentario_id': comentario}

  // Vincular o usuário que clicou no like com o conteúdo
  ajaxSend(data, url);
};

// Alteração de formato do botão do dislike e acréscimo e decréscimo do mesmo
function dinamicoDislike(botaoLike, botaoDislike, quantidadeLike, quantidadeDislike){
  botaoDislike.toggleClass('fas far');

  if(botaoLike.hasClass('fas')){
    botaoLike.toggleClass('fas far');
    quantidadeLike.text(function(idx, txt) {
      return( (+txt == 0) ? 0 : (+txt - 1));
    });
  }
  
  if(botaoDislike.hasClass('far')){
    quantidadeDislike.text(function(idx, txt) {
      return( (+txt == 0) ? 0 : (+txt - 1));
    });
  }
  else{
    quantidadeDislike.text(function(idx, txt) {
      return +txt + 1;
    });
  }
};

// Alteração de formato do botão do like e acréscimo e decréscimo do mesmo
function dinamicoLike(botaoLike, botaoDislike, quantidadeLike, quantidadeDislike){
  botaoLike.toggleClass('fas far');

  if(botaoDislike.hasClass('fas')){
    botaoDislike.toggleClass('fas far');
    quantidadeDislike.text(function(idx, txt) {
      return( (+txt == 0) ? 0 : (+txt - 1));
    });
  }

  if(botaoLike.hasClass('far')){
    quantidadeLike.text(function(idx, txt) {
      return( (+txt == 0) ? 0 : (+txt - 1));
    });
  }
  else{
    quantidadeLike.text(function(idx, txt) {
      return +txt + 1;
    });
  }
};

// Enviando resposta 
function enviarResposta(elem){
  // comentário
  const comentario = $(elem).closest('.row').find('#input-resposta').val();

  if(comentario.length > 255){
    var text = "O tamanho de caracteres excede o tamanho proposto"; 
    $(elem).closest('.row').find('#input-resposta').val('');
    alertaComentario(text);
  }else if(comentario.length == 0){
    var text = "O input comentário está vázio"
    alertaComentario(text);
  }else{
    // usuário (essa variável não é utilizado no AJAX)
    const usuario = $('.usuario').attr('value');

    // id do comentário
    const resposta = $(elem).closest('.card-comentario').attr('value');

    const csrftoken = getCookie('csrftoken');
    $.ajax({
      url: '../../post_resposta/',
      type: "POST",
      headers: {'X-CSRFToken': csrftoken},
      data: {
        'comentario': comentario,
        'resposta'  : resposta,
        'conteudo'  : conteudoId,
      },
      success: function(data) {
        adicionarResposta(elem, comentario, usuario, data.comentarioId, data.perfil, data.perfil_id)
        $(elem).closest('.row').find('#input-resposta').val("")
      },
      error: function(data) {
        if(data.status == 403){
          var data = JSON.parse(data.responseText); 
          alerta("error", "Perfil Silenciado", data.msg)
        }
      }
    });
  }
};

// Adicionar o card resposta dinamicamente
function adicionarResposta(elem, comentario, usuario, comentarioId, foto, perfil_id){
  var comentario = htmlEncode(comentario);
  // após o usuário clicar em responder e adicionar um comentário e clicar no botão enviar, aparece esse html dinâmico
  var respostas = `
                  <div class="card card-comentario ml-2 card-resposta" value="` + comentarioId + `">
                  <div class="row">
                    <img src="`+foto+`" alt="Foto de Perfil"  class="foto-perfil-base">
                    <div class="col-sm-9 col-11">
                        <div class="d-flex flex-row">
                          <a href="../../../perfil/`+perfil_id+`">
                            <h6 class="card-title">` + usuario + `</h6>
                          </a>
                          <div class="ml-3">
                              <button class="btn bg-cinza-escuro btn-sm btn-secondary" onclick="deletarComentario(this, `+ comentarioId + `)">
                              <i class="fa fa-trash text-dark" aria-hidden="true"></i>
                              </button>
                          </div>
                        </div>
                        ` + comentario + ` 
                        <div class="row">
                          <div class="d-inline-flex ml-3">
                              <div class="p-1">
                                <i class="far fa-thumbs-up like" onclick="likeComentario(this)" title="Gostei"></i>
                                <span class="quantidade-like-comentario" value="0">0</span>
                              </div>
                              <div class="p-1">
                                <i class="far fa-thumbs-down dislike" onclick="dislikeComentario(this)" title="Não gostei"></i>
                                <span class="quantidade-dislike-comentario" value="0">0</span>
                              </div>
                          </div>
                        </div>
                    </div>
                  </div>
                `
  
  // adicionar o card de resposta
  $(elem).closest('.resposta').next().append(respostas)
  // habilitar o buttonr responder
  $(elem).closest('.card-comentario').find('.responder').attr('onClick', 'responder(this);this.onclick=null;')
  // remover a barra de comentario
  $(elem).closest('.barra-comentario').remove()

}

// Gira a setinha do accordion
function rotacionar(elem){
  let setinha = $(elem).find('i');
  if(setinha.hasClass('fa-angle-down')){
    setinha.removeClass('fa-angle-down').addClass('fa-angle-up');
  }else{
    setinha.removeClass('fa-angle-up').addClass('fa-angle-down');
  }
}

// Abre uma barra de comentário para responder 
function responder(elem){
  let foto = $('.perfil-logado').attr('src')

  var resposta = `
  <div class="row barra-comentario">
    <div class="ml-3">
      <img src="`+foto+`" alt="Foto de Perfil"  class="foto-perfil-base perfil-logado">
    </div>
    <div class="col-sm-9 col-md-6">
        <input type="text" class="form-control" id="input-resposta" onkeyup="respostaKeyUp(this)" onkeypress="pressEnter(event, this)" placeholder="Adicione uma resposta... ">
    </div>
    <div class="col-sm-1 col-md-1">
        <button type="button" class="btn btn-sm buttonresposta text-light enviar_resposta" onclick="enviarResposta(this)" disabled>Enviar</button>
    </div>
  </div>
` 
  $(elem).closest('.d-inline-flex').next().append(resposta)
}

let quantidadeComentario = $('.quantidade-comentario').attr('value');

// Requisição Ajax global
function ajaxSend(data, url){
  const csrftoken = getCookie('csrftoken');

  $.ajax({
    url: '../../'+ url +'/',
    type: "POST",
    headers: {'X-CSRFToken': csrftoken},
    data: data,
    success: function({data}) {
    },
    error: function(data) {
        alert("Error!");
    }
  });
}
  
// Deletar comentário
function deletarComentario(elem, id){
  Swal.fire({
    title: 'Você tem certeza que quer deletar esse comentário?',
    text: "Você não pode reverter isso!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Deletar'
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire(
        'Deletado!',
        'Seu comentário foi excluído.',
        'success'
      )
      
      if(!$(elem).closest('.card-comentario').hasClass('card-resposta')){
        quantidadeComentario--;
      }
      if(quantidadeComentario < 2){
        $('.comentario').text('Comentário')
      }
      
      data  = {'id': id};
      url   = 'post_delete_comentario';
      ajaxSend(data, url);
      accordionResposta(elem);
    }
  })
}

// Função que atualiza a quantidade de respostas que está atrelado com o comentário
function accordionResposta(elem){
  let comentario          = $(elem).closest('.card-comentario');
  let accordion           = $(elem).closest('.accordion-resposta');
  let textResposta        = "resposta";
  let quantidadeResposta  = accordion.closest('#accordion').find('.quantidade-resposta');

  comentario.remove()

  if (accordion.children().length == 0){
    accordion.closest('#accordion').remove();
  }

  if(accordion.children().length > 1){
    textResposta = "respostas"
  }

  quantidadeResposta.text(accordion.children().length + ' ' + textResposta)
  $('.quantidade-comentario').text(quantidadeComentario);

}

// Função para aumentar a quantidade de comentário
function aumentarComentario(){
  quantidadeComentario++;
  if(quantidadeComentario > 1){
    $('.comentario').text('Comentários')
  }
  $('.quantidade-comentario').text(quantidadeComentario);
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

// Transformação de um script para text
function htmlEncode(str){
  return String(str).replace(/[^\w. ]/gi, function(c){
     return '&#'+c.charCodeAt(0)+';';
  });
}

// Faz o set up das opções existentes na aba do canto superior direito da tela
function configuraBotoesMenu() {
  // Verifica se o usuário é dono do conteúdo
  $.get(`/trilhas/conteudo/is_owner/${conteudoId}`, function(data) {

    if (data.is_owner) {
      const request_url_update = $("#solicita-edicao-url").attr("data-url");

      $('#navbarNavDropdown .dropdown-menu')
        .prepend(`
          <a class="dropdown-item" href="${request_url_update}">
          <i class="fas fa-pen"></i> Solicitar a edição
          </a>`);
      
      $('#navbarNavDropdown .dropdown-menu')
        .prepend(`
          <a class="dropdown-item" onclick="solicita_exclusao()">
          <i class="fas fa-trash"></i> Solicitar a exclusão
          </a>`);
      
      $('#navbarNavDropdown .dropdown-menu')
        .prepend(`
          <a class="dropdown-item" onclick="solicita_certificado()">
          <i class="fas fa-download"></i> Baixar certificado
          </a>`);
    }
  });
}

function sinalizar_comentario(elem){
  const request_url_sinalizacao = $(elem).attr("data-url");

  const csrftoken = getCookie('csrftoken');
  alertConfirm('success',
    'Tem certeza que deseja sinalizar este comentário?',
    () => {
    $.ajax({
      url: request_url_sinalizacao,
      type: "POST",
      headers: {'X-CSRFToken': csrftoken},
      success: function(data) {
        alerta("success", "Sinalização enviada aos Administradores", "Espere a avaliação dos Administradores para a conclusão da sinalização") 
      },
      error: function(data) {
          if(data.status == 403)
            alerta("error", "Sinalização já feita", "Espere a avaliação dos Administradores para a conclusão da sinalização")
      }
    });  
  });

}

function solicita_exclusao() {
  const request_url_delete = $("#solicita-exclusao-url").attr("data-url");

  const csrftoken = getCookie('csrftoken');
  alertConfirm('success',
    'Tem certeza que deseja solicitar a exclusão deste conteúdo?',
    () => {
    $.ajax({
      url: request_url_delete,
      type: "POST",
      headers: {'X-CSRFToken': csrftoken},
      success: function(data) {
        alerta("success", "Requisição enviada aos Administradores", "Espere a avaliação dos Administradores para a conclusão da solicitação") 
      },
      error: function(data) {
          if(data.status == 403)
            alerta("error", "Solicitação de exclusão já feita", "Espere a avaliação dos Administradores para a conclusão da solicitação")
      }
    });  
  });
}

function solicita_certificado() {
  document.location.href = "gerar_certificado";
}

// Modal de alerta de comentário
function alerta(icon="success", title, text){
  return Swal.fire({
    icon: icon,
    title: title,
    text: text,
  })
}

function alertConfirm(icon="success", title, callback, params) {
  return Swal.fire({
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

function sinalizar_conteudo(icon="success", title='Sinalizar conteúdo') {
  const request_url_sinalizacao = $('#sinalizar-conteudo').attr('data-url')

  const csrftoken = getCookie('csrftoken');

  return Swal.fire({
    title: title,
    showDenyButton: true,
    width: '600px',
    html: `
    <hr>
    <div class="form-check text-left">
      <input class="form-check-input" type="radio" name="opcaoSinalizacaoConteudo" id="radioConteudo" value="sinalizacoes_conteudo">
      <label class="form-check-label h5" for="radioConteudo">
        Conteúdo
      </label>
      <br>
      <span class="text-muted">
          Este conteúdo possui uma qualidade muito baixa.
      </span>
    </div>

    <div class="form-check text-left mt-2">
      <input class="form-check-input" type="radio" name="opcaoSinalizacaoConteudo" id="radioTitulo" value="sinalizacoes_titulo">
      <label class="form-check-label h5" for="radioTitulo">
        Título
      </label>
      <br>
      <span class="text-muted">
        Título não tem ligação com conteúdo.
      </span>
    </div>

    <div class="form-check text-left mt-2">
      <input class="form-check-input" type="radio" name="opcaoSinalizacaoConteudo" id="radioDescricao" value="sinalizacoes_descricao">
      <label class="form-check-label h5" for="radioDescricao">
        Descrição
      </label>
      <br>
      <span class="text-muted">
        A descrição não detalha o que o conteúdo quer propor.
      </span>
    </div>
    
    <div class="form-check text-left mt-2">
      <input class="form-check-input" type="radio" name="opcaoSinalizacaoConteudo" id="radioTecnologia" value="sinalizacoes_tecnologia">
      <label class="form-check-label h5" for="radioTecnologia">
        Tecnologia
      </label>
      <br>
      <span class="text-muted">
        Tecnologia está fora do padrão do conteúdo.
      </span>
    </div>

    <div class="form-check text-left mt-2">
      <input class="form-check-input" type="radio" name="opcaoSinalizacaoConteudo" id="radioSecao" value="sinalizacoes_secao">
      <label class="form-check-label h5" for="radioSecao">
        Seção
      </label>
      <br>
      <span class="text-muted">
        Seção está fora do padrão do conteúdo.
      </span>
    </div>  

    `,
    showCancelButton: false,
    confirmButtonText: 'Prosseguir',
    denyButtonText: `Cancelar`,
    preConfirm: () => {
      const opcao = $('input:radio[name="opcaoSinalizacaoConteudo"]').is(':checked')
      let dados = $('input[name="opcaoSinalizacaoConteudo"]:checked').val()
      if (!opcao) {
        Swal.showValidationMessage(`Selecione alguma das opções acima`)
      }
      return { opcao: dados}
    }
  }).then((result) => {
    /* Read more about isConfirmed, isDenied below */
    if (result.isConfirmed) {
      $.ajax({
        url: request_url_sinalizacao,
        type: "POST",
        headers: {'X-CSRFToken': csrftoken},
        dataType:'json',
        data: {'opcao': result.value.opcao},
        success: function(data) {
          
          alerta("success", "Sinalização enviada aos Administradores", "Espere a avaliação dos Administradores para a conclusão da sinalização") 
        },
        error: function(xhr) {
            var err = JSON.parse(xhr.responseText); 
            if(xhr.status == 403)
              alerta("error", "Erro na hora de sinalizar", err.msg)
        }
      });

    }
  })
}

