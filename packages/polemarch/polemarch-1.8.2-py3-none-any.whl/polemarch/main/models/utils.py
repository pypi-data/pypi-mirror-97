# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from typing import NoReturn, Text, Any, Iterable, Tuple, List, Dict, Union
import os
import re
import time
import signal
import shutil
import logging
import tempfile
import traceback
from pathlib import Path
from collections import namedtuple, OrderedDict
from subprocess import Popen
from functools import reduce
from django.utils import timezone
from vstutils.utils import tmp_file, KVExchanger, raise_context
from vstutils.tools import get_file_value
from .hosts import Inventory
from .tasks import History, Project
from ...main.utils import CmdExecutor, AnsibleArgumentsReference, PMObject


logger = logging.getLogger("polemarch")
InventoryDataType = Tuple[Text, List]
PolemarchInventory = namedtuple("PolemarchInventory", "raw keys")
AnsibleExtra = namedtuple('AnsibleExtraArgs', [
    'args',
    'files',
])


# Classes and methods for support
class DummyHistory:
    # pylint: disable=unused-argument
    def __init__(self, *args, **kwargs):
        self.mode = kwargs.get('mode', None)

    def __setattr__(self, key: Text, value: Any) -> NoReturn:
        if key == 'raw_args':
            logger.info(value)

    def __getattr__(self, item: Text) -> None:
        return None  # nocv

    @property
    def raw_stdout(self) -> Text:
        return ""  # nocv

    @raw_stdout.setter
    def raw_stdout(self, value: Text) -> NoReturn:
        logger.info(value)  # nocv

    def get_hook_data(self, when: Text) -> None:
        return None

    def write_line(self, value: Text, number: int, endl: Text = ''):  # nocv
        # pylint: disable=unused-argument
        logger.info(value)

    def save(self) -> None:
        pass


class Executor(CmdExecutor):
    __slots__ = 'history', 'counter', 'exchanger'

    def __init__(self, history: History):
        super(Executor, self).__init__()
        self.history = history
        self.counter = 0
        self.exchanger = KVExchanger(self.CANCEL_PREFIX + str(self.history.id))
        env_vars = {}
        if self.history.project is not None:
            env_vars = self.history.project.env_vars
        self.env = env_vars

    @property
    def output(self) -> Text:
        # Optimize for better performance.
        return ''

    @output.setter
    def output(self, value) -> NoReturn:
        pass  # nocv

    def working_handler(self, proc: Popen):
        if proc.poll() is None and self.exchanger.get() is not None:  # nocv
            self.write_output("\n[ERROR]: User interrupted execution")
            self.exchanger.delete()
            for _ in range(5):
                try:
                    os.kill(-proc.pid, signal.SIGTERM)
                except Exception:  # nocv
                    break
                proc.send_signal(signal.SIGINT)
                time.sleep(5)
            proc.terminate()
            proc.kill()
            proc.wait()
        super(Executor, self).working_handler(proc)

    def write_output(self, line: Text):
        self.counter += 1
        self.history.write_line(line, self.counter, '\n')

    def execute(self, cmd: Iterable[Text], cwd: Text):
        pm_ansible_path = ' '.join(self.pm_ansible())
        new_cmd = list()
        for one_cmd in cmd:
            if isinstance(one_cmd, str):
                with raise_context():
                    one_cmd = one_cmd.decode('utf-8')
            new_cmd.append(one_cmd)
        self.history.raw_args = " ".join(new_cmd).replace(pm_ansible_path, '').lstrip()
        return super(Executor, self).execute(new_cmd, cwd)


class AnsibleCommand(PMObject):
    ref_types = {
        'ansible-playbook': 'playbook',
        'ansible': 'module',
    }
    command_type = None
    ansible_ref_class = AnsibleArgumentsReference

    status_codes = {
        4: "OFFLINE",
        -9: "INTERRUPTED",
        -15: "INTERRUPTED",
        "other": "ERROR"
    }

    class ExecutorClass(Executor):
        '''
        Default executor class.
        '''

    class Inventory(object):
        hidden_vars = Inventory.HIDDEN_VARS

        def __init__(self, inventory: Union[Inventory, int, Text], cwd: Text = "/tmp", tmpdir: Text = '/tmp'):
            self.cwd = cwd
            self.tmpdir = tmpdir
            self._file = None
            self.is_file = True
            if isinstance(inventory, str):
                self.raw, self.keys = self.get_from_file(inventory)
            else:
                self.raw, self.keys = self.get_from_int(inventory)

        def get_from_int(self, inventory: Union[Inventory, int]) -> InventoryDataType:
            if isinstance(inventory, int):
                inventory = Inventory.objects.get(pk=inventory)  # nocv
            return inventory.get_inventory()

        def get_from_file(self, inventory: Text) -> InventoryDataType:
            _file = "{}/{}".format(self.cwd, inventory)
            try:
                new_filename = os.path.join(self.tmpdir, 'inventory')
                shutil.copyfile(_file, new_filename)
                if not os.path.exists(new_filename):
                    raise IOError  # nocv
                self._file = new_filename
                return get_file_value(new_filename, ''), []
            except IOError:
                self._file = inventory
                self.is_file = False
                return inventory.replace(',', '\n'), []

        @property
        def file(self) -> Union[tmp_file, Text]:
            self._file = self._file or tmp_file(self.raw, dir=self.tmpdir)
            return self._file

        @property
        def file_name(self) -> Text:
            # pylint: disable=no-member
            if isinstance(self.file, str):
                return self.file
            return self.file.name

        def close(self) -> NoReturn:
            # pylint: disable=no-member
            map(lambda key_file: key_file.close(), self.keys) if self.keys else None
            if not isinstance(self.file, str):
                self._file.close()

    def __init__(self, *args, **kwargs):
        self.args = args
        if 'verbose' in kwargs:
            kwargs['verbose'] = int(float(kwargs.get('verbose', 0)))
        self.kwargs = kwargs
        self.__will_raise_exception = False
        self.ref_type = self.ref_types[self.command_type]
        self.ansible_ref = self.ansible_ref_class().raw_dict[self.ref_type]
        self.verbose = kwargs.get('verbose', 0)
        self.cwd = tempfile.mkdtemp()
        self._verbose_output('Execution tmpdir created - [{}].'.format(self.cwd), 0)
        self.env = dict()

    def _verbose_output(self, value: Text, level: int = 3) -> NoReturn:
        if self.verbose >= level:
            if hasattr(self, 'executor'):
                self.executor.write_output(value)
            logger.debug(value)

    def _get_tmp_name(self) -> Text:
        return os.path.join(self.cwd, 'project_sources')

    def _send_hook(self, when: Text, **kwargs) -> NoReturn:
        msg = OrderedDict()
        msg['execution_type'] = self.history.kind
        msg['when'] = when
        inventory = self.history.inventory
        if isinstance(inventory, Inventory):
            inventory = inventory.get_hook_data(when)
        msg['target'] = OrderedDict()
        msg['target']['name'] = self.history.mode
        msg['target']['inventory'] = inventory
        msg['target']['project'] = self.project.get_hook_data(when)
        msg['history'] = self.history.get_hook_data(when)
        msg['extra'] = kwargs
        self.project.hook(when, msg)

    def __generate_arg_file(self, value: Text) -> Tuple[Text, List[tmp_file]]:
        file = tmp_file(value, dir=self.cwd)
        return file.name, [file]

    def __parse_key(self, key: Text, value: Text) -> Tuple[Text, List]:
        # pylint: disable=unused-argument,
        if re.match(r"[-]+BEGIN .+ KEY[-]+", value):
            # Add new line if not exists and generate tmpfile for private key value
            value = value + '\n' if value[-1] != '\n' else value
            return self.__generate_arg_file(value)
        # Return path in project if it's path
        path = (Path(self.workdir)/Path(value).expanduser()).resolve()
        return str(path), []

    def __convert_arg(self, ansible_extra: AnsibleExtra, item: Tuple[Text, Any]) -> Tuple[List, List]:
        extra_args, files = ansible_extra
        key, value = item
        key = key.replace('_', '-')
        if key == 'verbose':
            extra_args += ['-' + ('v' * value)] if value else []
            return extra_args, files
        result = [value, list()]
        if key in ["key-file", "private-key"]:
            result = self.__parse_key(key, value)
        elif key in ["vault-password-file", "new-vault-password-file"]:
            result = self.__generate_arg_file(value)  # nocv
        value = result[0]
        files += result[1]

        key_type = self.ansible_ref[key].get('type', None)
        if (key_type is None and value) or key_type:
            extra_args.append("--{}".format(key))
        extra_args += [str(value)] if key_type else []
        return extra_args, files

    def __parse_extra_args(self, **extra) -> AnsibleExtra:
        handler_func = self.__convert_arg
        return AnsibleExtra(*reduce(
            handler_func, extra.items(), ([], [])
        ))

    @property
    def workdir(self) -> Text:
        return self.get_workdir()

    @property
    def path_to_ansible(self) -> List[Text]:
        return self.pm_ansible(self.command_type)

    def get_hidden_vars(self) -> List[Text]:
        return self.inventory_object.hidden_vars

    def get_inventory_arg(self, target: Text, extra_args: List[Text]) -> List[Text]:
        # pylint: disable=unused-argument
        args = [target]
        if self.inventory_object is not None:
            args += ['-i', self.inventory_object.file_name]
        return args

    def get_args(self, target: Text, extra_args: List[Text]) -> List[Text]:
        return (
            self.path_to_ansible +
            self.get_inventory_arg(target, extra_args) +
            extra_args
        )

    def get_workdir(self) -> Text:
        return self._get_tmp_name()

    def get_kwargs(self, target, extra_args) -> Dict[Text, Any]:
        # pylint: disable=unused-argument
        return dict(cwd=self._get_tmp_name())

    def hide_passwords(self, raw: Text) -> Text:
        regex = r'|'.join((
            r"(?<=" + hide + r":\s).{1,}?(?=[\n\t\s])"
            for hide in self.get_hidden_vars()
        ))
        subst = "[~~ENCRYPTED~~]"
        raw = re.sub(regex, subst, raw, 0, re.MULTILINE)
        return raw

    def get_execution_revision(self, project: Project):  # nocv
        return project.revision

    def prepare(self, target: Text, inventory: Any, history: History, project: Project) -> NoReturn:
        self.target, self.project = target, project
        self.history = history if history else DummyHistory()
        self.history.status = "RUN"
        self.project.sync_on_execution_handler()
        if inventory:
            self.inventory_object = self.Inventory(inventory, cwd=self.project.path, tmpdir=self.cwd)
            self.history.raw_inventory = self.hide_passwords(
                self.inventory_object.raw
            )
        else:  # nocv
            self.inventory_object = None
        self.history.revision = self.get_execution_revision(project)
        self.history.save()
        self.executor = self.ExecutorClass(self.history)

        prepare_func = getattr(
            self,
            'dir_prepare_{}'.format(project.type.lower()),
            self.dir_prepare_copy
        )
        work_dir = self._get_tmp_name()
        self._verbose_output('Copy project to tmp directory.', 2)
        prepare_func(self.project.path, work_dir, self.history.revision)
        self._verbose_output('Project copied to {}.'.format(work_dir), 2)
        project_cfg = os.path.join(work_dir, 'ansible.cfg')
        if os.path.exists(project_cfg) and os.path.isfile(project_cfg):
            self.executor.env['ANSIBLE_CONFIG'] = os.environ.get(
                'ANSIBLE_CONFIG', project_cfg
            )

    def dir_prepare_git(self, src: Text, work_dir: Text, revision: Text):
        # pylint: disable=no-member
        import git
        repo = git.Repo.clone_from(
            url=src + "/.git",
            to_path=work_dir,
            **self.project.repo_handlers.opts(self.project.type).get('PREP_KWARGS', {})
        )
        repo.git.checkout(revision or self.project.branch)
        for sm in repo.submodules:
            # Calling git directly for own submodules
            # since using relative path is not working in gitpython
            # see https://github.com/gitpython-developers/GitPython/issues/730
            with raise_context():
                if sm.url[0:3] == '../':
                    repo_parent_url, _ = os.path.split(repo.remotes.origin.url)
                    actual_url = os.path.join(repo_parent_url, sm.name)
                    with sm.config_writer() as writer:
                        writer.set('url', actual_url)
                sm.update(init=True)

    def dir_prepare_copy(self, src: Text, work_dir: Text, revision: Text):
        # pylint: disable=unused-argument
        if os.path.exists(src):
            shutil.copytree(src=src, dst=work_dir)
        else:  # nocv
            raise Exception('Project dir {} is not exist.'.format(src))

    def error_handler(self, exception: BaseException) -> NoReturn:
        # pylint: disable=no-else-return
        default_code = self.status_codes["other"]
        error_text = str(exception)
        self.history.status = default_code

        if isinstance(exception, self.ExecutorClass.CalledProcessError):  # nocv
            error_text = "{}".format(exception.output)
            self.history.status = self.status_codes.get(
                exception.returncode, default_code
            )
        elif isinstance(exception, self.project.SyncError):
            self.__will_raise_exception = True

        last_line_object = self.history.raw_history_line.last()
        last_line = 0
        if last_line_object:
            last_line = last_line_object.line_number  # nocv
        for line in error_text.split('\n'):
            last_line += 1
            self.history.write_line(line, last_line)

    def execute(self, target: Text, inventory: Any, history: History, project: Project, **extra_args) -> NoReturn:
        try:
            self.prepare(target, inventory, history, project)
            self.history.status = "OK"
            extra = self.__parse_extra_args(**extra_args)
            args = self.get_args(self.target, extra.args)
            kwargs = self.get_kwargs(self.target, extra.args)
            self._send_hook('on_execution', args=args, kwargs=kwargs)
            self.executor.execute(args, **kwargs)
        except Exception as exception:
            logger.error(traceback.format_exc())
            self.error_handler(exception)
            if self.__will_raise_exception:
                raise
        finally:
            inventory_object = getattr(self, "inventory_object", None)
            if inventory_object is not None:
                inventory_object.close()
            self.history.stop_time = timezone.now()
            self.history.save()
            self._send_hook('after_execution')
            self.__del__()

    def run(self):
        try:
            return self.execute(*self.args, **self.kwargs)
        except Exception:  # nocv
            logger.error(traceback.format_exc())
            raise

    def __del__(self):
        if hasattr(self, 'cwd') and os.path.exists(self.cwd):
            self._verbose_output('Tmpdir "{}" was cleared.'.format(self.cwd))
            shutil.rmtree(self.cwd, ignore_errors=True)


class AnsiblePlaybook(AnsibleCommand):
    command_type = "ansible-playbook"


class AnsibleModule(AnsibleCommand):
    command_type = "ansible"

    def __init__(self, target: Text, *pargs, **kwargs):
        kwargs['module-name'] = target
        if not kwargs.get('args', None):
            kwargs.pop('args', None)
        super(AnsibleModule, self).__init__(*pargs, **kwargs)
        self.ansible_ref['module-name'] = {'type': 'string'}

    def execute(self, group: Text = 'all', *args, **extra_args):
        return super(AnsibleModule, self).execute(group, *args, **extra_args)
