

function create_name_file(name_process){
    let date = new Date();
    let day = date.getDate();
    let month = date.getMonth() + 1;
    let year = date.getFullYear();
    let hour = date.getHours();
    let minute = date.getMinutes();

    if (day < 10) {
        day = "0" + day;
    }
    if (month < 10) {
        month = "0" + month;
    }
    let file_name = name_process + day + "-" + month + ".-" + year + " " + hour + ":" + minute + ".txt";
    return file_name;
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

    link.setAttribute("download", " GNRE.txt");
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