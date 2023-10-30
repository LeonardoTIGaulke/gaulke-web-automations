function postUpdateContasGNRE(url, csrf_token) {
    const table_contas_GNRE = document.querySelector(".table-contas-gnre");
    const rows = table_contas_GNRE.querySelector("tbody").querySelectorAll("tr");
    const data_post = new Array();

    let td_temp = null;
    let row_uf = null;
    let row_conta_credito = null;
    let row_conta_debito = null;
    
    rows.forEach((data)=>{
        td_temp = data.querySelectorAll("td");
    
        row_uf = td_temp[0].textContent;
        row_conta_credito = td_temp[1].querySelector("input").value;
        row_conta_debito = td_temp[2].querySelector("input").value;
        data_post.push(
            {
                "uf": row_uf,
                "conta_credito": row_conta_credito,
                "conta_debito": row_conta_debito,
            }
        );
    })
    let headers = { "X-CSRFToken": csrf_token };
    fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(data_post),
    }).then((data)=>{
        return data.json();
    }).then((data)=>{
        let element = document.querySelector(".message-response-post");
        if (data["code"] == 200){
            element.querySelector("p").textContent = "registro atualizado!";
            element.classList.toggle("active");
            setTimeout(()=>{
                element.classList.toggle("active");
            }, 2500);
            
        } else {
            element.querySelector("p").textContent = "falha ao atualizar!";
            element.classList.toggle("active");
            setTimeout(()=>{
                element.classList.toggle("active");
            }, 2500);
        }
    });

}

//  ------------------- POST PREVIEW PAYROLL RELATION -------------------
function previewRelation(url, csrf_token){

    const cod_empresa = document.getElementById("cod_empresa").value;
    const filial = document.getElementById("filial").value;
    const numero_conta_debito = document.getElementById("numero_conta_debito").value;
    const numero_conta_credito = document.getElementById("numero_conta_credito").value;
    
        
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
        
        for (let i =0; i < elementos_td.length; i++){
            let check_input = elementos_td[1].querySelector("input");
            if (check_input.checked == true){
                check_id= true;
            }
            if (i > 1){
                list_temp.push(elementos_td[i].textContent.toString().trim());
            }
        }
        
        if (check_id){
            obj_rows.push(list_temp);
        }
    });

    let data = {
        'cod_empresa': cod_empresa,
        'filial': filial,
        'numero_conta_debito': numero_conta_debito,
        'numero_conta_credito': numero_conta_credito,
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