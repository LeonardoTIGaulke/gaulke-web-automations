// controller_check_inputs.js

function validInputs(number_check_files) {
    let file = document.getElementById("file").value;
    let file_2 = document.getElementById("file_2").value;
    
    let block_info_error = document.querySelector(".block-info-erros-input-file");

    if (number_check_files == 1){
        if (file == "") {
            block_info_error.style.display = "flex";
            return false;
        }
        else {
            return true;
        }
    }
    else if (number_check_files == 2){

        if (file == "" || file_2 == "") {
            block_info_error.style.display = "flex";
            return false
            
        } else {
            return true;
        }
    }
}

function checkSelectFile(number_check_files){
    let btn_send_file = document.getElementById("btn-send-file");
    let form_file = document.getElementById("form-select-file-01");

    let check = validInputs(number_check_files);
    
    form_file.addEventListener("submit", function(event){
        event.preventDefault();
        
        if (check){
            animationLoadPostFile();
            form_file.submit();
        } else {
            animationLoadPostFile();
        }
    });
 
}


// -------------------- ATUALIZA CONTAS FORNECEDORES | UTILIZADO PARA CONFIGIRAR CONTAS DÉBITO NA IMPORTAÇÃO DO SICOOB --------------------
function atualiza_ContasFornecedores(e) {
    const id = "D-comum-CNPJ-" + e.id.replace(" ", ".");
    const valor = e.value;

    console.log(id)
    console.log(valor)

    const fields_to_update = document.querySelectorAll(`.${id}`);
    if (fields_to_update) {
        fields_to_update.forEach((field)=>{
            field.textContent = valor;
            console.log("NUM. CONTA: ", field.textContent);
            console.log(valor)
        });
    }
}