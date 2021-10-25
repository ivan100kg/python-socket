def index():
    with open('templates/index.html') as f:
        return f.read()


def blog():
    with open('templates/blog.html') as f:
        return f.read()
