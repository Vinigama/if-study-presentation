$(document).ready(function() {  
    $("#search-bar").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#conteudos h4").filter(function() {
          $(this).closest('.card-body').toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
      });
});
