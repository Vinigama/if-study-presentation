$( document ).ready(function() {
    setTimeout(function() {
            $('.message').fadeOut('slow');
        }, 1500); 

    $('.enviar').on('click', function(e) {
        e.preventDefault();
        let check = $('input[name=opcao]:checked')
        if (check.val()){
        const csrftoken = getCookie('csrftoken');
        if(check.val() == 'remover'){
            alertConfirm('success','Excluir esse comentário permanentemente?')
        }else{
            alertConfirm('success','Você deseja alterar o status desse comentário para ok?', 'Alterar', '#006600')
        }
    }  
    });
});

function alertConfirm(icon="success", title, confirmButtonText='Deletar', confirmButtonColor="#cc3f44", url) {
  return Swal.fire({
    title: title,
    showDenyButton: true,
    showCancelButton: false,
    confirmButtonText: confirmButtonText,
    denyButtonText: `Cancelar`,
    confirmButtonColor: confirmButtonColor,
    denyButtonColor: "#808080"
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