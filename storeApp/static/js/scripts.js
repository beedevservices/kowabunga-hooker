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

// Generate review order
let rootUrl = 'http://127.0.0.1:8000/api/'
let allCust = 'allCustomers/'
let allProds = 'allProducts/'
let allOrders = 'allOrderNumbers/'
let allInvs = 'allInvoiceNumbers/'
let oneCust = 'oneCustomer/'
let oneProd = 'oneProduct/'
let oneOrder = 'oneOrderNumber/'
let oneInv = 'oneInvoiceNumber/'
let allData = 'allData/'

// console.log(`${rootUrl}${cust}`)

async function invoiceData() {
    var theUser = document.getElementById('theUser').value
    var theOrder = document.getElementById('theOrder').value
    console.log(theUser, theOrder)
    var res = await fetch(`${rootUrl}${allData}`)
    var data = await res.json()
    console.log('the data', data)

    var order
    var user
    for(let o = 0; o < data.theOrders.length; o++) {
        if(data.theOrders[o]['orderNum'] == theOrder) {
            // console.log('yay')?
            console.log(data.theOrders[o])
            order = data.theOrders[o]
        } 
    }
    // console.log(order)
    for(let u = 0; u < data.users.length; u++) {
        // console.log(data.users[u])
        if(data.users[u]['id'] == theUser) {
            console.log(data.users[u])
            user = data.users[u]
        } 
    }
    var orderProds = []
    for(let i = 0; i < data.theItems.length; i++) {
        if(data.theItems[i]['orderNum_id'] == order.id) {
            orderProds.push(data.theItems[i])
            console.log('the items', orderProds)
        }
    }
    var div = document.createElement('div')
    for(i = 0; i < orderProds.length; i++) {
        for(p = 0; p < data.theProducts.length; p++) {
            if(data.theProducts[p]['id'] == i['id']) {
                var prodh3 = document.createElement('h3')
                var prodname = document.createTextNode(data.theProducts[p]['name'])
                prodh3.appendChild(prodname)
                div.appendChild(prodh3)
            }
        }
    }
    document.getElementById('print').append(div)
}

// function info() {
//     fetch(`${rootUrl}${cust}`)
//     .then(res => res.json())
//     .then(data => {
//         data = data['customers']
//         console.log(data)
//     })
// }
