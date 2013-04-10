import md5, os, json
import web, config

urls = (
    '/upload',      'Upload',
)

def GetType(name):
    for ptype in config.VALID_IMAGE_TYPE:
        if name[-len(ptype):].lower() == ptype:
            return ptype
    return 0

def Save(filename, content):
    basepath = os.path.join(config.STATIC_IMAGE_DIR, filename[0:2])
    if not os.path.exists(basepath):
        os.makedirs(basepath, 0777)
    filepath = os.path.join(basepath, filename)
    if not os.path.exists(filepath):
        fout = open(filepath, 'wb')
        fout.write(content)
        fout.close()
    return 1


class Upload:
    def POST(self):
        addr = ''
        x = web.input(picture={})
        if x.picture.file:
            pic_type = GetType(x.picture.filename)
            if pic_type:
                picture = x.picture.file.read()
                name = md5.new(picture).hexdigest() + pic_type
                Save(name, picture)
                addr = config.STATIC_IMAGE_URL + name[0:2] + '/' + name
        return json.dumps({"c":0, "addr":addr})


if __name__ == "__main__":
    app = web.application(urls, globals()) 
    app.run()

