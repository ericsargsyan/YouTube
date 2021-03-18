function showdiv(){
    document.getElementById("alert").style.visibility = "visible";
}

setTimeout("showdiv()", 100)

function hidediv(){
    document.getElementById("alert").style.visibility = "hidden";
}

setTimeout("hidediv()", 3000)