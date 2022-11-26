$(window).ready(function() {

  $("label[for=id_body]").remove();
  $("#tecnologia").trigger("change");

});

function getTecnologias(id, callBack, ...restante){
  $.ajax({
      url: '/trilhas/get_tecnologias/',
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
  secao = $('#secao');
  secao.empty();
  secao.append(`<option value="" selected>Não selecionada</option>`);
  data.forEach((item) => secao.append(`<option value="${item.nome}">${item.nome}</option>`));
}