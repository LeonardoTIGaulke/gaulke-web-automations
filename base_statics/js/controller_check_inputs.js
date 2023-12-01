// controller_check_inputs.js

function validarAraoDosSantos() {
    var file = document.getElementById("file").value;
    var file_2 = document.getElementById("file_2").value;
    
    if (file == "" || file_2 == "") {
        alert("Por favor, preencha todos os campos.");
        return false;
    }
    else {
        return true;
    }
}

function checkSelectFile(){

    console.log(" --------- acionado preventDefault");
    let btn_send_file = document.getElementById("btn-send-file");
    let form_file = document.getElementById("form-select-file-01");

    form_file.addEventListener("submit", function(event) {
        if (!validarAraoDosSantos()) {
            event.preventDefault();
            return
        }
        else {
            event.submitter();
        }
    });
}