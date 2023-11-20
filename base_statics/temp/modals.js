var btn_config = document.querySelector(".btn-config-payroll-relation");
var btn_export_data = document.querySelector(".btn-export-data");

var status_btn_export_data = false;
var data_to_csv = null;


function displayModalConfigContas(){

    if (list_select.length >= 1){
        const pageElements = document.querySelector(".container-base-elements");
        const modalConfigContas = document.getElementById("container-modal-preview");
        
        pageElements.classList.toggle("enableBlur_PreviewRelation");
        // ----
        modalConfigContas.classList.toggle("display-modal-config-contas");
        modalConfigContas.classList.toggle("disableBlur_PreviewRelation");
        // ----
        document.getElementById("container-preview-relation").classList.toggle("enableBlur_PreviewRelation");
    }

}


function close_modal_error(){
    document.getElementById("modal-error-import-data-folha").style.display = "none";
}

function close_modal_config_payroll_relation() {
    document.getElementById("container-preview-payroll").style.display = "none";
    document.getElementById("container-payroll-relation").classList.toggle("enableBlur");
    document.getElementById("container-payroll-relation").classList.toggle("disableBlur");
    
    // ----
    document.getElementById("form-file-payroll-relation").classList.remove("enableBlur");
    // ----
    // document.getElementById("block-content-preview").classList.toggle("enableBlur");
    // document.getElementById("block-content-preview").classList.toggle("disableBlur");
}

function open_modal_config_payroll_relation() {
    document.getElementById("container-preview-payroll").style.display = "block";
    document.getElementById("container-payroll-relation").classList.toggle("enableBlur");
    document.getElementById("container-payroll-relation").classList.toggle("disableBlur");

    // ---------- FORM FILE ----------
    document.getElementById("form-file-payroll-relation").classList.toggle("enableBlur");
    document.getElementById("form-file-payroll-relation").classList.toggle("disableBlur");
    // // ----
    // document.getElementById("block-content-preview").classList.toggle("enableBlur");
    // document.getElementById("block-content-preview").classList.toggle("disableBlur");


}

function stringToFloat(str) {
    return parseFloat(str.replace(',', '.').replace('.', '').replace(',', '.'));
}
//  ------------------- POST PREVIEW PAYROLL RELATION -------------------
function previewPayrollRelation(url, csrf_token){

    const cod_empresa = document.getElementById("cod_empresa").value;
    const filial = document.getElementById("filial").value;
    const data_lacamento = document.getElementById("data_lacamento").value;
    const numero_conta_contabil_debito = document.getElementById("numero_conta_contabil_debito").value;
    const numero_conta_contabil_credito = document.getElementById("numero_conta_contabil_credito").value;
    
    let table = document.getElementById("form-payroll-relaction");
    let thead = table.querySelector("thead");
    let tbody = table.querySelector("tbody");

    let header = thead.querySelector("tr").querySelectorAll("th");
    let rows = tbody.querySelectorAll("tr");

    let obj_headers = new Array();
    let obj_rows = new Array();

    
    for (let i =0; i< header.length; i++){
        if (i > 1){
            obj_headers.push(header[i].textContent)
        }
    }
    
    rows.forEach((e)=>{
        var list_temp = new Array();
        var check_id = false;

        var elementos_td = e.querySelectorAll("td");
        // console.log(elementos_td);


        for (let i =0; i < elementos_td.length; i++){
            let check_input = elementos_td[1].querySelector("input");
            if (check_input.checked == true){
                check_id= true;
            }
            if (i > 1){
                
                list_temp.push(elementos_td[i].textContent);
            }
        }
        
        if (check_id){
            obj_rows.push(list_temp);
        }
    });

    let data = {
        'cod_empresa': cod_empresa,
        'filial': filial,
        'data_lacamento': data_lacamento,
        'numero_conta_contabil_debito': numero_conta_contabil_debito,
        'numero_conta_contabil_credito': numero_conta_contabil_credito,
        'headers': obj_headers,
        'rows': obj_rows,
    };
    console.log(data);

    let headers = { "X-CSRFToken": csrf_token };

    fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(data),
        }
    ).then((data)=>{
        return data.json();
        }
    ).then((data)=>{

        console.log("\n\n -------FIM POST ---- ")
        console.log(data);

        status_btn_export_data = false;
        if(data.code == 200){
            console.log("ok....");

            data_to_csv = JSON.parse(data["data"]);
            status_btn_export_data = true;
            console.log(" ---------------- JSON FINALIZADO ---------------- ")
            console.log(data_to_csv);
            status_btn_exportData();

            // document.querySelector(".btn-export-data").classList.toggle("status-disabled");
                        
            close_modal_config_payroll_relation();
        } else {
            console.log("error....")
            status_btn_export_data = false;
            status_btn_exportData();
        }
    })

}