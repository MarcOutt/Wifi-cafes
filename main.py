import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(app)


class Cafe(db.Model):
    """Class representing a Cafe in the database.

    Attributes:
        id (int): Unique identifier for the cafe.
        name (str): Name of the cafe.
        map_url (str): URL link to the cafe's location on a map.
        img_url (str): URL link to an image of the cafe.
        location (str): Location of the cafe.
        seats (str): Description of available seating.
        has_toilet (bool): True if the cafe has a toilet, False otherwise.
        has_wifi (bool): True if the cafe has wifi, False otherwise.
        has_sockets (bool): True if the cafe has power sockets, False otherwise.
        can_take_calls (bool): True if the cafe allows phone calls, False otherwise.
        coffee_price (str): Price of coffee at the cafe.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        """Converts Cafe object to a dictionary."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    """Renders the home page."""
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    """Returns a random cafe from the database."""
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    """Returns all cafes in the database."""
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def get_search_cafes():
    """Returns cafes in the specified location."""
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not found": "Sorry, we don't have a cafe at that location."}), 404


@app.route("/add", methods=['POST'])
def suggest_cafe_wifi():
    """Adds a new cafe to the database."""
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


@app.route("/update-price/<int:cafe_id>", methods=['PATCH'])
def update_cafe_price(cafe_id):
    """Updates the coffee price of a cafe."""
    new_price = request.args.get("new_price")
    cafe = db.get_or_404(Cafe, cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "The price has been updated with success"})
    else:
        return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in the database."})


@app.route("/update-price/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    """Deletes a cafe from the database."""
    api_key = request.args.get('api_key')
    cafe = db.get_or_404(Cafe, cafe_id)
    if api_key == "TopSecretAPIKey":
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "The cafe has been deleted with success"})
        else:
            return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in the database."})
    else:
        return jsonify(error={"Not Permission": "Sorry, you don't have permission"})


if __name__ == '__main__':
    app.run(debug=True)
