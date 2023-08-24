let rootUrl = 'http://127.0.0.1:8000/api/'
let cust = 'allCustomers/'
let prod = 'allProducts/'
let ord = 'allOrderNumbers/'
let inv = 'allInvoiceNumbers/'

console.log(`${rootUrl}${cust}`)

function info() {
    fetch(`${rootUrl}${cust}`)
    .then(res => res.json())
    .then(data => {
        data = data['customers']
        console.log(data)
    })
}
info()