from flask import Flask,render_template,redirect,url_for,request,abort
def create_app():
    app = Flask(__name__)
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/index')
    def gotoindex():
        return redirect(url_for('index'))


    @app.route('/doc')
    def doc():
        return render_template('doc.html')

    @app.route('/search')
    def search():
        keywords = request.args.get('query',type=str)
        if keywords is not None:

            #icourse and icourse163
            from . import icourses_searcher
            icourse163_List,icourses_List = icourses_searcher.search(keywords)


            #xuetangx
            #from . import xuetangx_searcher_async
            #xuetangx_List = xuetangx_searcher_async.search(keywords)
            # xuetangx
            from . import xuetangx_searcher
            xuetangx_List = xuetangx_searcher.search(keywords)

            return render_template('course_list.html', icourses_List=icourses_List, icourse163_List=icourse163_List,xuetangx_List=xuetangx_List)
        return render_template('search.html')



    @app.route('/get')
    def get():
        #http://www.icourses.cn/web/sword/portal/shareIntroduction?courseId=7331
        #https://www.icourse163.org/course/BIT-268001
        #http://www.xuetangx.com/courses/course-v1:TsinghuaX+30240184+sp/about
        url = request.args.get('url',type=str)
        if url:
            if 'icourses' in url:
                id = url.split('=')[-1]
                return redirect(url_for('resource',website='icourses',id=id,_external=True))
            elif 'icourse163' in url:
                id = url.split('/')[-1]
                return redirect(url_for('resource',website='icourse163',id=id,_external=True))
            elif 'xuetangx' in url:
                id = url.split('/')[-2]
                return redirect(url_for('resource',website='xuetangx',id=id,_external=True))
            else:
                abort(404)
        else:
            abort(404)
        return 'hello'
    @app.route('/resource/<string:website>/<string:id>')
    def resource(website,id):
        if website == 'icourse163':
            from . import icourse163_getter
            getter = icourse163_getter.icourse163_getter(id)
            chapter_list = getter.get_chapters()
            if not chapter_list:
                abort(501)
        elif website == 'icourses':
            from . import icourses_getter
            getter = icourses_getter.icourses_getter(id)
            chapter_list = getter.get_chapter()
            if not chapter_list:
                abort(501)
        elif website == 'xuetangx':
            from . import xuetangx_getter
            chapter_list = xuetangx_getter.get_xuetangx(id)

        return render_template('resource_list.html',chapter_list=chapter_list)
        
    @app.errorhandler(500)
    def internal_error(e):
        return render_template('404.html',error='Ops, an error has occured!')
    
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html',error='Can\'t find the page you are looking for...')

    @app.errorhandler(501)
    def sever_error(e):
        return render_template('404.html', error='Server error')

    return app



