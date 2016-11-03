/**
 * Created by ranganathan on 11/3/16.
 */

function primarynaturedisablechackebox(){
    var pn = document.getElementById("otherPrimaryNature");
    if(pn.checked)
        document.getElementById("apprenticeship[otherNatureOfWork]").disabled = false;
    else
        document.getElementById("apprenticeship[otherNatureOfWork]").disabled = true;
}

function priorWorkdisablechackebox(){
    var pw = document.getElementById("otherPrimaryWork");
    if(pw.checked)
        document.getElementById("apprenticeship[otherAmountOfWork]").disabled = false;
    else
        document.getElementById("apprenticeship[otherAmountOfWork]").disabled = true;
}

function financestextboxdisabled(){
    var f = document.getElementById("isNotSure");
    if(f.checked)
        document.getElementById("apprenticeship[Finances[speedType]]").disabled = true;
    else
        document.getElementById("apprenticeship[Finances[speedType]]").disabled = false;
}
