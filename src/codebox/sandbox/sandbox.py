import json, os, shutil, tempfile
from io import BytesIO
from docker import Client

class GenericSandbox(object):
    def __init__(self, sandbox_dir='/sandbox'):
        self.client = Client()
        self.dockerdir = tempfile.mkdtemp('codebox_docker')
        self.sandbox_dir = sandbox_dir
        self.image_tag = 'codebox/generic'
        self.built = False

        self.dockerfile = [
            'FROM ubuntu',
            'RUN apt-get install unzip',
            'RUN mkdir %s' % sandbox_dir,
            'WORKDIR %s' % sandbox_dir,
            ]

    def build(self):
        dockerpath = os.path.join(self.dockerdir, 'Dockerfile')
        dockercontents = '\n'.join(self.dockerfile)
        with open(dockerpath, 'w') as f:
            #print(dockercontents)
            f.write(dockercontents)
        buildresult = self.client.build(path=self.dockerdir,
                                        tag=self.image_tag,
                                        )
        for row in buildresult:
            if type(row) == bytes:
                row = str(row, 'utf-8')
            if type(row) != str:
                raise TypeError("Non-string result row!", row)
            print(row.strip())
            row = json.loads(row)
            if row.get('error'):
                raise Exception('Image building error', row)
        self.built = True

    def include_file(self, fname, source_fname=None, source_contents=None):
        if not (source_fname or source_contents):
            raise ValueError("No source specified!")
        if source_fname:
            sourcecopy_path = os.path.join(self.dockerdir, fname)
            shutil.copyfile(source_fname, sourcecopy_path)
            destination_path = os.path.join(self.sandbox_dir, fname)

            command = "ADD {source} {dest}".format(source=fname,
                                                   dest=destination_path)
            self.dockerfile.append(command)
        else:
            if type(source_contents)==bytes:
                data = source_contents
            elif type(source_contents)==str:
                data = source_contents.encode()
            else:
                raise TypeError('Source contents are not string or bytes.')
            source_path = os.path.join(self.dockerdir, fname)
            destination_path = os.path.join(self.sandbox_dir, fname)
            with open(source_path, 'wb') as f:
                f.write(data)
            command = "ADD {source} {dest}".format(source=fname,
                                                   dest=destination_path)
            self.dockerfile.append(command)

    def include_zip(self, source_fname=None, source_contents=None):
        if not (source_fname or source_contents):
                raise ValueError("No source specified!")
        ZIPNAME = "__codebox_zip_upload.zip"
        self.include_file(ZIPNAME, source_fname, source_contents)

        command = "RUN unzip {name}".format(name=ZIPNAME)
        self.dockerfile.append(command)

        command = "RUN rm {name}".format(name=ZIPNAME)
        self.dockerfile.append(command)

    def run_cmd(self, command):
        assert self.built
        container = self.client.create_container(image=self.image_tag,
                                                 command=command,
                                                 mem_limit="100m",)
        cid = container['Id']
        self.client.start(container=cid)
        exitcode = self.client.wait(container=cid)
        print("Exit code: %s" % exitcode)
        logs = self.client.logs(container=cid)
        self.client.remove_container(container=cid)
        return logs

    def destroy(self):
        shutil.rmtree(self.dockerdir)
