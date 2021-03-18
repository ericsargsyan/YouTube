let progress = document.getElementById('progressbar');
let totalHeight = document.getElementsByClassName('contain').scrollHeight - window.innerHeight;
window.onscroll = function (){
    let progressHeight = (window. / totalHeight) * 100
    progress.style.height = progressHeight + "%";
}
