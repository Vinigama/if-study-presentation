$(document).ready(function() {
    $('#formConteudo').on('submit', function(e){
      e.preventDefault();
      //Captura dos dados
      const form = new FormData();
    
      let valoresInput = {};
      $('#formConteudo .dadosConteudo').each(function(){
        let elem = $(this);
        valoresInput[elem.prop('name')] = elem.val();
      });
    
      let thumbnail = $('#formConteudo [name=thumbnail]')[0].files[0];
      
      form.append('thumbnail', thumbnail);
    
      appendForm(form, valoresInput);
    
      tags = $('#tags').getTagsValues();
    
      appendList(form, tags, 'tags');
      
      //Envio dos dados
      const csrftoken = getCookie('csrftoken');
      const url = $("#solicita-edicao-url").attr('data-url');
      $.ajax({
        url: url,
        type: "POST",
        headers: {'X-CSRFToken': csrftoken},
        contentType: false,
        processData: false,
        data: form,
        success: function({data}) {
            document.location.href = '/trilhas';
        },
        error: function(data) {
            alert("Error!");
        }
      });
    });
    mostraMensagemCasoJaExistente();
  });
  
  
  
  function getTecnologias(id, callBack, ...restante){
      $.ajax({
          url: '../../get_tecnologias/',
          type: "GET",
          data: {'id': id},
          success: function({data}) {
              callBack(data, restante);
          },
          error: function(data) {
              alert("Error!");
          }
      });
  }
  
  
  function atualizarSecoes(data, ...restante){
      secao = $('#secao_select');
      secao.empty();
      secao.append(`<option value="" selected disabled>Selecione uma seção</option>`);
      data.forEach((item) => secao.append(`<option value="${item.nome}">${item.nome}</option>`));
  }
  
  
  function appendForm(formData, objeto){
    Object.entries(objeto).forEach(item => formData.append(item[0], item[1]));
  }
  
  function appendList(formData, list, keyName){
    for (var i = 0; i < list.length; i++) {
      formData.append(`${keyName}[]`, list[i].trim());
    }
  }
  
  function habilitarInput(botao) {
      $(botao).parent('.div-pai').find('.dadosConteudo,.hab-botao').prop('disabled', false);
  }
  
  
  //Código Externo
  
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
  
  
  (function() {
    'use strict';
    window.addEventListener('load', function() {
      var forms = document.getElementsByClassName('needs-validation');
      var validation = Array.prototype.filter.call(forms, function(form) {
        form.addEventListener('submit', function(event) {
          if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
          }
          form.classList.add('was-validated');
        }, false);
      });
    }, false);
  })();

// Modal de alerta sobre conteúdo já criado
function alertaConteudoExistente(texto, titulo) {
  return Swal.fire({
    icon: 'warning',
    title: titulo,
    text: texto,
  })
}

// Caso conteúdo já esteja vinculado a outra requisição, mostra aviso
function mostraMensagemCasoJaExistente() {
  const titulo = "Atenção! Já existe uma solicitação vinculada a este conteúdo";
  const texto = "Verifique se a ação que está prestes a tomar já não foi tomada";
  const exists = $("#diversos-attr").attr('data-existe');
  if(exists == 'True')
    alertaConteudoExistente(texto, titulo);
}

function mostrarInput() {
  Swal.fire({
    title: "Novo Recurso",
    text: "Digite o nome do recurso:",
    input: 'text',
    showCancelButton: true        
  }).then((result) => {
      if (result.value) {
          console.log("Result: " + result.value);
      }
  });
}