function getAllRows_TablePreview(){
    var table, rows;
    table = document.querySelector(".container-table-preview").querySelector("table");
    rows = table.querySelector("tbody").querySelectorAll("tr");
    return rows;
}

function selectAllCheckboxes(element){
    var rows, td, btn_actions;
    btn_actions = document.querySelectorAll(`[data-btn-action="open-model-config"]`);
    rows = getAllRows_TablePreview();
    
    if (element.checked){
        btn_actions.forEach((btn)=>{
            btn.disabled = false;
            btn.classList.add("active");
        });
    } else {
        btn_actions.forEach((btn)=>{
            btn.disabled = true;
            if (btn.classList.contains("active")){
                btn.classList.remove("active");
            }
        });
    }

    rows.forEach((row)=>{

        td = row.querySelectorAll("td")[0].querySelector("input");
        if (element.checked) {
            td.checked = true;
        } else {
            td.checked = false;
        }

    });

}

function selectCheckbox(element){
    var rows, td, btn_actions;
    btn_actions = document.querySelectorAll(`[data-btn-action="open-model-config"]`);
    rows = getAllRows_TablePreview();

    btn_actions.forEach((btn)=>{
        btn.disabled = true;
        if (btn.classList.contains("active")){
            btn.classList.remove("active");
        }
    });


    for (let i = 0; i < rows.length; i++){
        td = rows[i].querySelectorAll("td")[0].querySelector("input");
        if (td.checked || element.checked) {

            btn_actions.forEach((btn)=>{
                btn.disabled = false;
                if (btn.classList.add("active")){
                    btn.classList.add("active");
                }
            });

            break;

        }
    }
  



}
