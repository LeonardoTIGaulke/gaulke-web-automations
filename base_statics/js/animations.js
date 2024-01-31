function displayModalAccounts(){
    let container_elements = document.querySelector(".container-base-elements");
    let modalAccounts = document.querySelector(".block-config-data-to-text");
    let container_footer = document.querySelector(".container-footer");
    let container_companies_to_auth = document.querySelector(".container-all-companies-to-auth");
   
    container_elements.classList.toggle("filter-blur-10");
    container_footer.classList.toggle("filter-blur-10");
    container_companies_to_auth.classList.toggle("filter-blur-10");

    modalAccounts.classList.toggle("displayModalVisible");
    modalAccounts.classList.toggle("disble-filter-blur");
}

function displayModal_ContasFornecedores(){
    let container_elements = document.querySelector(".container-base-elements");
    let modalAccounts = document.querySelector(".block-config-data-to-CPF-CNPJ");
    let container_footer = document.querySelector(".container-footer");
    container_companies_to_auth.classList.toggle("filter-blur-10");
    
    container_elements.classList.toggle("filter-blur-10");
    container_footer.classList.toggle("filter-blur-10");

    modalAccounts.classList.toggle("displayModalVisible");
    modalAccounts.classList.toggle("disble-filter-blur");
}

// ------------------

function animationLoadPostFile(){
    document.querySelector(".container-processing-data").classList.toggle("displayflexAnimationProcessingData");
}


// ------------------ CONFIGURAÇÕES AVANÇADAS DE CONTAS ------------------
function displayModal_ConfiguracoesAvancadas(){
    let container_elements = document.querySelector(".container-base-elements");
    let modalAccounts = document.querySelector(".modal-configuracoes-avancadas");
    let container_footer = document.querySelector(".container-footer");
   
    container_elements.classList.toggle("filter-blur-10");
    container_footer.classList.toggle("filter-blur-10");

    modalAccounts.classList.toggle("displayModalVisible");
    modalAccounts.classList.toggle("disble-filter-blur");
}
