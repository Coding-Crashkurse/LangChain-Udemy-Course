from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    user_message = None
    ai_message = None

    if request.method == "POST":
        user_message = request.form.get("user_message")
        ai_message = f"AI response to: {user_message}"

    return render_template(
        "index.html", user_message=user_message, ai_message=ai_message
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=4444)
