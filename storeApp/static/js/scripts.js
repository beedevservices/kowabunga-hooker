function menu(ele) {
    var x = document.getElementById(ele)
    if(x.style.display === 'flex') {
        x.style.display = 'none'
    } else {
        x.style.display = 'flex'
        x.style.flexDirection = 'column'
    }
}