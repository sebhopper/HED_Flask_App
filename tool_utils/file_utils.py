"""Utils for handing the files in the flask app"""

ALLOWED_EXTENSIONS = {'csv', 'txt'}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
