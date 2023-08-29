function changeImg(ele) {
    var theNew = document.getElementById(ele)
    var curr = document.getElementById('current')
    console.log(theNew.src, curr.src)
    curr.src = theNew.src
}