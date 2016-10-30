function fakeScan(id) {
    $.post('/fake/id', JSON.stringify({id: id}))
}