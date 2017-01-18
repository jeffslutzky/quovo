import web

urls = (
  '/', 'index   '
)

app = web.application(urls, globals())

render = web.template.render('/')

class Index(object):
    def GET(self):
        return render.index()

    def POST(self):
        form = web.input

if __name__ == "__main__":
    app.run()
