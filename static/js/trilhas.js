$( document ).ready(function() {
    setTimeout(function() {
        $('.message').fadeOut('slow');
    }, 1500); 
});

function getTecnologias(id, callBack, ...restante){
    $.ajax({
        url: 'get_tecnologias/',
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
