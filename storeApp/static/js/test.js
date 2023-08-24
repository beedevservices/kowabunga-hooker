function apiTest() {
    fetch(`http://127.0.0.1:8000/api/allCustomers`)
    .then(res => res.json())
    .then(data => {
        console.log('theData', data)
        // theList = data.customers[0].customer.user
        // console.log('theList', theList)
    })
}
apiTest()