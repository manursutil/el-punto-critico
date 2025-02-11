from website import create_app, create_admin

app = create_app()

if __name__ == '__main__':
    create_admin()
    app.run(debug=True)