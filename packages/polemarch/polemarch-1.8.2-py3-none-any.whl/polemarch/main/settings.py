from collections import OrderedDict
from vstutils.settings import *

WEBSERVER_COMMAND = 'webserver'

POLEMARCH_VERSION = PROJECT_VERSION
APACHE = False if ("runserver" in sys.argv) else True

# Directory for git projects
PROJECTS_DIR = main.get("projects_dir", fallback="{LIB}/projects")
os.makedirs(PROJECTS_DIR) if not os.path.exists(PROJECTS_DIR) else None

# Polemarch apps
INSTALLED_APPS += [
    '{}.main'.format(VST_PROJECT_LIB_NAME),
    '{}.api'.format(VST_PROJECT_LIB_NAME),
]

# Additional middleware and auth
MIDDLEWARE += [
    'vstutils.middleware.TimezoneHeadersMiddleware',
    '{}.main.middleware.PolemarchHeadersMiddleware'.format(VST_PROJECT_LIB_NAME),
]

AUTH_PASSWORD_VALIDATORS += [
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# API settings
VST_API_VERSION = 'v2'

REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
    "{}.api.{}.permissions.ModelPermission".format(VST_PROJECT_LIB_NAME, VST_API_VERSION),
]

API_URL = VST_API_URL
DEFAULT_API_URL = "/{}/{}".format(API_URL, VST_API_VERSION)
API = {
    VST_API_VERSION: OrderedDict(
        project={'view': '{}.api.v2.views.ProjectViewSet'.format(VST_PROJECT_LIB_NAME)},
        community_template={'view': '{}.api.v2.views.ProjectTemplateViewSet'.format(VST_PROJECT_LIB_NAME)},
        inventory={'view': '{}.api.v2.views.InventoryViewSet'.format(VST_PROJECT_LIB_NAME)},
        group={'view': '{}.api.v2.views.GroupViewSet'.format(VST_PROJECT_LIB_NAME)},
        host={'view': '{}.api.v2.views.HostViewSet'.format(VST_PROJECT_LIB_NAME)},
        history={'view': '{}.api.v2.views.HistoryViewSet'.format(VST_PROJECT_LIB_NAME), "op_types": ['get', 'del', 'mod']},
        _bulk={'view': '{}.api.v2.views.BulkViewSet'.format(VST_PROJECT_LIB_NAME), 'type': 'view'},
        user={'view': '{}.api.v2.views.UserViewSet'.format(VST_PROJECT_LIB_NAME)},
        team={'view': '{}.api.v2.views.TeamViewSet'.format(VST_PROJECT_LIB_NAME)},
        token={'view': '{}.api.v2.views.TokenView'.format(VST_PROJECT_LIB_NAME), 'type': 'view'},
        hook={'view': '{}.api.v2.views.HookViewSet'.format(VST_PROJECT_LIB_NAME)},
        stats={'view': '{}.api.v2.views.StatisticViewSet'.format(VST_PROJECT_LIB_NAME), 'op_types': ['get']})
}

PROJECT_GUI_MENU = [
    {
        'name': 'Projects',
        'url': '/project',
        'span_class': 'fas fa-cubes',
    },
    {
        'name': 'Community',
        'url': '/community_template',
        'span_class': 'fa fa-cloud',
    },
    {
        'name': 'Inventories',
        'url': '/inventory',
        'span_class': 'fa fa-folder',
        'sublinks': [
            {
                'name': 'Groups',
                'url': '/group',
                'span_class': 'fas fa-server',
            },
            {
                'name': 'Hosts',
                'url': '/host',
                'span_class': 'fas fa-hdd',
            },
        ]
    },
    {
        'name': 'History',
        'url': '/history',
        'span_class': 'fa fa-calendar',
    },
    {
        'name': 'System',
        'span_class': 'fa fa-cog',
        'sublinks': [
            {
                'name': 'Users',
                'url': '/user',
                'span_class': 'fa fa-user',
            },
            {
                'name': 'Hooks',
                'url': '/hook',
                'span_class': 'fa fa-plug'
            },
        ]
    },
]

SWAGGER_SETTINGS['DEFAULT_INFO'] = '{}.api.v2.swagger.api_info'.format(VST_PROJECT_LIB_NAME)

OPENAPI_EXTRA_LINKS = dict()
OPENAPI_EXTRA_LINKS['Request'] = [
    {
        'url': (
                'https://gitlab.com/vstconsulting/polemarch/issues/new?'
                'issuable_template%5D=Ask&issue%5Btitle%5D=Ask%20about%20version%20'
                +str(POLEMARCH_VERSION)
        ),
        'name': 'Question'
    },
    {
        'url': (
                'https://gitlab.com/vstconsulting/polemarch/issues/new?'
                'issuable_template%5D=Bug&issue%5Btitle%5D=Bug%20in%20version%20'
                + str(POLEMARCH_VERSION)
        ),
        'name': 'Bug report'
    },
    {
        'url': (
            'https://gitlab.com/vstconsulting/polemarch/issues/new?'
            'issuable_template%5D=Feature%20request&issue%5Btitle%5D='
        ),
        'name': 'Feature request'
    },
]
OPENAPI_EXTRA_LINKS['Documentation'] = {
    'url': 'http://polemarch.readthedocs.io/',
    'name': 'Official documentation'
}
OPENAPI_EXTRA_LINKS['Repository'] = {
    'url': 'https://gitlab.com/vstconsulting/polemarch.git',
    'name': 'Official repository'
}

# Polemarch handlers

# Repos
class GitSection(BaseAppendSection):
    pass


class GitFetchSection(GitSection):
    types_map = {
        'all': cconfig.BoolType(),
        'append': cconfig.BoolType(),
        'multiple': cconfig.BoolType(),
        'unshallow': cconfig.BoolType(),
        'update-shallow': cconfig.BoolType(),
        'force': cconfig.BoolType(),
        'keep': cconfig.BoolType(),
        'prune': cconfig.BoolType(),
        'prune-tags': cconfig.BoolType(),
        'no-tags': cconfig.BoolType(),
        'tags': cconfig.BoolType(),
        'no-recurse-submodules': cconfig.BoolType(),
        'update-head-ok': cconfig.BoolType(),
        'quiet': cconfig.BoolType(),
        'verbose': cconfig.BoolType(),
        'ipv4': cconfig.BoolType(),
        'ipv6': cconfig.BoolType(),
        'depth': cconfig.IntType(),
        'deepen': cconfig.IntType(),
        'jobs': cconfig.IntType(),
    }

    def all(self):
        data = super().all()
        data['force'] = True
        return data


class GitCloneSection(GitSection):
    types_map = {
        'local': cconfig.BoolType(),
        'no-hardlinks': cconfig.BoolType(),
        'shared': cconfig.BoolType(),
        'dissociate': cconfig.BoolType(),
        'quiet': cconfig.BoolType(),
        'verbose': cconfig.BoolType(),
        'single-branch': cconfig.BoolType(),
        'no-single-branch': cconfig.BoolType(),
        'no-tags': cconfig.BoolType(),
        'shallow-submodules': cconfig.BoolType(),
        'no-shallow-submodules': cconfig.BoolType(),
        'depth': cconfig.IntType(),
        'jobs': cconfig.IntType(),
    }


git_fetch = {}
git_clone = {}

if TESTS_RUN:
    config['git'] = dict(fetch=dict(), clone=dict())

if 'git' in config:
    git = config['git']

    if 'fetch' in git:
        git_fetch = GitFetchSection('git.fetch', config, git['fetch']).all()

    if 'clone' in git:
        git_clone = GitCloneSection('git.clone', config, git['clone']).all()


REPO_BACKENDS = {
    "MANUAL": {
        "BACKEND": "{}.main.repo.Manual".format(VST_PROJECT_LIB_NAME),
    },
    "GIT": {
        "BACKEND": "{}.main.repo.Git".format(VST_PROJECT_LIB_NAME),
        "OPTIONS": {
            "CLONE_KWARGS": git_clone,
            "FETCH_KWARGS": git_fetch,
            "GIT_ENV": {
                "GLOBAL": {
                    "GIT_SSL_NO_VERIFY": "true"
                }
            }
        }
    },
    "TAR": {
        "BACKEND": "{}.main.repo.Tar".format(VST_PROJECT_LIB_NAME),
    },
}

# Custom user repos
DEFAULT_COMMUNITY_REPOS_URL = 'https://gitlab.com/vstconsulting/polemarch-community-repos/raw/master/projects.yaml'
COMMUNITY_REPOS_URL = main.get('community_projects_url', fallback=DEFAULT_COMMUNITY_REPOS_URL)

# RPC tasks settings
TASKS_HANDLERS = {
    "REPO": {
        "BACKEND": "{}.main.tasks.tasks.RepoTask".format(VST_PROJECT_LIB_NAME)
    },
    "SCHEDUER": {
        "BACKEND": "{}.main.tasks.tasks.ScheduledTask".format(VST_PROJECT_LIB_NAME)
    },
    "MODULE": {
        "BACKEND": "{}.main.tasks.tasks.ExecuteAnsibleModule".format(VST_PROJECT_LIB_NAME)
    },
    "PLAYBOOK": {
        "BACKEND": "{}.main.tasks.tasks.ExecuteAnsiblePlaybook".format(VST_PROJECT_LIB_NAME)
    },
}

CLONE_RETRY = rpc.getint('clone_retry_count', fallback=5)

# ACL settings
ACL = {
    "MODEL_HANDLERS": {
        "Default": "{}.main.acl.handlers.Default".format(VST_PROJECT_LIB_NAME)
    }
}

# Outgoing hooks settings
HOOKS = {
    "HTTP": {
        "BACKEND": '{}.main.hooks.http.Backend'.format(VST_PROJECT_LIB_NAME)
    },
    "SCRIPT": {
        "BACKEND": '{}.main.hooks.script.Backend'.format(VST_PROJECT_LIB_NAME)
    },
}

HOOKS_DIR = main.get("hooks_dir", fallback="/etc/polemarch/hooks/")

__EXECUTOR_DEFAULT = '{INTERPRETER} -m pm_ansible'
EXECUTOR = main.get("executor_path", fallback=__EXECUTOR_DEFAULT).strip().split(' ')
SELFCARE = '/tmp/'

MANUAL_PROJECT_VARS = config['project_manual_vars'].all() or \
                      dict(forks=4, timeout=30, fact_caching_timeout=3600, poll_interval=5)

PROJECT_REPOSYNC_WAIT_SECONDS = main.getseconds('repo_sync_on_run_timeout', fallback='1:00')
PROJECT_CI_HANDLER_CLASS = "{}.main.ci.DefaultHandler".format(VST_PROJECT_LIB_NAME)


__PWA_ICONS_SIZES = [
    "36x36", "48x48", "72x72", "96x96", "120x120", "128x128", "144x144",
    "150x150", "152x152", "180x180", "192x192", "310x310", "512x512"
]

PWA_MANIFEST = {
    "description": "Ansible based service for IT infrastructure management",
    "icons": list(
        map(lambda icon_size : {
            "src": "{0}img/logo/logo_{1}.png".format(STATIC_URL, icon_size),
            "sizes": icon_size,
            "type": "image/png"
        }, __PWA_ICONS_SIZES)
    ),
}

SPA_STATIC += [
    {'priority': 149, 'type': 'js', 'name': 'polemarch/pmlib.js'},
]

# TEST settings
if "test" in sys.argv:
    REPO_BACKENDS['GIT']['OPTIONS']['CLONE_KWARGS']['local'] = True
    CLONE_RETRY = 0
    PROJECTS_DIR = '/tmp/polemarch_projects' + str(KWARGS['PY_VER'])
    HOOKS_DIR = '/tmp/polemarch_hooks' + str(KWARGS['PY_VER'])
    os.makedirs(PROJECTS_DIR) if not os.path.exists(PROJECTS_DIR) else None
    os.makedirs(HOOKS_DIR) if not os.path.exists(HOOKS_DIR) else None
