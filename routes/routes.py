from flask import Blueprint, render_template, request, redirect, url_for
# from app.services.file_processor import process_file

main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    # if request.method == "POST":
    #     uploaded_file = request.files["file"]
    #     if uploaded_file.filename != "":
    #         file_path = f"uploads/{uploaded_file.filename}"
    #         uploaded_file.save(file_path)
    #         result = process_file(file_path)
    #         return render_template("index.html", result=result)
    return render_template("index.html")
