function postUpdateCobrancasPagas(url, csrf_token){

    const cod_empresa = document.getElementById("cod_empresa").value;
    const filial = document.getElementById("filial").value;
    const numero_conta_contabil_debito = document.getElementById("numero_conta_contabil_debito").value;
    const numero_conta_contabil_credito = document.getElementById("numero_conta_contabil_credito").value;
    // ----
    const numero_conta_contabil_juros = document.getElementById("numero_conta_juros").value;
    const numero_conta_contabil_desconto = document.getElementById("numero_conta_desconto").value;
    
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
        'numero_conta_contabil_debito': numero_conta_contabil_debito,
        'numero_conta_contabil_credito': numero_conta_contabil_credito,
        'numero_conta_contabil_juros': numero_conta_contabil_juros,
        'numero_conta_contabil_desconto': numero_conta_contabil_desconto,
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