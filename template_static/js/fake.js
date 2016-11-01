function fakeScan(id) {
    $.post('/fake/id', JSON.stringify({id: id}))
}

function flashCard() {
    $.post('/fake/id', JSON.stringify({id: $('#cardid').val()}))
}