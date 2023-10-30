//  SOMA TOTAIS SELECIONADO EM PAYROLL RELATION -------------------
var TT_SUM_Payroll_selected = 0;
var TT_Payroll_selected = 0;
var valueReume = null;
var list_select = new Array();

var soma_debito = 0.00;
var soma_credito = 0.00;
var dif_debito_credito = 0.00;

var elem_soma_debito = document.getElementById("soma_debito");
var elem_soma_credito = document.getElementById("soma_credito");
var elem_diff_soma = document.getElementById("diff_soma");
var elem_total_selecao = document.getElementById("total_selecao");

function calculateValues(e){

    let valor_liq = parseFloat(document.querySelector(`.${e.id}-valor`).textContent);
    let tipo_lanc = document.querySelector(`.tipo-lanc-${e.id}`).textContent;

    console.log(valor_liq);
    console.log(tipo_lanc);

    if (e.checked) {
        TT_Payroll_selected += 1;
        list_select.push(e.id);
        if (tipo_lanc == "C"){
            soma_credito += valor_liq;
        } else if (tipo_lanc == "D") {
            soma_debito += valor_liq;
        }
        
    } else {
        TT_Payroll_selected -= 1;
        let index = list_select.indexOf(e.id);
        if (index > -1){
            list_select.splice(index, 1);
        }
        if (tipo_lanc == "C"){

            soma_credito -= valor_liq;

        } else if (tipo_lanc == "D") {

            soma_debito -= valor_liq;

        }
    }


    dif_debito_credito = Math.abs(soma_debito - soma_credito);
    elem_soma_debito.textContent = soma_debito.toLocaleString('pt-br',{style: 'currency', currency: 'BRL'});
    elem_soma_credito.textContent = soma_credito.toLocaleString('pt-br',{style: 'currency', currency: 'BRL'});
    elem_diff_soma.textContent = dif_debito_credito.toLocaleString('pt-br',{style: 'currency', currency: 'BRL'});
    elem_total_selecao.textContent = TT_Payroll_selected;
    status_btn_config();

}

function status_btn_config(){
    console.log(" LISTA SELECT ---> ", list_select.length);
    
    if (list_select.length >= 1){

        btn_config.disabled = false;
        if( btn_config.classList.contains("status-disabled")){
            btn_config.classList.toggle("status-disabled");            
        }
    } else {
        btn_config.classList.toggle("status-disabled");
        btn_config.disabled = true;
        btn_export_data.disabled = true;
        status_btn_export_data = false;
        status_btn_exportData();
    }
}

function status_btn_exportData(){
    if (status_btn_export_data  ) {
        btn_export_data.disabled = false;
        btn_export_data.classList.remove("status-disabled");
    } else {
        btn_export_data.disabled = true;
        btn_export_data.classList.add("status-disabled");
    }
}

function exportDataPayrollRelation(){

    var csv = '';
    for(var i=0; i<data_to_csv.length; i++){
        var values = Object.values(data_to_csv[i]);
        csv += values.join(';') + '\n';
    }

    var blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    var url = URL.createObjectURL(blob);
    var link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", "Folha de Pagamento.txt");
    link.style.visibility = "hidden";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
function exportDataGNRERelation(){

    var csv = '';
    for(var i=0; i<data_to_csv.length; i++){
        var values = Object.values(data_to_csv[i]);
        csv += values.join(';') + '\n';
    }

    var blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    var url = URL.createObjectURL(blob);
    var link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", "Folha de GNRE.txt");
    link.style.visibility = "hidden";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
function exportDataPaymentAccountsRelation(){

    var csv = '';
    for(var i=0; i<data_to_csv.length; i++){
        var values = Object.values(data_to_csv[i]);
        csv += values.join(';') + '\n';
    }

    var blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    var url = URL.createObjectURL(blob);
    var link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", "Pagamento Conta.txt");
    link.style.visibility = "hidden";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function SelectAllData(check_button){
    var TT_SUM_Payroll_selected = 0;
    TT_Payroll_selected = 0;
    soma_credito = 0;
    soma_debito = 0;
  
    let table = document.getElementById("form-payroll-relaction");
    let thead = table.querySelector("thead");
    let tbody = table.querySelector("tbody");

    let header = thead.querySelector("tr").querySelectorAll("th");
    let rows = tbody.querySelectorAll("tr");

    let obj_headers = new Array();
    let obj_rows = new Array();

    header.forEach((e)=>{
        obj_headers.push(e.textContent);
    });

    rows.forEach((e)=>{
        var list_temp = new Array();
        
       
        let input_id = null;
        let checkbox_current = null;

        e.querySelectorAll("td").forEach((elem)=>{
            try {

                input_id = elem.querySelector("input").id;
                checkbox_current = document.getElementById(input_id);
                valor_liq = document.querySelector(`.${input_id}-valor`).textContent;
                valor_liq = parseFloat(valor_liq);

                let tipo_lanc = document.querySelector(`.tipo-lanc-${input_id}`).textContent;
                console.log(`
                    --->> tipo_lanc: ${tipo_lanc}
                    --->> valor_liq: ${valor_liq}
                `);

                if (check_button.checked == true){
                    if (valor_liq == "0,00" || valor_liq == "0.00") {
                        console.log(" valor incorreto. ")
                    }
                    checkbox_current.checked = true;
                    list_select.push(input_id);

                    TT_SUM_Payroll_selected += valor_liq;
                    TT_Payroll_selected += 1;
                    console.log(TT_Payroll_selected);

                    if (tipo_lanc == "C"){
                        soma_credito += valor_liq;
                    } else if (tipo_lanc == "D") {
                        soma_debito += valor_liq;
                    }

                } else {

                    if (tipo_lanc == "C"){
                        soma_credito -= valor_liq;
                    } else if (tipo_lanc == "D") {
                        soma_debito -= valor_liq;
                    }
                    
                    checkbox_current.checked = false;
                    TT_SUM_Payroll_selected -= valor_liq;
                    TT_Payroll_selected -= 1;
                    soma_credito = 0;
                    soma_debito = 0;
                    list_select = new Array();

                    let index = list_select.indexOf(input_id);
                    if (index > -1){
                        list_select.splice(index, 1);
                    }
                }
  
            } catch (error) {}
        });
        
    });

    if (check_button.checked == false){
        TT_Payroll_selected = 0;
        TT_SUM_Payroll_selected = 0.00;
    }
    dif_debito_credito = Math.abs(soma_debito - soma_credito);
    elem_soma_debito.textContent = soma_debito.toLocaleString('pt-br',{style: 'currency', currency: 'BRL'});
    elem_soma_credito.textContent = soma_credito.toLocaleString('pt-br',{style: 'currency', currency: 'BRL'});
    elem_diff_soma.textContent = dif_debito_credito.toLocaleString('pt-br',{style: 'currency', currency: 'BRL'});
    elem_total_selecao.textContent = TT_Payroll_selected;
    console.log(`
        >> soma_debito: ${soma_debito}
        >> soma_credito: ${soma_credito}
        >> dif_debito_credito: ${dif_debito_credito}
        >> TT_Payroll_selected: ${TT_Payroll_selected}
        >>>> TT_SUM_Payroll_selected: ${TT_SUM_Payroll_selected}
    
    `);
    status_btn_config();
}

close_modal_config_payroll_relation();
status_btn_config();