import json, os, shutil, tempfile
from io import BytesIO
from docker import Client

class GenericSandbox(object):
    def __init__(self, sandbox_dir='/sandbox', client_args={}):
        self.client = Client(**client_args)
        self.dockerdir = tempfile.mkdtemp('codebox_docker')
        self.sandbox_dir = sandbox_dir
        self.image_tag = 'codebox/generic'
        self.built = False
        self.containers = []

        self.dockerfile = [
            'FROM ubuntu',
            'RUN apt-get update -y',
            'RUN apt-get install -y unzip',
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
        rowbuf = ""
        for row in buildresult:
            if type(row) == bytes:
                row = str(row, 'utf-8')
            if type(row) != str:
                raise TypeError("Non-string result row!", row)
            print(row.strip())
            rowbuf += row.strip() + "\n"
            row = json.loads(row)
            if row.get('error'):
                raise Exception('Image building error %s \n\n %s' % (row, rowbuf))
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

    def run_cmd(self, command, cleanup=True):
        assert self.built
        container = self.client.create_container(image=self.image_tag,
                                                 command=command,
                                                 mem_limit="100m",
                                                 network_disabled=True)
        cid = container['Id']
        self.client.start(container=cid)
        exitcode = self.client.wait(container=cid)
        print("Exit code: %s" % exitcode)
        logs = self.client.logs(container=cid)
        self.containers.append(cid)
        if cleanup:
            self.cleanup_container(cid)
        return {'logs': logs,
                'container_id': cid,
                }

    def cleanup_container(self, container_id):
        self.containers.remove(container_id)
        self.client.remove_container(container=container_id)

    def get_file(self, container_id, fname):
        fpath = os.path.join('/sandbox', fname)
        data = self.client.copy(container=container_id, 
                                resource=fpath).read()
        data = data[512:]           # XXX: WTF, Docker?
        data = data.rstrip(b'\x00') # XXX: WTF, Docker?
        return data


    def destroy(self):
        for container in self.containers:
            self.cleanup_container(container)
        shutil.rmtree(self.dockerdir)
