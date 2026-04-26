import webbrowser

queries = [
    'a-non-orientable-game-of-strands',
    'a-study-in-jazz',
    'akakariri',
    'appetizers',
    'big-orchard',
    'blusteaus',
    'coq-au-vin',
    'dessert',
    'french-omelette',
    'harvest-season',
    'main-course',
    'mariah-carey-is-defrosted',
    'mother-dearest',
    'operators',
    'potato-raclette',
    'previous-preserves',
    'quenelle-nantua',
    'salad',
    'the-moo-york-times',
    'trail-mixup',
    'training-course',
    'view-farming'
]

for query in queries:
    webbrowser.open(f'http://localhost:3000/puzzle/{query}/solution')
