import os
import sys
from abc import ABC, abstractmethod
from pkg_resources import load_entry_point
from urllib.parse import urlparse
import logging
from time import sleep
from .task import task
from .subprocess import run, quote_argv
from .judge import compare_output
from .client import Judge, Testcase

logger = logging.getLogger(__package__)


class AuthError(BaseException):
    pass

class Persistable(ABC):

    @abstractmethod
    def __getstate__(self):
        pass

    @abstractmethod
    def __setstate__(self, state):
        pass


@task("Fetch testcases of {pid} from {oj}")
def testcases(client, oj, pid, writer):
    return client.testcases(pid, writer)

@task("Check against testcase {name}")
def run_test(name, argv, input, output):
    logger.debug("Running `%s`", quote_argv(argv))
    got = run(argv, input=input.read(), capture_output=True, check=True).stdout
    assert compare_output(got, output.read()), "Wrong Answer"


class Profile:

    def __init__(self, get_credential=None, state_store=None, cache_store=None):
        self.agents = {}

        self._get_credential = get_credential
        if get_credential is None:
            if sys.stdin.isatty():
                from .credential import readline_get_credential
                self._get_credential = readline_get_credential
            if os.environ.get('GITHUB_ACTIONS', 'false') == 'true':
                from .credential import environ_get_credential
                self._get_credential = environ_get_credential

        self.state_store = state_store
        if state_store is None:
            from .state.user import UserStateStore
            self.state_store = UserStateStore()
        self.cache_store = cache_store
        if cache_store is None:
            if os.environ.get('GITHUB_ACTIONS', 'false') == 'true':
                from .cache.github import GithubActionCacheStore
                self.cache_store = GithubActionCacheStore()
            else:
                from .cache.user import UserCacheStore
                self.cache_store = UserCacheStore()

        self.debug = False

    def set_debug(self, debug):
        self.debug = debug

    def __repr__(self):
        return "<{} credential={!r} state_store={!r} cache_store={!r}>".format(self.__class__.__name__, self._get_credential, self.state_store, self.cache_store)

    def get_agent(self, name='localhost'):
        if name not in self.agents:
            try:
                klass = load_entry_point(__package__, "online_judge_agents", name)
            except ImportError:
                assert False, f"agent '{name}' not found"
            agent = klass(self, name)
            self.load_state(agent)
            self.agents[name] = agent

        return self.agents[name]

    def get_client(self, oj, type=None):
        return self.get_agent().get_client(oj, type)

    def get_envs(self, oj):
        return self.get_agent().get_client(oj, Judge).envs

    @task("Extract problem ID from URL '{url}'")
    def pid(self, url):
        o = urlparse(url)
        client = self.get_client(o.netloc)
        pid = client.pid(o)
        return o.netloc, pid

    @task("Load testcases of problem {pid} of {oj}")
    def testcases(self, oj, pid):
        client = self.get_client(oj, Testcase)
        key = getattr(client, 'CACHE_KEY', oj)
        reader = self.cache_store.get(key, pid)
        if reader is None:
            writer = self.cache_store.create(key, pid)
            testcases(client, oj, pid, writer)
            reader = self.cache_store.get(key, pid)
        return reader

    def prologue(self, oj, pid):
        client = self.get_client(oj, Judge)
        return client.prologue(pid)

    @task("Test solution of problem {pid} of {oj}")
    def run_tests(self, oj, pid, names, argv):
        reader = self.testcases(oj, pid)
        for name in names or reader:
            input, output = reader[name]
            run_test(name, argv, input, output)

    def raw_submit(self, oj, pid, env, code, agent="localhost"):
        return self.get_agent(agent).submit(oj, pid, env, code)

    @task("Check status of submission {token}")
    def status(self, oj, token, agent="localhost"):
        return self.get_agent(agent).status(oj, token)

    @task("Submit solution to problem {pid} in {env} to {oj} via {agent}")
    def submit(self, oj, pid, env, code, agent="localhost"):
        token = self.raw_submit(oj, pid, env, code, agent)
        status = None
        while True:
            status, message, *extra = self.status(oj, token, agent)
            if status is not None:
                break
            sleep(2)
        assert status, message
        return message, extra[0]

    def load_state(self, client):
        if isinstance(client, Persistable):
            state = self.state_store.load(client.netloc)
            if state is not None:
                client.__setstate__(state)

    @task("Log into {client.netloc}", retry=True)
    def auth(self, client):
        try:
            if client.credential is None:
                if not self._get_credential:
                    raise AuthError("Credential not provided")
                client.credential = self._get_credential(client.netloc, client.__annotations__['CREDENTIAL'])
            client.login()
            if isinstance(client, Persistable):
                self.state_store.store(client.netloc, client.__getstate__())
            return
        except AuthError as e:
            client.credential = None
            assert False, str(e)
