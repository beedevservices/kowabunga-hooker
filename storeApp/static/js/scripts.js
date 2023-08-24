function menu(ele) {
    var x = document.getElementById(ele)
    if(x.style.display === 'flex') {
        x.style.display = 'none'
    } else {
        x.style.display = 'flex'
        x.style.flexDirection = 'column'
    }
}

function auth() {
    var l = document.getElementById('login')
    var r = document.getElementById('reg')
    var t = document.getElementById('text')
    if (r.style.display === 'flex') {
        r.style.display = 'none'
        l.style.display = 'flex'
        l.style.flexDirection = 'column';
        t.innerHTML = "Don't have an account? Register"
    } else {
        l.style.display = 'none'
        r.style.display = 'flex'
        r.style.flexDirection = 'column';
        t.innerHTML = 'Already have an account? Login'
    }
}