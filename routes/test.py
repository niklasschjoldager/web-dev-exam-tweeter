from bottle import default_app, run


from routes import test

try:
    import production

    app = default_app()
except:
    run(host="127.0.0.1", port=5555, debug=True, reloader=True)
