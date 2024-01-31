const list_id_acessorias = new Array();
const list_dates = new Array();
const list_values = new Array();

// ----------------------- MENU RULES -----------------------
function selectOptionRules(li, csrf_token, url) {
    console.log(li)

    var id_company, numero_conta_debito, tag;
    var data_option = li.getAttribute("data-option-rule");
    var liList = li.parentNode.children;


    for (var i = 0; i < liList.length; i++) {
        if (liList[i] === li) {
            liList[i].classList.add("active-option");
        } else {
            liList[i].classList.remove("active-option");
        }
    }

    // console.log(`---> data_option: ${data_option}`)
    const body = {};
    const headers = {
        "X-CSRFToken": csrf_token,
    };
    if (data_option == "rules_created"){
        document.querySelector(".block-create-tag-rule").style.display = "none";
        document.querySelector(".block-create-all-rules").style.display = "flex";
        document.querySelector(".block-create-all-PC").style.display = "none";
        console.log(`\n\n ----> URL: ${url} `)
        fetch(url, {
            method: "POST",
            headers: headers,
            body: JSON.stringify(body)
        }).then((data)=>{
            return data.json();
        }).then((data)=>{
            console.log(data);

            const table_all_tag_rules = document.getElementById("table-all-tag-rules");
            table_all_tag_rules.querySelector("tbody").remove();
            table_all_tag_rules.innerHTML += "<tbody></tbody>";

            for (let x in data["data"]){
                id_company = data["data"][x]["id_company"]
                company_name = data["data"][x]["company_name"]
                numero_conta_debito = data["data"][x]["numero_conta_debito"]
                tag = data["data"][x]["tag"]
                created_at = data["data"][x]["created_at"]
                update_at = data["data"][x]["update_at"]
                
                table_all_tag_rules.querySelector("tbody").innerHTML += `
                    <tr>
                        <td>${id_company}</td>
                        <td>${company_name}</td>
                        <td>${numero_conta_debito}</td>
                        <td>${tag}</td>
                        <td>${created_at}</td>
                        <td>${update_at}</td>
                    <tr>
                `;
                console.log(`
                    >> id_company: ${id_company}
                    >> numero_conta_debito: ${numero_conta_debito}
                    >> tag: ${tag}
                    >> created_at: ${created_at}
                    >> update_at: ${update_at}
                `)
            }
        })
    } else if (data_option == "create_new_rule") {
        document.querySelector(".block-create-tag-rule").style.display = "flex";
        document.querySelector(".block-create-all-rules").style.display = "none";
        document.querySelector(".block-create-all-PC").style.display = "none";
        
    } else if (data_option == "create_new_PC") {
        document.querySelector(".block-create-all-PC").style.display = "flex";
        document.querySelector(".block-create-tag-rule").style.display = "none";
        document.querySelector(".block-create-all-rules").style.display = "none";
    }
}

function removeTagBox (element) {
    console.log(element);
    element.remove();

    valueToRemove = element.innerHTML;

    const index_01 = list_id_acessorias.indexOf(valueToRemove);
    const index_02 = list_dates.indexOf(valueToRemove);
    const index_03 = list_values.indexOf(valueToRemove);

    if (index_01 > -1) {
        list_id_acessorias.splice(index_01, 1);
    }
    if (index_02 > -1) {
        list_dates.splice(index_02, 1);
    }
    if (index_03 > -1) {
        list_values.splice(index_03, 1);
    }

    // console.log(`
    //     list_id_acessorias: ${list_id_acessorias}
    //     list_dates: ${list_dates}
    //     list_values: ${list_values}
    // `)

}

// ----------------------- CNPJ/CPF | COMPANY -----------------------
function addNewTagBox(element){
    var id_acessorias, elem, element_tag, new_element, index_array;
    elem = element.getAttribute("data-add-element");
    console.log(elem)

    id_acessorias = document.getElementById(elem).value;
    console.log(id_acessorias)
    console.log("elem: ", elem)

    if (id_acessorias != "select_company") {
        document.getElementById(elem).style.borderColor = "var(--color-principal-cinza)";
        

        index_array = `${elem}-${id_acessorias}`
        element_tag = document.querySelector(`[data-id-acessorias-${elem}="${id_acessorias}"]`);
        if (!list_id_acessorias.includes(element_tag.innerHTML)){
            new_element = `<span onclick="removeTagBox(this);" data-id-acessorias-${elem}="${id_acessorias}" >${element_tag.innerHTML}</span>`;
            console.log(" --------------------- new_element --------------------- ")
            console.log(new_element)

            document.querySelector(`.block-tag-${elem}`).innerHTML += new_element;
            // list_id_acessorias.push(index_array);
            list_id_acessorias.push(element_tag.innerHTML);
        }
    
        console.log(list_id_acessorias)
    } else {
        document.getElementById(elem).style.borderColor = "red";
    }

}

// ----------------------- ADD NEW TAG DATE -----------------------
function parseRegexDate(str) {
    var m = str.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/);
    return (m);
}
function parseRegexValue(str) {
    var m = str.match(/^\d+\.\d{2}$/);
    return (m);
}
function validValueDate(element){
    var test, elem, element_btn;
    test = parseRegexDate(element.value);
    elem = element.id;

    element_btn = document.getElementById(elem);
    console.log(elem)    

    if (element.value != ""){
        if (test == null){
            element.style.borderColor = "red";
            element.style.background = "#f1b7d0";
        } else {
            element.style.borderColor = "green";
            element.style.background = "#c0f5c0";
            document.querySelector("[data-add-tag-dinamic=]")
            element_btn.disabled = true;
        }
    } else {
        element.style.background = "#fff";
        element.style.borderColor = "var(--color-principal-cinza)";
    }
}

function validValue(element){
    var test, elem, element_btn, name_attr;
    test = parseRegexValue(element.value);

    elem = element.id;
    name_attr = elem.replace("add-", "");


    console.log(elem)
    element_btn = document.querySelector(`[data-add-tag-dinamic="${name_attr}"]`);
    console.log(element_btn)   

    if (element.value != ""){
        if (test == null ){
            element.style.borderColor = "red";
            element.style.background = "#f1b7d0";
            element_btn.disabled = true;
        } else {
            element.style.borderColor = "green";
            element.style.background = "#c0f5c0";
            element_btn.disabled = false;
        }
    } else {
        element.style.background = "#fff";
        element.style.borderColor = "var(--color-principal-cinza)";
        element_btn.disabled = false;
    }
}


function addNewTagBoxDate(element){
    var attr, new_element, value;
    attr = element.getAttribute("data-add-tag-dinamic");
    value = document.getElementById(`add-${attr}`).value;
    test = parseRegexDate(value)

    if(value != "" && test != null){
        if (!list_dates.includes(value)){
            new_element = `<span onclick="removeTagBox(this);">${value}</span>`
            document.querySelector(`.block-${attr}`).innerHTML += new_element;
            document.getElementById(`add-${attr}`).style.borderColor = "var(--color-principal-cinza)";
            document.getElementById(`add-${attr}`).style.background = "#fff";
            document.getElementById(`add-${attr}`).value = "";

            list_dates.push(value);
            return;
        }
    } else {
        document.getElementById(`add-${attr}`).style.borderColor = "red";
        return;
    }
    // validValueDate(element)
}

// ----------------------- ADD NEW TAG VALUE -----------------------
function addNewTagBoxValue(element){
    var attr, new_element, value;
    attr = element.getAttribute("data-add-tag-dinamic");
    value = document.getElementById(`add-${attr}`).value;
    console.log(value)
    test = parseRegexValue(value);
    console.log(test)

    if(value != ""){
        if (!list_values.includes(value)){
            new_element = `<span onclick="removeTagBox(this);">${value}</span>`
            document.querySelector(`.block-${attr}`).innerHTML += new_element;
            document.getElementById(`add-${attr}`).style.borderColor = "var(--color-principal-cinza)";
            document.getElementById(`add-${attr}`).style.background = "#fff";
            document.getElementById(`add-${attr}`).value = "";

            list_values.push(value);
        }
    } else {
        document.getElementById(`add-${attr}`).style.borderColor = "red";
    }

}




// ---------------------- SAVE NEW RULE TO DATABASE ----------------------
function saveNewRule(csrf_token, host, sub_directory, path_dir_url){
    var numero_conta_debito, tags_date, tags_value, tags_cnpj_cpf, tags_companies;
    const obj_tags = {
        "numero_conta_debito": "",
        "tags_date": Array(),
        "tags_value": Array(),
        "tags_cnpj_cpf": Array(),
        "tags_companies": Array(),
    };

    tags_date = document.querySelector(".block-tag-new-date").querySelectorAll("span");
    tags_value = document.querySelector(".block-tag-new-value").querySelectorAll("span");
    tags_cnpj_cpf = document.querySelector(".block-tag-data-cnpj-cpf").querySelectorAll("span"); // block-tag-data-cnpj-cpf
    tags_companies = document.querySelector(".block-tag-data-companies").querySelectorAll("span"); // block-tag-data-companies
    numero_conta_debito = document.getElementById("numero_conta_debito");

    console.log("\n\n ------ tags_date ------ ")
    console.log(tags_date)
    tags_date.forEach((tag)=>{
        obj_tags.tags_date.push(tag.innerText);
    });
    console.log("\n\n ------ tags_value ------ ")
    console.log(tags_value)
    tags_value.forEach((tag)=>{
        obj_tags.tags_value.push(tag.innerText);
    });
    console.log("\n\n ------ tags_cnpj_cpf ------ ")
    console.log(tags_cnpj_cpf)
    tags_cnpj_cpf.forEach((tag)=>{
        obj_tags.tags_cnpj_cpf.push(tag.innerText);
    });
    console.log("\n\n ------ tags_companies ------ ")
    console.log(tags_companies)
    tags_companies.forEach((tag)=>{
        obj_tags.tags_companies.push(tag.innerText);
    });

    console.log("\n\n ------ numero_conta_debito ------ ")
    console.log(numero_conta_debito.value)
    obj_tags.numero_conta_debito = numero_conta_debito.value;

    console.log("\n\n\n ------ obj_tags ------ ")
    console.log(obj_tags)
    
    
    if ( obj_tags.numero_conta_debito != "" &  obj_tags.tags_date.length > 0 || obj_tags.tags_value.length > 0 || obj_tags.tags_cnpj_cpf.length > 0 || obj_tags.tags_companies.length > 0 ){
        
        url = `${host}/${sub_directory}/${path_dir_url}/`;
        headers = {
            "X-CSRFToken": csrf_token,
        }
        console.log("\n\n\n ------ url ------ ")
        console.log(url)
        console.log("\n\n\n ------ headers ------ ")
        console.log(headers)
        console.log("\n\n\n ------ obj_tags ------ ")
        console.log(obj_tags)

        fetch(url, {
            method: "POST",
            headers: headers,
            body: JSON.stringify(obj_tags)
        }).then((data)=>{
            return data.json();
        }).then((data)=>{
            console.log(data)
        })

    } else {
        console.log(" -------------- error -------------- ")
    }
    
}
