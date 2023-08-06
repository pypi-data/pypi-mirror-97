from queue import Queue
from threading import Thread

from ipykernel.kernelbase import Kernel
import re
import subprocess
import tempfile
import os
import os.path as path
import urllib.request


class RealTimeSubprocess(subprocess.Popen):
    """
    A subprocess that allows to read its stdout and stderr in real time
    """

    def __init__(self, cmd, write_to_stdout, write_to_stderr):
        """
        :param cmd: the command to execute
        :param write_to_stdout: a callable that will be called with chunks of data from stdout
        :param write_to_stderr: a callable that will be called with chunks of data from stderr
        """
        self._write_to_stdout = write_to_stdout
        self._write_to_stderr = write_to_stderr

        super().__init__(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)

        self._stdout_queue = Queue()
        self._stdout_thread = Thread(target=RealTimeSubprocess._enqueue_output, args=(self.stdout, self._stdout_queue))
        self._stdout_thread.daemon = True
        self._stdout_thread.start()

        self._stderr_queue = Queue()
        self._stderr_thread = Thread(target=RealTimeSubprocess._enqueue_output, args=(self.stderr, self._stderr_queue))
        self._stderr_thread.daemon = True
        self._stderr_thread.start()

    @staticmethod
    def _enqueue_output(stream, queue):
        """
        Add chunks of data from a stream to a queue until the stream is empty.
        """
        for line in iter(lambda: stream.read(4096), b''):
            queue.put(line)
        stream.close()

    def write_contents(self):
        """
        Write the available content from stdin and stderr where specified when the instance was created
        :return:
        """

        def read_all_from_queue(queue):
            res = b''
            size = queue.qsize()
            while size != 0:
                res += queue.get_nowait()
                size -= 1
            return res

        stdout_contents = read_all_from_queue(self._stdout_queue)
        if stdout_contents:
            self._write_to_stdout(stdout_contents)
        stderr_contents = read_all_from_queue(self._stderr_queue)
        if stderr_contents:
            self._write_to_stderr(stderr_contents)


class NativeKernel(Kernel):
    implementation = 'jupyter_native_kernel'
    implementation_version = '1.0'
    language = 'c'
    language_version = 'C11'
    language_info = {'name': 'c',
                     'mimetype': 'text/plain',
                     'file_extension': '.c'}
    banner = "Native kernel.\n" \
             "Uses gcc or compiler of user's choice, and creates source code files and executables in temporary folder.\n"

    def __init__(self, *args, **kwargs):
        super(NativeKernel, self).__init__(*args, **kwargs)
        self.files = []
        mastertemp = tempfile.mkstemp(suffix='.out')
        os.close(mastertemp[0])
        self.master_path = mastertemp[1]
        filepath = path.join(path.dirname(path.realpath(__file__)), 'resources', 'master.c')
        subprocess.call(['gcc', filepath, '-std=c11', '-rdynamic', '-ldl', '-o', self.master_path])

    def cleanup_files(self):
        """Remove all the temporary files created by the kernel"""
        for file in self.files:
            os.remove(file)
        os.remove(self.master_path)

    def new_temp_file(self, **kwargs):
        """Create a new temp file to be deleted when the kernel shuts down"""
        # We don't want the file to be deleted when closed, but only when the kernel stops
        kwargs['delete'] = False
        kwargs['mode'] = 'w'
        file = tempfile.NamedTemporaryFile(**kwargs)
        self.files.append(file.name)
        return file

    def _write_to_stdout(self, contents):
        self.send_response(self.iopub_socket, 'stream', {'name': 'stdout', 'text': contents})

    def _write_to_stderr(self, contents):
        self.send_response(self.iopub_socket, 'stream', {'name': 'stderr', 'text': contents})

    def create_jupyter_subprocess(self, cmd):
        return RealTimeSubprocess(cmd,
                                  lambda contents: self._write_to_stdout(contents.decode()),
                                  lambda contents: self._write_to_stderr(contents.decode()))

    def compile_with_compiler(self, compiler, source_filename, binary_filename, cflags=None, ldflags=None):
        cflags = ['-std=c11', '-fPIC', '-shared', '-rdynamic'] + cflags
        args = [compiler, source_filename] + cflags + ['-o', binary_filename] + ldflags
        return self.create_jupyter_subprocess(args)

    def _filter_magics(self, code):

        magics = {'compiler': 'gcc',
                  'cflags': [],
                  'ldflags': [],
                  'args': []}

        for line in code.splitlines():
            if line.startswith('//%') and line[3:7] != 'load':
                key, value = line[3:].split(":", 2)
                key = key.strip().lower()

                if key == 'compiler':
                    magics['compiler'] = value.strip()
                elif key in ['ldflags', 'cflags']:
                    for flag in value.split():
                        magics[key] += [flag]
                elif key == 'args':
                    # Split arguments respecting quotes
                    for argument in re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', value):
                        magics['args'] += [argument.strip('"')]

        return magics

    # Generates a new payload for the frontend to display.
    def _magic_load(self, code):
        # Replaces lines below the first %load declaration with retrieved code.
        out_text = []
        did_load = False
        out = None
        for line in code.splitlines():
            if line.startswith('%'):
                key, value = line[1:].split(" ", 2)
                key = key.strip().lower()

                if key == 'load':
                    # If URL, fetch code at URL, and replace everything below.
                    if len(value.split('://')) > 1:
                        protocol, url_path = value.split('://')
                        if protocol in ['http', 'https']:
                            try:
                                # Cite: https://stackoverflow.com/a/7244263
                                response = urllib.request.urlopen(value)
                                data = response.read()       # A `bytes` object.
                                text = data.decode('utf-8')  # A `str`; this step can't be used if data is binary.
                                out_text.append("//" + line) # Current line, commented out.
                                out_text.append(text)        # Loaded code.
                                did_load = True
                            except Exception as e:
                                self._write_to_stderr("{}\n".format(e))
                        else:
                            out_text.append("//" + line) # Current line, commented out.
                            self._write_to_stderr("[Native kernel] Invalid protocol type provided in URL to '%load {}'\n".format(value))
                    # Otherwise, it's a local file.
                    else:
                        # Get list of valid subdirs/files we can work with.
                        valid_prefixes = os.listdir()
                        # Sanitize path (ensure it's curdir or lower).
                        local_path = path.normcase(value) # Normalize path.
                        local_path = local_path.replace('..', '') # Remove jump-ups.
                        local_path = path.normpath(local_path) # Simplify path.
                        # Rewrite the expression in the notebook, if needed.
                        if len(local_path) < len(value):
                            out_text.append("%load " + local_path)
                            did_load = True
                            break
                        # Validate path against prefixes from earlier.
                        is_valid_path = False
                        for prefix in valid_prefixes:
                            if local_path.startswith(prefix):
                                is_valid_path = True
                                break
                        else:
                            self._write_to_stderr("[Native kernel] Invalid path provided in '%load {}'\n".format(value))
                        # Attempt to read in file, if path was valid.
                        if is_valid_path:
                            with open(local_path, 'r') as f:
                                code_text = f.read()
                                out_text.append("//" + line) # Current line, commented out.
                                out_text.append(code_text)
                                did_load = True
                    break
            else:
                # Otherwise, it's a normal code line, and we append it.
                out_text.append(line)
        if did_load:
            out = {
                "source": "set_next_input",
                "text": "\n".join(out_text),  # Restore newlines when concatenating the lines.
                "replace": True
            }
        return out

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        # If the user has a %load, handle that first off.
        payload = self._magic_load(code)
        self._write_to_stderr(payload)
        if payload is not None:
            return {'status': 'ok', 'execution_count': self.execution_count, 'payload': [payload], 'user_expressions': {}}
        # Handle magics for compiler flags.
        magics = self._filter_magics(code)

        with self.new_temp_file(suffix='.c') as source_file:
            source_file.write(code)
            source_file.flush()
            with self.new_temp_file(suffix='.out') as binary_file:
                p = self.compile_with_compiler(magics['compiler'], source_file.name, binary_file.name, magics['cflags'], magics['ldflags'])
                while p.poll() is None:
                    p.write_contents()
                p.write_contents()
                if p.returncode != 0:  # Compilation failed
                    self._write_to_stderr(
                            "[Native kernel] {} exited with code {}, the executable will not be executed".format(
                                    magics['compiler'],
                                    p.returncode))
                    return {'status': 'ok', 'execution_count': self.execution_count, 'payload': [],
                            'user_expressions': {}}

        p = self.create_jupyter_subprocess([self.master_path, binary_file.name] + magics['args'])
        while p.poll() is None:
            p.write_contents()
        p.write_contents()

        if p.returncode != 0:
            self._write_to_stderr("[Native kernel] Executable exited with code {}".format(p.returncode))
        return {'status': 'ok', 'execution_count': self.execution_count, 'payload': [], 'user_expressions': {}}

    def do_shutdown(self, restart):
        """Cleanup the created source code files and executables when shutting down the kernel"""
        self.cleanup_files()
