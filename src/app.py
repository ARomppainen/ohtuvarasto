from flask import Flask, render_template, request, redirect, url_for
from varasto import Varasto

app = Flask(__name__)

# In-memory storage for warehouses
warehouses = {}


@app.route('/')
def index():
    """Display all warehouses"""
    return render_template('index.html', warehouses=warehouses)


@app.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new warehouse"""
    if request.method == 'POST':
        new_id = max(warehouses.keys(), default=0) + 1
        tilavuus = float(request.form.get('tilavuus', 0))
        alku_saldo = float(request.form.get('alku_saldo', 0))
        nimi = request.form.get('nimi', '')

        warehouses[new_id] = {
            'id': new_id,
            'nimi': nimi,
            'varasto': Varasto(tilavuus, alku_saldo)
        }
        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/edit/<int:warehouse_id>', methods=['GET', 'POST'])
def edit(warehouse_id):
    """Edit an existing warehouse"""
    if warehouse_id not in warehouses:
        return redirect(url_for('index'))

    if request.method == 'POST':
        tilavuus = float(request.form.get('tilavuus', 0))
        alku_saldo = float(request.form.get('alku_saldo', 0))
        nimi = request.form.get('nimi', '')

        warehouses[warehouse_id]['nimi'] = nimi
        warehouses[warehouse_id]['varasto'] = Varasto(tilavuus, alku_saldo)
        return redirect(url_for('index'))

    return render_template('edit.html', warehouse=warehouses[warehouse_id])


@app.route('/add/<int:warehouse_id>', methods=['GET', 'POST'])
def add(warehouse_id):
    """Add content to an existing warehouse"""
    if warehouse_id not in warehouses:
        return redirect(url_for('index'))

    if request.method == 'POST':
        maara = float(request.form.get('maara', 0))
        warehouses[warehouse_id]['varasto'].lisaa_varastoon(maara)
        return redirect(url_for('index'))

    return render_template('add.html', warehouse=warehouses[warehouse_id])


@app.route('/delete/<int:warehouse_id>', methods=['POST'])
def delete(warehouse_id):
    """Delete an existing warehouse"""
    if warehouse_id in warehouses:
        del warehouses[warehouse_id]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
