from app import create_app

app = create_app()

if __name__ == "__main__":
    # debug=True allows the server to automatically restart when you save a file
    app.run(debug=True)
