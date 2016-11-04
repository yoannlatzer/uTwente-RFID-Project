import user_sql as userActions
import product_sql as itemActions
import userfr_sql as userFrontendActions

def demoData():
    print('Insert demo data')
    userActions.newUser('Admin', 's1000000', 'password', '0', 'tag')
    userActions.makeAdmin(1)
    userActions.newUser('Pieter-Tjerk', 'x1000001', 'password', '1', 'Studenten kaart')
    itemActions.newItem('Bueno', 10, 0.54, 'bueno.png', 2)
    itemActions.newItem('Bastogne', 10, 0.54, 'snacks/bastogne.png', 2)
    itemActions.newItem('Chips', 10, 0.54, 'snacks/chips.png', 2)
    itemActions.newItem('Gevulde Koek', 10, 0.54, 'snacks/Gevulde-koek.png', 2)
    itemActions.newItem('Kinder', 10, 0.54, 'snacks/kinder.png', 2)
    itemActions.newItem('Liga', 10, 0.54, 'snacks/liga.png', 2)
    itemActions.newItem('M&M\'s', 10, 0.54, 'snacks/m&m.png', 2)
    itemActions.newItem('Maltesers', 10, 0.54, 'snacks/maltesers.png', 2)
    itemActions.newItem('Mars', 10, 0.54, 'snacks/mars.png', 2)
    itemActions.newItem('Milky Way', 10, 0.54, 'snacks/milky-way.png', 2)
    itemActions.newItem('Oreo', 10, 0.54, 'snacks/oreo.png', 2)
    itemActions.newItem('Snickers', 10, 0.54, 'snacks/snickers.png', 2)
    itemActions.newItem('Sultana', 10, 0.54, 'snacks/sultana.png', 2)
    itemActions.newItem('Timeout', 10, 0.54, 'snacks/timeout.png', 2)
    itemActions.newItem('Timeout Granen', 10, 0.54, 'snacks/timeout_granen.png', 2)
    itemActions.newItem('Tuc', 10, 0.54, 'snacks/tuc.png', 2)
    itemActions.newItem('Twix', 10, 0.54, 'snacks/twix.png', 2)
    itemActions.newItem('Bagel', 104, 0.66, 'bagel.png', 1)
    itemActions.newItem('Appeltje', 4, 0.26, 'food/appeltje.png', 1)
    itemActions.newItem('Banaan', 4, 0.66, 'food/banaan.png', 1)
    itemActions.newItem('Frikandelbroodje', 4, 0.66, 'food/frikandelbroodje.png', 1)
    itemActions.newItem('Groene appel', 4, 0.66, 'food/groene_appel.png', 1)
    itemActions.newItem('Muffin', 4, 0.66, 'food/muffin.png', 1)
    itemActions.newItem('Muffin Chocolate', 4, 0.66, 'food/muffin_chocolate.png', 1)
    itemActions.newItem('Saucijzen', 4, 0.66, 'food/saucijzen.png', 1)
    itemActions.newItem('Snelle Jelle', 4, 0.66, 'food/snelle_jelle.png', 1)
    itemActions.newItem('Fristi', 15, 1.01, 'fristi.png', 0)
    itemActions.newItem('Coca Cola', 25, 0.99, 'drinks/coca-cola.png', 0)
    itemActions.newItem('Dr Pepper', 25, 0.99, 'drinks/dr-pepper.png', 0)
    itemActions.newItem('Fanta', 25, 0.99, 'drinks/fanta.png', 0)
    itemActions.newItem('Fanta Casis', 25, 0.99, 'drinks/fanta-casis.png', 0)
    itemActions.newItem('Redbull', 25, 0.99, 'drinks/redbull.png', 0)
    itemActions.newItem('Sprite', 25, 0.99, 'drinks/sprite.png', 0)
    userFrontendActions.CreateTransAndBask(2, [
        (26, 20),
        (19, 4),
        (20, 2)
    ])
    userFrontendActions.CreateTransAndBask(2, [
        (26, 1),
        (27, 5)
    ])
    print('Database is ready')