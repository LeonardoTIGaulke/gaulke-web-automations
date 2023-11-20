
function clearElementTable(table, element){
    try {
        table.querySelector(element).remove();
    } catch (error) {};
}
// ----
function addElementTable(table, element){
    if (element == null){
        table.innerHTML += "-";
    } else {
        table.innerHTML += element;
    }
}
// ----
function updateProgressTable(progress){
    document.querySelector(".progress_table_update").innerHTML = `Progresso: ${progress}`;
}

// ----
function populateTablePreviewGeneric(json_headers, json_body){

    const container_table_preview = document.querySelector(".table-preview");
    
    clearElementTable(table=container_table_preview, element="thead");
    clearElementTable(table=container_table_preview, element="tbody");
    
    addElementTable(table=container_table_preview, element=`
    <thead>
        <tr>
            <th class="col-fixed-table" style="z-index:1099" >#</th>
        </tr>
    </thead>`);

    addElementTable(table=container_table_preview, element="<tbody></tbody>");

    const thead = container_table_preview.querySelector("thead");
    const tbody = container_table_preview.querySelector("tbody");

    json_headers.forEach((col)=>{
        thead.querySelector("tr").innerHTML += `<th>${col}</th>`;
    })

    
    let index_aux = 1;
    
    var tt_registros = json_body.length;
    if (tt_registros >= 1){
        const populateTable = new Promise((resolve, reject)=>{
            
            json_body.forEach((e)=>{
                
                let row = `table-row-${index_aux}`;
                
                tbody.innerHTML += `<tr class="${row}"></tr>`;
                let tr = document.querySelector(`.${row}`);
                addElementTable(table=tr, element=`<td class="col-fixed-table">${index_aux}</td>`);
                // ----
                addElementTable(table=tr, element=`<td> ${e.TIPO_LANC} </td>`);
                addElementTable(table=tr, element=`<td> ${e.COD_EMPRESA} </td>`);
                addElementTable(table=tr, element=`<td> ${e.FILIAL} </td>`);
                addElementTable(table=tr, element=`<td> ${e.DATA_ENTRADA} </td>`);
                addElementTable(table=tr, element=`<td> ${e.COD_ERP_CLIENTE} </td>`);
                addElementTable(table=tr, element=`<td> ${e.TIPO_REGISTRO} </td>`);
                addElementTable(table=tr, element=`<td> ${e.CONTA} </td>`);
                addElementTable(table=tr, element=`<td> ${e.SUB_CONTA} </td>`);
                addElementTable(table=tr, element=`<td> ${e.VALOR} </td>`);
                addElementTable(table=tr, element=`<td> ${e.ACAO_LANC} </td>`);
                addElementTable(table=tr, element=`<td> ${e.PRIM_HIST_CONTA} </td>`);
                addElementTable(table=tr, element=`<td> ${e.COD_HIST} </td>`);
                addElementTable(table=tr, element=`<td class="col-long-custom"> ${e.COMPLEM_HIST} </td>`);
                addElementTable(table=tr, element=`<td> ${e.GRUPO_LANC} </td>`);
                addElementTable(table=tr, element=`<td> ${e.CNPJ} </td>`);
                addElementTable(table=tr, element=`<td> ${e.INSC_ESTADUAL} </td>`);
                addElementTable(table=tr, element=`<td> ${e.TP_CNPJ} </td>`);
                addElementTable(table=tr, element=`<td> ${e.CONTA_ORIGEM} </td>`);
                addElementTable(table=tr, element=`<td> ${e.CNPJ_EMPRESA} </td>`);
                addElementTable(table=tr, element=`<td> ${e.IE_EMPRESA} </td>`);
                index_aux += 1;
    
                // var progress = index_aux / tt_registros;
                // updateProgressTable(progress);
    
            });
            resolve({"process": "finish"});
        }).then((data)=>{
            console.log(data);
        });
    }
    document.querySelector(".container-processing-data").style.display =  "none";
    document.getElementById("container-preview-relation").style.display = "flex";
}
// ----
function redo_parameters(){
    const container_base_elements = document.querySelector(".container-base-elements");
    container_base_elements.classList.toggle("display-container-elements");
    console.log("Test...");
};
