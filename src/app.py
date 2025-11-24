from flask import Flask, render_template, request, redirect, url_for, flash
from warehouse_repository import (
    WarehouseRepository,
    InMemoryWarehouseRepository
)

app = Flask(__name__)
# Secret key needed for flash messages
app.secret_key = 'dev-secret-key-change-in-production'

# Dependency injection: repository instance
repository: WarehouseRepository = InMemoryWarehouseRepository()


@app.route('/')
def index():
    """Display all warehouses"""
    warehouses = repository.get_all()
    return render_template('index.html', warehouses=warehouses)


@app.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new warehouse"""
    if request.method == 'POST':
        try:
            tilavuus = float(request.form.get('tilavuus', 0))
            alku_saldo = float(request.form.get('alku_saldo', 0))
            nimi = request.form.get('nimi', '')

            repository.create(nimi, tilavuus, alku_saldo)
            return redirect(url_for('index'))
        except (ValueError, TypeError):
            flash('Virheelliset syötteet. Tarkista arvot ja yritä uudelleen.')
            return redirect(url_for('create'))

    return render_template('create.html')


@app.route('/edit/<int:warehouse_id>', methods=['GET', 'POST'])
def edit(warehouse_id: int):  # pylint: disable=too-many-statements
    """Edit an existing warehouse"""
    warehouse = repository.get_by_id(warehouse_id)
    if warehouse is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            tilavuus = float(request.form.get('tilavuus', 0))
            alku_saldo = float(request.form.get('alku_saldo', 0))
            nimi = request.form.get('nimi', '')

            repository.update(warehouse_id, nimi, tilavuus, alku_saldo)
            return redirect(url_for('index'))
        except (ValueError, TypeError):
            flash('Virheelliset syötteet. Tarkista arvot ja yritä uudelleen.')
            return redirect(url_for('edit', warehouse_id=warehouse_id))

    return render_template('edit.html', warehouse=warehouse)


@app.route('/add/<int:warehouse_id>', methods=['GET', 'POST'])
def add(warehouse_id: int):
    """Add content to an existing warehouse"""
    warehouse = repository.get_by_id(warehouse_id)
    if warehouse is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            maara = float(request.form.get('maara', 0))
            repository.add_to_warehouse(warehouse_id, maara)
            return redirect(url_for('index'))
        except (ValueError, TypeError):
            flash('Virheellinen määrä. Tarkista arvo ja yritä uudelleen.')
            return redirect(url_for('add', warehouse_id=warehouse_id))

    return render_template('add.html', warehouse=warehouse)


@app.route('/delete/<int:warehouse_id>', methods=['POST'])
def delete(warehouse_id: int):
    """Delete an existing warehouse"""
    repository.delete(warehouse_id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
