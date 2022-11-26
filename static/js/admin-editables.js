$("window").ready(function() {
    criaBotoesEdicao()
});

function criaBotoesEdicao() {
    const elements = $("[data-editable-component='true']");
    elements.each(function(cont) {
        const component = $(this);
        const defaultButtonHTML = `
        <button onclick="(event)=event.preventDefault()" type="button" class="btn btn-dark p-2 text-center button-editable edit-button-upper-right"><i class="fas fa-edit m-0 p-0"></i></button>`;
        if(component.attr("data-editable-custom-button")) {
            // Para este caso, um botão com classe 'button-editable' deve ser colocado dentro do elemento HTML
            // Implementar
        } else {
            // Este é o comportamento padrão
            // Criar div wrapper como pai do elemento e colocar botão neste wrapper
            let wrapper = document.createElement("div");
            wrapper.classList.add('editable-wrapper');
            component.parent().append(wrapper);
            wrapper.appendChild(this);

            // botão
            const defaultButton = document.createElement("button");
            $(defaultButton).addClass(['btn btn-dark p-2 text-center button-editable edit-button-upper-right'])
            defaultButton.innerHTML = `<i class="fas fa-edit m-0 p-0"></i>`;
            $(wrapper).append(defaultButton);
            $(defaultButton).click(openAdmin);
            configuraBotoes(component, defaultButton);
        }
    });
};

function configuraBotoes(parentComponent, button) {
    /** 
     * Aplica regra de formatação em botões com base em dados passados por atributos 
     * Caso, não seja passado nada. Valor padrão é aplicado: top: 5; right: 5;
     * 
     * data-edit-button-right   - equivalente à propriedade right no CSS
     * data-edit-button-left    - equivalente à propriedade left no CSS
     * data-edit-button-top     - equivalente à propriedade top no CSS
     * data-edit-button-bottom  - equivalente à propriedade bottom no CSS
     * 
     * **/
    if(!parentComponent.attr("data-edit-button-right") 
            && !parentComponent.attr("data-edit-button-left")
            && !parentComponent.attr("data-edit-button-top")
            && !parentComponent.attr("data-edit-button-bottom")) {

        $(button).css("right", "5");
        $(button).css("top", "5");
    } else {
        if(parentComponent.attr("data-edit-button-right"))
            $(button).css("right", String(Number(parentComponent.attr("data-edit-button-right"))));
        if(parentComponent.attr("data-edit-button-left"))
            $(button).css("left", String(Number(parentComponent.attr("data-edit-button-left"))));
        if(parentComponent.attr("data-edit-button-top"))
            $(button).css("top", String(Number(parentComponent.attr("data-edit-button-top"))));
        if(parentComponent.attr("data-edit-button-bottom"))
            $(button).css("bottom", String(Number(parentComponent.attr("data-edit-button-bottom"))));
    }
}

function openAdmin(event) {
    /**
     * Possui dois comportamentos distintos, um para botão personalizado, outro comportamento padrão
     * Personalizado - Botão se encontra dentro do elemento, sobe até encontrar os dados necessários no elemento pai
     * Padrão - Sobe até o wrapper e desce procurando os dados necessários nos elementos filhos deste wrapper
     * */
    event.preventDefault();
    const component = $(event.currentTarget);
    teste = component
    if(component.attr("data-editable-custom-button")) {
        // Comportamento de botão personalizado
        // Implementar
    } else {
        // Comportamento padrão
        const requestedComponent = component.parent(".editable-wrapper").find("[data-editable-component='true']");
        const model = requestedComponent.attr("data-editable-model");
        const app = requestedComponent.attr("data-editable-app");
        const id = requestedComponent.attr("data-editable-id");
        window.open(`/admin/${app}/${model}/${id}/change`, '_blank');
        console.log(`http://127.0.0.1:8000/admin/${app}/${model}/${id}/change`);
    }
}
