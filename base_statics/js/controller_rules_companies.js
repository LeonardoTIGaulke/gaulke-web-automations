function filterTableAllCompanies(str){
    var table_companies, value_filter, rows, td, id_client, razao_social, cnpj_cpf;
    table_companies = document.querySelector(".container-all-companies-clients").querySelector("table");
    rows = table_companies.querySelector("tbody").querySelectorAll("tr");
    value_filter = str.value.toUpperCase();

    rows.forEach((row)=>{
        console.log("\n\n -------------------------------- ")
        console.log(`str: ${value_filter}`)
        console.log(row)
        td = row.querySelectorAll("td");
        id_client = td[0].innerText.toUpperCase();
        razao_social = td[1].innerText.toUpperCase();
        cnpj_cpf = td[2].innerText.toUpperCase();
        console.log(`
            >> value_filter: ${value_filter}
            --------------------
            >> id_client: ${id_client}
            >> razao_social: ${razao_social}
            >> cnpj_cpf: ${cnpj_cpf}
        `)
        
        if (id_client.indexOf(value_filter) > -1 || razao_social.indexOf(value_filter) > -1 || cnpj_cpf.indexOf(value_filter) > -1) {
            console.log("filtro encontrado...");
            row.style.display = "table-row";
        } else {
            console.log("filtro não encontrado...");
            row.style.display = "none";
        }
    });
};

function openModalEditCompany(element, url, csrf_token){
    var id_company, row_company, company_name, cnpj, code_account;

    // adiciona blur ao abrir modal
    let container_elements = document.querySelector(".base-elements");
    let container_footer = document.querySelector(".container-footer");
    let container_code_company = document.querySelector(".container-all-companies-to-auth");
    
    container_elements.classList.toggle("filter-blur-10");
    container_footer.classList.toggle("filter-blur-10");
    container_code_company.classList.toggle("filter-blur-10");

    
    id_company = element.getAttribute("data-id-client");
    row_company = document.querySelector(`[data-row-company=company-${id_company}]`);
    company_name = row_company.querySelectorAll("td")[1].innerText;
    cnpj = row_company.querySelectorAll("td")[2].innerText;
    console.log(element)
    console.log(row_company)
    console.log(`
        -----------------------------------
        >> id_company: ${id_company}
        >> company_name: ${company_name}
        >> cnpj: ${cnpj}
    `)

    const aPromisse = new Promise((resolve, reject)=>{
        let headers = {
            "X-CSRFToken": csrf_token,
        };
        let body = {
            "id_company": id_company,
        }
        let data = fetch(url, {
            method: "POST",
            headers: headers,
            body: JSON.stringify(body)
        });
        resolve(data);
    }).then((data)=>{
        return data.json();
    }).then((data)=>{
        console.log(data);
        document.getElementById("code_account").value = data.code_account;
    });


    document.getElementById("company").value = company_name;
    document.getElementById("code_company").value = id_company;
    document.getElementById("cnpj_company").value = cnpj;
    document.querySelector(".container-modal-config-company").classList.toggle("active");

};


function closeModalConfiAccountsCompany() {
    let container_elements = document.querySelector(".base-elements");
    let container_footer = document.querySelector(".container-footer");
    let container_code_company = document.querySelector(".container-all-companies-to-auth");
    container_elements.classList.toggle("filter-blur-10");
    container_footer.classList.toggle("filter-blur-10");
    container_code_company.classList.toggle("filter-blur-10");
    document.querySelector(".container-modal-config-company").classList.toggle("active");
};

function selectModelAccount(element) {
    var model;
    model = element.getAttribute("data-model-account");
    console.log(model)
    if (model == "code_debit"){
        document.getElementById("code_credit").checked =  false;
    } else {
        document.getElementById("code_debit").checked =  false;
    }
};

function saveCodeAccountCompany(url, csrf_token){

    const code_company = document.getElementById("code_company").value;
    const company = document.getElementById("company").value;
    const code_account = document.getElementById("code_account").value;

  
    obj_config_account = {
        "code_company": code_company,
        "company": company,
        "code_account": code_account,
    };
    headers = {
        "X-CSRFToken": csrf_token,
    }

    console.log(url, csrf_token)

    fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(obj_config_account)
    }).then((data)=>{
        return data.json();
    }).then((data)=>{
        console.log(data)
    });
    

};


// const rulesTag_ToPost = new Array();

// function selectTag(e){
//     // e.style.display = "none"
//     // e.remove();

//     var status_filter, index_tag, content_filter_tags;

//     content_filter_tags = document.querySelector(".content-filter-tags");

    
//     console.log(e);
//     // console.log (e.querySelector());
//     var contentTag = e.querySelector("span").textContent.trim();

//     status_filter = e.getAttribute("data-status-filter");
//     index_tag = e.getAttribute("data-index-tag");

//     if (status_filter == "0"){
//         e.setAttribute("data-status-filter", "1");
//         content_filter_tags.appendChild(e);
//         // document.querySelector(".content-config-new-rule").appendChild(e);
        
        
//         // rulesTag_ToPost.push(contentTag);

//     } else {
//         e.setAttribute("data-status-filter", "0");
//         // document.querySelector(".content-all-tags").appendChild(e);
        
//         let itemTag = document.querySelector(".content-all-tags").getElementsByTagName("li")[parseInt(index_tag)-1]
//         document.querySelector(".content-all-tags").insertBefore(e, itemTag);
//     }
//     console.log(rulesTag_ToPost, status_filter, index_tag);

//     if (content_filter_tags.querySelectorAll("li").length > 0){
//         document.querySelector(".content-config-new-rule").style.display = "flex";
//         // document.querySelector(".content-config-new-rule").classList.toggle("visible");
//     } else {
//         document.querySelector(".content-config-new-rule").style.display = "none";
//     }
// }

// function filterAllTags(e){
//     console.log(e)
//     var txtValue, all_tags, tag, value_input;

//     value_input = e.value.toUpperCase();
//     all_tags = document.querySelector(".content-all-tags").querySelectorAll("li");

//     for (let i=0; i < all_tags.length; i++){
//         tag = all_tags[i].querySelector("span");
//         txtValue = tag.textContent.toUpperCase() || tag.innerText.toUpperCase();
//         console.log( i, value_input, txtValue, txtValue.indexOf(value_input));
        
//         if ( txtValue.indexOf(value_input) > -1){
//             all_tags[i].style.display = "flex";
//         } else {
//             all_tags[i].style.display = "none";
//         }
//     }
//     console.log(value_input)
// }


// function create_RuleTag(csrf_token, host, sub_directory, path_dir_url, username){
//     var tags, value_tag, numero_conta_debito, decription_rule, list_tags, object_post_tags, url, headers;

//     numero_conta_debito = document.getElementById("numero_conta_debito");
//     decription_rule = document.getElementById("decription_rule");

//     if (numero_conta_debito.value != "" && decription_rule.value != ""){
//         numero_conta_debito.style.borderColor = "var(--color-principal-laranja-claro)";
//         decription_rule.style.borderColor = "var(--color-principal-laranja-claro)";
        

//         list_tags = new Array();
//         tags = document.querySelector(".content-filter-tags").querySelectorAll("li");
//         tags.forEach((tag)=>{
//             value_tag = tag.querySelector("span").innerText;
//             list_tags.push(value_tag);
            
//             console.log(value_tag);
    
//             console.log(url);
//         });
        
//         url = `${host}/${sub_directory}/${path_dir_url}/`;
//         object_post_tags = {
//             numero_conta_debito: numero_conta_debito.value,
//             decription_rule: decription_rule.value,
//             list_tags: list_tags,
//             username: username
//         };
//         headers = {
//             "X-CSRFToken": csrf_token,
//         }
    
//         console.log(object_post_tags)

//         document.querySelector(".block-btn-actions").disabled = true;
    
//         fetch(url, {
//             method: "POST",
//             headers: headers,
//             body: JSON.stringify(object_post_tags)
//         }).then((data)=>{
//             return data.json();
//         }).then((data)=>{
//             console.log(data)
//             console.log(data.status_process)
//             const element_message = document.querySelector(".message-status-process");
//             element_message.style.display = "flex";


//             element_message.querySelector("p").classList.remove("active-success");
//             element_message.querySelector("p").classList.remove("active-error");

//             if (data.status_process){
//                 element_message.querySelector("p").textContent = "Regra criada com sucesso!";
//                 element_message.querySelector("p").classList.add("active-success");
            
//             } else {
//                 element_message.querySelector("p").textContent = "Essa regra já existe para este usuário.";
//                 element_message.querySelector("p").classList.add("active-error");
                

//             }

//             for (let i=0; i < 10; i++){
//                 try {
//                     clearInterval(i);
//                     console.log(i, "limpo...")
//                 } catch (error) {}
//             }
//             setInterval(()=>{
//                 element_message.style.display = "none";
//                 document.querySelector(".block-btn-actions").setAttribute("disabled", true);

//             }, 4000);
//         })
//     } else {
//         numero_conta_debito.style.borderColor = "red";
//         decription_rule.style.borderColor = "red";
//     }

// }

// // function reloadPage(){
// //     document.querySelector(".btn-reload").querySelector("i").classList.toggle("active");
    
// // }
// function reloadPage() {
//     location.reload();
//     const icon = document.querySelector('#icon-reload');
//     let rotation = 0;
//     const intervalId = setInterval(() => {
//       rotation += 10;
//       icon.style.transform = `rotate(${rotation}deg)`;
//     }, 20);
//   }

// function selectActionMenu(e){

//     var options;
//     // menu-active

//     options = document.querySelector(".block-menu-actions").querySelector("ul").querySelectorAll("li");
//     console.log(" ----------------------------------------- ")
//     console.log(options)
//     console.log(e.getAttribute("data-action"))
//     console.log(" ----------------------------------------- ")

//     options.forEach((option)=>{
//         console.log("\n\n -------- OPTION -------- ")
//         if (option.classList.contains("menu-active")){
//             console.log(" --------->>>>> contem")
//         } else {
//             console.log(" --------->>>>> não contem")
//         }

//         // if(option.)
//     })
// }