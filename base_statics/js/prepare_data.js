function removeCaracter(date_string){
    return date_string.replace("/", "").replace("/", "");
}
// ------------------
function formatDateToString(date_to_str) {
    console.log(` ------------>> DATE: ${date_to_str}`);
    let date = new Date(date_to_str);
    date.setUTCDate(date.getUTCDate() + 1);
    let dataFormatada = date.toLocaleDateString('pt-BR');
    
    console.log(dataFormatada);
    return dataFormatada.replace("/", "").replace("/", "");
}

function SelectAllDataTemp(){
    let btn_select_all = document.querySelector(".btn-select-all-rows");
    let table = document.querySelector(".container-table-preview").querySelector("table");
    let table_body = table.querySelector("tbody").querySelectorAll("tr");
    let table_td = null;
    table_body.forEach((row)=>{
        if (btn_select_all.checked){
            table_td = row.querySelectorAll("td")[0].querySelector("input").checked = true;
        } else {
            table_td = row.querySelectorAll("td")[0].querySelector("input").checked = false;
        }
        console.log(table_td);
    });
}
function SelectAllDataTemp_extra_02(){
    let btn_select_all = document.querySelector(".btn-select-all-rows-extra-02");
    let table = document.querySelector(".container-table-preview-extra-02").querySelector("table");
    let table_body = table.querySelector("tbody").querySelectorAll("tr");
    let table_td = null;
    table_body.forEach((row)=>{
        if (btn_select_all.checked){
            table_td = row.querySelectorAll("td")[0].querySelector("input").checked = true;
        } else {
            table_td = row.querySelectorAll("td")[0].querySelector("input").checked = false;
        }
        console.log(table_td);
    });
}
// ----
function disabledRowsTable(){
    let btn_select_all = document.querySelector(".btn-select-all-rows");
    let table = document.querySelector(".container-table-preview").querySelector("table");
    let table_body = table.querySelector("tbody").querySelectorAll("tr");
    let table_td = null;
    table_body.forEach((row)=>{
        table_td = row.querySelectorAll("td")[0].querySelector("input");
        try {
            if (table_td.checked == true){
                row.style.display = "none";
                row.disabled = true;
            }
        } catch (error) {};
        
    });
}

function checktotalRowsExported(host_port, subdir, path){
    let table = document.querySelector(".container-table-preview").querySelector("table");
    let table_body = table.querySelector("tbody").querySelectorAll("tr");
    let tt_rows_table = table_body.length;
    let tt_rows_exported = 0;
    table_body.forEach((row)=>{
        table_td = row.querySelectorAll("td")[0].querySelector("input");
        try {
            if (table_td.checked == true){
                tt_rows_exported += 1;
                console.log(`
                    ---> tt_rows_table: ${tt_rows_table}
                    ---> tt_rows_exported: ${tt_rows_exported}
                `);
                if (tt_rows_table == tt_rows_exported){
                    // window.location.href = "http://localhost:8000/automations/relacao-GNRE/";
                    window.location.href = `${host_port}/${subdir}/${path}/`;
                }
            }
        } catch (error) {};
    });
}