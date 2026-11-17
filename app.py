
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "mini_instagram_secret"

# Dictionary to store Instagram users
instagram = {}


@app.route("/")
def home():
    return render_template("index.html", instagram=instagram)


@app.route("/create_account", methods=["POST"])
def create_account():
    username = request.form["username"]
    bio = request.form["bio"]

    if username not in instagram:
        instagram[username] = {
            "bio": bio,
            "followers": 0,
            "following": [],
            "posts": {}
        }
        flash("Account created successfully!")
    else:
        flash("Username already exists!")

    return redirect(url_for("home"))


@app.route("/create_post", methods=["POST"])
def create_post():
    username = request.form["username"]
    post = request.form["post"]

    if username in instagram:
        post_id = max(instagram[username]["posts"], default=0) + 1

        instagram[username]["posts"][post_id] = {
            "content": post,
            "likes": 0
        }

        flash("Post uploaded successfully!")
    else:
        flash("User not found!")

    return redirect(url_for("home"))


@app.route("/like_post", methods=["POST"])
def like_post():
    username = request.form["username"]
    post_id = int(request.form["post_id"])

    if username in instagram and post_id in instagram[username]["posts"]:
        instagram[username]["posts"][post_id]["likes"] += 1
        flash("Post liked successfully!")
    else:
        flash("Post not found!")

    return redirect(url_for("home"))


@app.route("/follow", methods=["POST"])
def follow():
    username = request.form["username"]
    target = request.form["target"]

    if username in instagram and target in instagram:
        if username != target and target not in instagram[username]["following"]:
            instagram[username]["following"].append(target)
            instagram[target]["followers"] += 1
            flash("You are now following " + target)
        else:
            flash("Invalid request or already following!")
    else:
        flash("User not found!")

    return redirect(url_for("home"))


@app.route("/update_bio", methods=["POST"])
def update_bio():
    username = request.form["username"]
    bio = request.form["bio"]

    if username in instagram:
        instagram[username]["bio"] = bio
        flash("Bio updated successfully!")
    else:
        flash("User not found!")

    return redirect(url_for("home"))


@app.route("/delete_post", methods=["POST"])
def delete_post():
    username = request.form["username"]
    post_id = int(request.form["post_id"])

    if username in instagram and post_id in instagram[username]["posts"]:
        instagram[username]["posts"].pop(post_id)
        flash("Post deleted successfully!")
    else:
        flash("Post not found!")

    return redirect(url_for("home"))


@app.route("/profile", methods=["POST"])
def profile():
    username = request.form["username"]

    if username in instagram:
        return render_template(
            "index.html",
            instagram=instagram,
            selected_user=username
        )

    flash("User not found!")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
