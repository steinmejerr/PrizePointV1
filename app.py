import os

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

from state import (
    PRIZES,
    add_prize,
    finish_order,
    register_ticket_balance,
    start_order,
    state,
)


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "development-secret")


@app.get("/")
def display():
    return render_template(
        "display.html",
        state=state,
    )


@app.get("/mobile")
def mobile():
    return render_template(
        "mobile.html",
        state=state,
        prizes=PRIZES,
    )

@app.get("/api/state")
def api_state():
    return jsonify(
        {
            "active": state["active"],
            "side": state["side"],
            "starting_balance": state["starting_balance"],
            "remaining_balance": state["remaining_balance"],
            "prizes": state["prizes"],
        }
    )

@app.get("/nfc/start/<side>")
def nfc_start(side):
    if side not in ("left", "right"):
        flash("Ugyldig side.", "error")
        return redirect(url_for("mobile"))

    success, message = start_order(side)

    flash(message, "success" if success else "error")

    return redirect(url_for("mobile"))


@app.get("/scan-tickets")
def scan_tickets():
    if not state["active"]:
        flash("Start først en ekspedition.", "error")
        return redirect(url_for("mobile"))

    return render_template(
        "scan_tickets.html",
        state=state,
    )


@app.post("/register-ticket")
def register_ticket():
    if not state["active"]:
        flash("Der er ingen aktiv ekspedition.", "error")
        return redirect(url_for("mobile"))

    barcode = request.form.get("barcode", "").strip()

    try:
        amount = int(barcode)
    except ValueError:
        flash(
            "Billetstregkoden kunne ikke aflæses som en billetsaldo.",
            "error",
        )
        return redirect(url_for("scan_tickets"))

    if amount <= 0:
        flash("Billetsaldoen skal være større end 0.", "error")
        return redirect(url_for("scan_tickets"))

    success, message = register_ticket_balance(amount)

    flash(message, "success" if success else "error")

    return redirect(url_for("mobile"))


@app.get("/nfc/prize/<slug>")
def nfc_prize(slug):
    success, message = add_prize(slug)

    flash(message, "success" if success else "error")

    return redirect(url_for("mobile"))


@app.post("/finish")
def finish():
    success, message = finish_order()

    flash(message, "success" if success else "error")

    return redirect(url_for("mobile"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True,
    )