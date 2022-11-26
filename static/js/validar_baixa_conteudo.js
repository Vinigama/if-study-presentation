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
});
  
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

function efetuarBaixa() {
  alertConfirm(icon="warning", "Tem certeza que deseja efetuar a baixa do conteúdo?", solicitarBaixa);
}

function solicitarBaixa() {
  const csrftoken = getCookie('csrftoken');
    $.ajax({
      url: 'executar_baixa/',
      type: "POST",
      headers: {'X-CSRFToken': csrftoken},
      contentType: false,
      processData: false,
      success: function({data}) {
          document.location.href = './';
      },
      error: function(data) {
          alert("Error!");
      }
  });
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