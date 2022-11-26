function buscarConteudo() {
  const codigo = $("#conteudo-search-bar").val();

  window.location.href = `/trilhas/conteudo/validar_baixa/${codigo}/`;
}