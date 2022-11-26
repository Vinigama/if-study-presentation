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
      let arquivo = $('#formConteudo [name=arquivo]')[0].files[0];
      
      form.append('thumbnail', thumbnail);
      form.append('arquivo', arquivo);
    
      appendForm(form, valoresInput);
    
      tags = $('#tags').getTagsValues();
    
      appendList(form, tags, 'tags');
      
      //Envio dos dados
      const csrftoken = getCookie('csrftoken');
      $.ajax({
        url: 'aprovar/',
        type: "POST",
        headers: {'X-CSRFToken': csrftoken},
        contentType: false,
        processData: false,
        data: form,
        success: function({data}) {
            document.location.href = '../../../';
        },
        error: function(data) {
            alert("Error!");
        }
      });
    });
    configurarCarga();
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
  
function secondsToHourSecMin(seconds) {
  // Recebe valor inteiro e retorna uma lista [horas, minutos, segundos]
  const horas = Math.floor(seconds/3600);
  const sobraHoras = seconds % 3600;
  const minutos = Math.floor(sobraHoras/60);
  const segundos = sobraHoras % 60;
  return [horas, minutos, segundos];
}

function configurarCarga() {
  let [horas, minutos, segundos] = secondsToHourSecMin(parseInt(carga_conteudo));
  $("input[name=carga_horas]").val(horas);
  $("input[name=carga_minutos]").val(minutos);
  $("input[name=carga_segundos]").val(segundos);
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