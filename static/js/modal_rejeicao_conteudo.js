$(document).ready(function() {
    $("#btn-modal-rejeicao").on("click", function() {
        rejeitarRequisicao();
    })
});

function rejeitarRequisicao() {
    const csrftoken = getCookie('csrftoken');
    const descricaoRejeicao = $("#modalRejeicao #descricaoRejeicao").val()

    $.ajax({
        url: `/trilhas/conteudo/validar/${solicitacao_id}/rejeitar/`,
        type: "POST",
        headers: {'X-CSRFToken': csrftoken},
        data: {
          'motivo_rejeicao': descricaoRejeicao
        },
        success: function(data) {
            document.location.href = '/trilhas';
        },
        error: function(data) {
            alert("Error!");
        }
      });
}