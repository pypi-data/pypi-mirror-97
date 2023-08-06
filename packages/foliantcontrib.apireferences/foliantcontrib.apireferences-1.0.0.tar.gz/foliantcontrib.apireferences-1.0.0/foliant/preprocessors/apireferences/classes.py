'''Helper classes for APIReferences preprocessor'''

import yaml
import ssl
import sys
import re

from bisect import bisect_left, insort
from inspect import getmembers, isclass, getfullargspec
from io import BytesIO
from pathlib import PosixPath
from logging import getLogger
from lxml import etree
from urllib.request import urlopen

from foliant.preprocessors.utils.header_anchors import to_id
from foliant.preprocessors.utils.combined_options import Options
from .tools import urlopen_with_auth, normalize_content, ensure_root

logger = getLogger('flt.apireferences.classes')

HTTP_VERBS = ('OPTIONS', 'GET', 'HEAD', 'POST',
              'PUT', 'DELETE', 'TRACE', 'CONNECT',
              'PATCH', 'LINK', 'UNLINK')
DEFAULT_TAG_LIST = ['h1', 'h2', 'h3', 'h4']


class WrongModeError(Exception):
    '''Exception which raises when user requested wrong API mode'''
    pass


class BadConfigError(Exception):
    '''Exception which raises when API configuration is incorrect'''
    pass


class ReferenceNotFoundError(Exception):
    '''Exception which raises when reference is not found in API'''
    pass


class Reference:
    '''
    Class representing a reference. It is a reference attribute collection
    with values defaulting to ''

    If you want to modify this class, note that it SHOULD NOT introduce
    attributes that are not reference properties because it is widely used with
    the __dict__ method.
    '''

    def __init__(self, **kwargs):
        self.__dict__ = {
            'source': '',  # should be set explicitly
            'prefix': '',
            'verb': '',
            'command': '',  # always root
            'endpoint_prefix': ''  # always root; note: endpoint_prefix is only set by API object
        }
        self._init_from_dict(kwargs)

    def __repr__(self):
        attrs = ', '.join(f'{k}={v}' for k, v in self.__dict__.items())
        return f'{self.__class__.__name__}({attrs})'

    def init_from_match(self, match):
        '''
        Init values for all reference attributes from a match object.
        Method sets attributes with __setattr__ which triggers attribute checks.

        :param match: match object with init values.
        '''
        match_dict = match.groupdict()
        match_dict['source'] = match.group(0)
        self._init_from_dict(match_dict)

    def _init_from_dict(self, dict_: dict):
        '''
        Init values for all reference attributes from a dictionary.
        Method sets attributes with __setattr__ which triggers attribute checks.

        :param dict_: dict with init values.
        '''
        for k, v in dict_.items():
            self.__setattr__(k, v)

    def __setattr__(self, name, value):
        '''
        If name of the attr is command or endpoint_prefix — ensure that
        they are root.

        If command contains endpoint prefix — strip it out.
        '''
        if name in ('command', 'endpoint_prefix'):
            super().__setattr__(name, ensure_root(value))
            self._fix_command()
        else:
            super().__setattr__(name, value)

    def _fix_command(self):
        '''If command contains endpoint prefix — strip it out'''

        if not (self.command and self.endpoint_prefix):
            return
        if self.command.startswith(self.endpoint_prefix):
            self.__dict__['command'] = ensure_root(
                self.command[len(self.endpoint_prefix):]
            )
        logger.debug(
            f'Parsed reference after fixing command:\n{self}'
        )

    @property
    def command_with_prefix(self):
        """
        Return command with endpoint prefix.
        """
        return self.endpoint_prefix.rstrip('/') + self.command

    @property
    def rel_command(self):
        """
        Return command without leading slash.
        """
        return self.command.lstrip('/')


class APIBase:
    """
    API base class.

    Important: all __init__ parameters in this class and descendants
    must be named exactly as their counterparts in preprocessor options API section,
    except `name` which is passed explicitly.
    """

    mode = ''

    def __init__(self,
                 name: str,
                 url: str):
        self.name = name
        self.url = url

    def __repr__(self):
        attrs = ', '.join(f'{k}={v}' for k, v in self.__dict__.items())
        return f'{self.__class__.__name__}({attrs})'

    def gen_full_url(self, anchor) -> str:
        '''
        Generate a full url to a method on the API documentation website.

        :param anchor: anchor to the method description.

        :returns: full url to the method description on API website.
        '''
        return f'{self.url}#{anchor}'

    def get_link_by_reference(self, ref: Reference) -> str:
        """
        Generate link to API method for specified reference. Should raise
        ReferenceNotFoundError if reference cannot be found in API.

        :param ref: Reference object which should be found.

        :returns: full link to the referenced method.
        """
        raise NotImplementedError()


class APIByTagContent(APIBase):
    """
    API class which generates links based on tag content. It parses the url and
    collects ids and text contents from specified tag list.
    """

    mode = 'find_by_tag_content'

    def __init__(self,
                 name: str,
                 url: str,
                 content_template: str,
                 endpoint_prefix: str = '',
                 tags: list = DEFAULT_TAG_LIST,
                 login: str or None = None,
                 password: str or None = None):
        super().__init__(name, url)
        self.content_template = content_template
        self.tags = tags
        self.registry = {}
        self.endpoint_prefix = endpoint_prefix
        self.login = login
        self.password = password

        self.command_in_content = 'command' in self.content_template
        self.generate_registry()

    def generate_registry(self):
        """
        Parse self.url and collect all tags from self.tags list which have ids
        into self.registry.

        Registry has format {<tag content>: <id>}
        """

        logger.debug(f'Generating registry for {self}')
        context = ssl._create_unverified_context()
        if self.login and self.password:
            page = urlopen_with_auth(self.url, self.login, self.password, context)
        else:
            page = urlopen(self.url, context=context).read()  # may throw HTTPError, URLError
        self.registry = {}
        for _, elem in etree.iterparse(BytesIO(page), html=True):
            if elem.tag in self.tags:
                anchor = elem.attrib.get('id', None)
                if anchor:
                    content = normalize_content(elem.text)
                    self.registry[content] = normalize_content(anchor)

    def get_link_by_reference(self, ref: Reference) -> str:
        """
        Generate link to API method for specified reference. Raises
        ReferenceNotFoundError if reference cannot be found in API.

        :param ref: Reference object which should be found.

        :returns: full link to the referenced method.
        """

        self.check_reference(ref)
        anchor = self.get_anchor_by_reference(ref)  # may throw ReferenceNotFoundError
        return self.gen_full_url(anchor)

    def check_reference(self, ref: Reference):
        """
        Check if reference has all groups which are defined in self.content_template.
        If some group is missing — raise ReferenceNotFoundError.
        """

        missing = []
        for match in re.finditer(r'\{(\S+?)\}', self.content_template):
            elem = match.group(1)
            if elem not in ref.__dict__:
                missing.append(elem)

        if missing:
            raise ReferenceNotFoundError(f'Reference {ref} doesn\'t contain required groups: {missing}')

    def get_anchor_by_reference(self, ref: Reference) -> str:
        """
        Get anchor for the reference from the registry. The key to search in the
        registry is formed by self.content_template.  First try with `command` from
        the reference, then (if that fails) try removing leading slash from command,
        then (if that fails) try adding self.endpoint_prefix if present.

        If reference cannot be found — raise ReferenceNotFoundError.

        :param ref: Reference object to be found.

        :returns: anchor to the referenced method.
        """

        content = self.generate_content_by_reference(ref, False)
        result = self.registry.get(content)
        if result:
            logger.debug(f'Found anchor: {result}')
            return result
        elif self.command_in_content:  # try relative command
            content = self.generate_content_by_reference(ref, False, True)
            result = self.registry.get(content)
            if result:
                logger.debug(f'Found anchor: {result}')
                return result
            elif self.endpoint_prefix:  # try with ep
                content = self.generate_content_by_reference(ref, True)
                result = self.registry.get(content)
                if result:
                    logger.debug(f'Found anchor: {result}')
                    return result

        logger.debug('Not found')
        raise ReferenceNotFoundError(f'Reference {ref.source} not found in API {self.name}')

    def generate_content_by_reference(self,
                                      ref: Reference,
                                      with_ep: bool = False,
                                      rel_command: bool = False) -> str:
        '''
        Generate tag content to search in the registry by self.content_template.

        :param ref: Reference object to generate content.
        :param with_ep: bool whether to add endpoint prefix to command.
        :param rel_command: bool whether to remove leading slash from command.

        :returns: generated tag content.

        '''
        logger.debug(
            'Generating content for reference {ref}'
            ' with endpoint_prefix' if with_ep else ''
            ' with relative command' if rel_command else ''
        )
        api_ref = Reference(**ref.__dict__)  # copy of original ref
        if self.endpoint_prefix:
            api_ref.endpoint_prefix = self.endpoint_prefix

        ref_dict = api_ref.__dict__
        if rel_command:
            ref_dict['command'] = api_ref.rel_command
        if with_ep and self.endpoint_prefix:
            ref_dict['command'] = api_ref.command_with_prefix

        return self.content_template.format(**ref_dict)


class APIByAnchor(APIBase):
    """
    API class which generates links based on tag id. It parses the url and
    collects ids from specified tag list.
    """

    mode = 'find_by_anchor'

    def __init__(self,
                 name: str,
                 url: str,
                 anchor_template: str,
                 anchor_converter: str = 'pandoc',
                 endpoint_prefix: str = '',
                 tags: list = DEFAULT_TAG_LIST,
                 login: str or None = None,
                 password: str or None = None):
        super().__init__(name, url)
        self.anchor_template = anchor_template
        self.anchor_converter = anchor_converter
        self.tags = tags
        self.registry = {}
        self.endpoint_prefix = endpoint_prefix
        self.login = login
        self.password = password

        self.command_in_anchor = 'command' in self.anchor_template
        self.generate_registry()

    def generate_registry(self):
        """
        Parse self.url and collect all tags from self.tags list which have ids.

        Registry has format [id1, id2, ...] (the list is sorted).
        """

        logger.debug(f'Generating registry for {self}')
        context = ssl._create_unverified_context()
        if self.login and self.password:
            page = urlopen_with_auth(self.url, self.login, self.password, context)
        else:
            page = urlopen(self.url, context=context).read()  # may throw HTTPError, URLError
        self.registry = []
        for _, elem in etree.iterparse(BytesIO(page), html=True):
            if elem.tag in self.tags:
                anchor = elem.attrib.get('id', None)
                if anchor:
                    insort(self.registry, normalize_content(anchor))

    def get_link_by_reference(self, ref: Reference) -> str:
        """
        Generate link to API method for specified reference. Raises
        ReferenceNotFoundError if reference cannot be found in API.

        :param ref: Reference object which should be found.

        :returns: full link to the referenced method.
        """

        self.check_reference(ref)
        anchor = self.get_anchor_by_reference(ref)  # may throw ReferenceNotFoundError
        return self.gen_full_url(anchor)

    def check_reference(self, ref: Reference):
        """
        Check if reference has all groups which are defined in self.anchor_template.
        If some group is missing — raise ReferenceNotFoundError.
        """

        missing = []
        for match in re.finditer(r'\{(\S+?)\}', self.anchor_template):
            elem = match.group(1)
            if elem not in ref.__dict__:
                missing.append(elem)

        if missing:
            raise ReferenceNotFoundError(f'Reference {ref} doesn\'t contain required groups: {missing}')

    def get_anchor_by_reference(self, ref: Reference) -> str:
        """
        Get anchor for the reference from self.registry. The search is performed by
        anchor formatted by self.anchor_template. First try with `command from the
        reference, then (if that fails), try removing leading slash from command,
        then (if that fails), tryadding self.endpoint_prefix if present.

        If reference cannot be found — raise ReferenceNotFoundError.

        :param ref: Reference object to be found.

        :returns: found version of anchor.
        """

        anchor = self.generate_anchor_by_reference(ref, False)
        if self.is_in_registry(anchor):
            logger.debug(f'Found anchor "{anchor}"')
            return anchor
        elif self.command_in_anchor:
            anchor = self.generate_anchor_by_reference(ref, False, True)
            if self.is_in_registry(anchor):
                logger.debug(f'Found anchor "{anchor}"')
                return anchor
            elif self.endpoint_prefix:
                anchor = self.generate_anchor_by_reference(ref, True)
                if self.is_in_registry(anchor):
                    logger.debug(f'Found anchor "{anchor}"')
                    return anchor

        logger.debug('Not found')
        raise ReferenceNotFoundError(f'Reference {ref.source} not found in API {self.name}')

    def is_in_registry(self, elem: str) -> bool:
        """
        Search for elem in the registry, return result of the search.

        :param elem: element to be found in registry.

        :returns: true if `elem` is present in registry, false if not.
        """

        i = bisect_left(self.registry, elem)
        if i != len(self.registry) and self.registry[i] == elem:
            return True
        else:
            return False

    def generate_anchor_by_reference(self,
                                     ref: Reference,
                                     with_ep: bool = False,
                                     rel_command: bool = False) -> str:
        '''
        Generate anchor to search in the registry by self.anchor_template.

        :param ref: Reference object to generate content.
        :param with_ep: bool whether to add endpoint prefix to command.
        :param rel_command: bool whether to remove leading slash from command.

        :returns: generated anchor.

        '''
        logger.debug(
            'Generating anchor for reference {ref}'
            ' with endpoint_prefix' if with_ep else ''
            ' with relative command' if rel_command else ''
        )
        api_ref = Reference(**ref.__dict__)  # copy of original ref
        if self.endpoint_prefix:
            api_ref.endpoint_prefix = self.endpoint_prefix

        ref_dict = api_ref.__dict__
        if rel_command:
            ref_dict['command'] = api_ref.rel_command
        if with_ep and self.endpoint_prefix:
            ref_dict['command'] = api_ref.command_with_prefix

        anchor_source = self.anchor_template.format(**ref_dict)
        return to_id(anchor_source, self.anchor_converter)


class APIGenAnchor(APIBase):
    """
    API class which generates links based on anchor template. No url parsing is
    involved.

    Warning: only use this class when reference prefix is defined, because it
    doesn't perform any checks and always returns a url (if reference is valid).
    """

    mode = 'generate_anchor'

    def __init__(self,
                 name: str,
                 url: str,
                 anchor_template: str,
                 anchor_converter: str = 'pandoc',
                 endpoint_prefix: str = ''):
        super().__init__(name, url)
        self.anchor_template = anchor_template
        self.anchor_converter = anchor_converter
        self.endpoint_prefix = endpoint_prefix

    def get_link_by_reference(self, ref: Reference) -> str:
        """
        Generate link to API method for specified reference.

        :param ref: Reference object which should be converted to link.

        :returns: full link to the referenced method.
        """
        self.check_reference(ref)
        anchor = self.generate_anchor_by_reference(ref)
        return self.gen_full_url(anchor)

    def check_reference(self, ref: Reference):
        """
        Check if reference has all groups which are defined in self.anchor_template.
        If some group is missing — raise RuntimeError.
        """

        missing = []
        for match in re.finditer(r'\{(\S+?)\}', self.anchor_template):
            elem = match.group(1)
            if elem not in ref.__dict__:
                missing.append(elem)

        if missing:
            raise RuntimeError(f'Reference {ref} doesn\'t contain required groups: {missing}')

    def generate_anchor_by_reference(self, ref: Reference) -> str:
        '''
        Generate anchor by self.anchor_template.

        :param ref: Reference object to generate content.

        :returns: generated anchor.

        '''
        api_ref = Reference(**ref.__dict__)  # copy of original ref
        if self.endpoint_prefix:
            api_ref.endpoint_prefix = self.endpoint_prefix

        ref_dict = api_ref.__dict__
        anchor_source = self.anchor_template.format(**ref_dict)
        return to_id(anchor_source, self.anchor_converter)


class APIBySwagger(APIBase):
    """
    API class which generates links based on tag id. It parses the swagger spec
    and collects all method definitions, their tags and operation ids.

    Default resulting anchor contains tag and operation id.
    """

    REGISTRY_KEY_TEMPLATE = '{verb} {command}'
    DEFAULT_ANCHOR_TEMPLATE = '/{tag}/{operation_id}'

    mode = 'find_for_swagger'

    def __init__(
        self,
        name: str,
        url: str,
        spec: str or PosixPath,
        anchor_template: str = DEFAULT_ANCHOR_TEMPLATE,
        anchor_converter: str = 'no_transform',
        endpoint_prefix: str = '',
        login: str or None = None,
        password: str or None = None,
    ):
        super().__init__(name, url)
        self.anchor_template = anchor_template
        self.anchor_converter = anchor_converter
        self.endpoint_prefix = endpoint_prefix
        self.login = login
        self.password = password
        self.spec_path = spec

        self._load_spec(spec)
        self.registry = {}  # {VERB_path: ext_dict}
        self.generate_registry()

    def _load_spec(self, spec_path: str or PosixPath):
        """
        Read data from `spec_path` into self.spec dictionary.

        May throw HTTPError (403, 404, ...) or URLError if spec_path is incorrect or
        unavailable url.

        :param spec_path: path or url to OpenAPI spec.
        """

        if not isinstance(spec_path, (str, PosixPath)):
            raise TypeError('spec_path must be str or PosixPath!')
        elif isinstance(spec_path, str) and spec_path.startswith('http'):
            context = ssl._create_unverified_context()
            if self.login and self.password:
                spec = urlopen_with_auth(spec_path, self.login, self.password, context)
            else:
                spec = urlopen(spec_path, context=context).read()  # may throw HTTPError, URLError
        else:  # supplied path, not a link
            with open(spec_path, encoding='utf8') as f:
                spec = f.read()
        self.spec = yaml.load(spec, yaml.Loader)

    def generate_registry(self):
        """
        Parse self.spec and collect all operations into registry.

        Registry is a dictionary of format {VERB_path: ext_dict} where
        VERB_path is a combination of operation verb and operation path,
        ext_dict is a dictionary with extra info about operation which may be used
        to construct anchor:

        ext_dict = {'tag': <first tag>, 'operationId': operationId}
        """

        logger.debug(f'Generating registry for {self}')
        if 'paths' not in self.spec:
            raise RuntimeError(f'{self.spec_path} is not a valid OpenAPI spec.')
        for path_, path_info in self.spec['paths'].items():
            for verb, method_info in path_info.items():
                if verb.upper() not in HTTP_VERBS:
                    continue
                ref_ext = {}
                ref_ext['tag'] = method_info['tags'][0]
                ref_ext['operation_id'] = method_info['operationId']
                key = self.REGISTRY_KEY_TEMPLATE.format(verb=verb.upper(),
                                                        command=path_)
                self.registry[key] = ref_ext

    def get_link_by_reference(self, ref: Reference) -> str:
        """
        Generate link to API method for specified reference. Raises
        ReferenceNotFoundError if reference cannot be found in API.

        :param ref: Reference object which should be found.

        :returns: full link to the referenced method.
        """

        self.check_reference(ref)
        anchor = self.get_anchor_by_reference(ref)  # may throw ReferenceNotFoundError
        return self.gen_full_url(anchor)

    def check_reference(self, ref: Reference):
        """
        Check if reference has all groups which are defined in self.anchor_template,
        except those in ref_ext. verb and command groups are necessary to find the
        operation in the spec.
        If some group is missing — raise ReferenceNotFoundError.
        """

        required = list(
            map(
                lambda m: m.group(1),
                re.finditer(r'\{(\S+?)\}', self.anchor_template)
            )
        )
        required.extend(('verb', 'command'))
        missing = []

        for elem in required:
            if elem not in ('tag', 'operation_id') and elem not in ref.__dict__:
                missing.append(elem)

        if missing:
            raise ReferenceNotFoundError(f'Reference {ref} doesn\'t contain required groups: {missing}')

    def get_anchor_by_reference(self, ref: Reference) -> str:
        """
        Generate anchor for the reference. First search for the operation in the
        registry and update the reference object. Then format the anchor with
        self.anchor_template.

        If reference cannot be found — raise ReferenceNotFoundError.

        :param ref: Reference object to be found.

        :returns: generated anchor.
        """

        api_ref = self.get_extended_reference(ref)
        anchor_source = self.anchor_template.format(**api_ref.__dict__)
        return to_id(anchor_source, self.anchor_converter)

    def get_extended_reference(self, ref: Reference) -> dict:
        """
        Get ext_dict for the reference from self.registry. The search is performed by
        key formatted by REGISTRY_KEY_TEMPLATE. First try with `command from the
        reference, then (if that fails) try adding self.endpoint_prefix if present.

        Update the ref object with data from ext_dict.

        If reference cannot be found — raise ReferenceNotFoundError.

        :param ref: Reference object to be found.

        :returns: updated Reference object with extra fiedls.
        """
        api_ref = Reference(**ref.__dict__)  # copy of original ref
        if self.endpoint_prefix:
            api_ref.endpoint_prefix = self.endpoint_prefix

        key = self.REGISTRY_KEY_TEMPLATE.format(verb=api_ref.verb, command=api_ref.command)
        logger.debug(f'Looking for reference {ref} by key "{key}"')
        if key in self.registry:
            logger.debug(f'Found')
            for k, v in self.registry[key].items():
                api_ref.__setattr__(k, v)
            return api_ref
        elif self.endpoint_prefix:
            key = self.REGISTRY_KEY_TEMPLATE.format(verb=api_ref.verb, command=api_ref.command_with_prefix)
            logger.debug(f'Not found. Looking for reference with endpoint_prefix by key "{key}"')
            if key in self.registry:
                logger.debug(f'Found')
                for k, v in self.registry[key].items():
                    api_ref.__setattr__(k, v)
                return api_ref

        logger.debug('Not found')
        raise ReferenceNotFoundError(f'Reference {ref.source} not found in API {self.name}')


class APIForRedoc(APIBySwagger):
    """
    API class which generates links based on tag id. It parses the redoc swagger spec
    and collects all method definitions, their tags and operation ids.

    Same as APIBySwagger except the default anchor template is different.

    Default resulting anchor contains tag and operation id.
    """

    DEFAULT_ANCHOR_TEMPLATE = 'operation/{operation_id}'
    mode = 'find_for_redoc'


def get_api(options: Options):
    """
    Find class for mode in options and initialize it with options.

    :options: Options object for API.

    :returns: initialized API object.
    """
    apis = getmembers(sys.modules[__name__], isclass)

    apis = [a[1] for a in apis]
    apis = tuple(
        filter(lambda x: issubclass(x, APIBase),
               apis)
    )
    for api in apis:
        if api.mode == options['mode']:
            init_args = get_args_dict(api, options)
            return api(**init_args)

    modes = ', '.join(a.mode for a in apis)
    raise WrongModeError(f"Wrong mode \"{options['mode']}\", should be one of: {modes}.")


def get_args_dict(class_, options: Options) -> dict:
    """
    Filter from options all keys which are not in class_.__init__ method
    Also check for all required arguments, otherwise raise BadConfigError.

    :param class_: API class to be inspected.
    :param options: Options object.

    :returns: dictionary for initializing the class_.
    """

    argspec = getfullargspec(class_.__init__)
    init_args = argspec.args
    init_args.pop(0)  # self
    result = {k: v for k, v in options.items() if k in init_args}

    positional_args = init_args[:-len(argspec.defaults)]

    missing_args = [a for a in positional_args if a not in options]
    if missing_args:
        raise BadConfigError(
            f'Some required parameters are missing in "{options["name"]}" config: ' +
            ', '.join(missing_args)
        )
    return result


def set_up_logger(logger_):
    '''Set up a global logger for classes in this module'''

    global logger
    logger = logger_
