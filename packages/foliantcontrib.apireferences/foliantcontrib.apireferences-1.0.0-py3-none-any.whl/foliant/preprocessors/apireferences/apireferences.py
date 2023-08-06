'''APIReferences preprocessor for Foliant. Replaces API references with links to API
docs'''
import re
from collections import OrderedDict
from urllib import error

from .classes import (get_api, Reference, ReferenceNotFoundError, set_up_logger,
                      HTTP_VERBS, BadConfigError)
from foliant.preprocessors.utils.combined_options import Options
from foliant.preprocessors.utils.preprocessor_ext import (BasePreprocessorExt,
                                                          allow_fail)


DEFAULT_REF_REGEX = r'`((?P<prefix>[\w-]+):\s*)?' +\
                    rf'(?P<verb>{"|".join(HTTP_VERBS)})\s+' +\
                    r'(?P<command>\S+)`'
DEFAULT_IGNORING_PREFIX = 'Ignore'

DEFAULT_REF_DICT = {
    'regex': DEFAULT_REF_REGEX,
    'only_defined_prefixes': False,
    'only_with_prefixes': False,
    'trim_template': '`{verb} {command}`',
    'output_template': '[{verb} {command}]({url})'
}


class GenURLError(Exception):
    '''Exception in the full url generation process'''
    pass


class Preprocessor(BasePreprocessorExt):
    defaults = {
        'reference': [DEFAULT_REF_DICT],
        'prefix_to_ignore': DEFAULT_IGNORING_PREFIX,
        'targets': [],
        'trim_if_targets': [],
        'API': {},
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = self.logger.getChild('apireferences')
        set_up_logger(self.logger)

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')
        self.current_filename = ''

        self.apis = OrderedDict()
        self.default_api = None
        self.set_apis()

        self.counter = 0

    def is_prefix_defined(self, prefix):
        '''Return True if prefix is defined in config under API or prefix-to-ignore'''
        defined_prefixes = [*self.apis.keys(), self.options['prefix_to_ignore'].lower()]

        result = (prefix or '').lower() in defined_prefixes
        if result:
            self.logger.debug(f'Prefix "{prefix}" is defined.')
        else:
            self.logger.debug(f'Prefix "{prefix}" is not defined.')

        return result

    def set_apis(self):
        '''
        Fills self.apis dictionary with API objects representing each API from
        the config.
        '''

        for api in self.options.get('API', {}):
            try:
                api_options = Options(
                    self.options['API'][api],
                    required=['url', 'mode']
                )
                api_options['name'] = api
                api_obj = get_api(api_options)
                self.apis[api.lower()] = api_obj
            except (error.HTTPError, error.URLError) as e:
                self._warning(f'Could not open url {api_options["url"]} for API {api}: {e}. '
                              'Skipping.')
            except BadConfigError as e:
                self._warning(f'API "{api}" is not set up. {e} Skipping.', error=e)
        if not self.apis:
            raise RuntimeError('No APIs are set up')

    def process_links(self, content: str) -> str:
        def _sub(block) -> str:
            '''
            Replaces each occurence of the reference to API method (described
            by regex in 'ref-regex' option) with link to the API documentation
            web-page.

            If can't determine link (mistake in the prefix or method name,
            several methods with this name and no prefix, etc) — shows warning
            and leaves reference unchanged.
            '''

            ref = Reference()
            ref.init_from_match(block)

            self.logger.debug(f'Found ref: {ref}')

            if ref_options['only_with_prefixes'] and not ref.prefix:
                self.logger.debug('`only_with_prefixes` option is on and this reference does not '
                                  'have prefix. Skipping.')
                return ref.source

            if ref_options['only_defined_prefixes'] and not self.is_prefix_defined(ref.prefix):
                self.logger.debug(f'`only_defined_prefixes` option is on and reference prefix {ref.prefix} '
                                  'is not not defined. Skipping.')
                return ref.source

            if (ref.prefix or '').lower() == main_options['prefix_to_ignore'].lower():
                self.logger.debug(f'Prefix {ref.prefix} is ignored. Skipping.')
                return ref.source

            api_url = self.get_api_link_for_reference(ref)
            if not api_url:
                return ref.source
            else:
                api, url = api_url

            ref.endpoint_prefix = api.endpoint_prefix
            self.counter += 1
            return ref_options['output_template'].format(url=url, **ref.__dict__)

        processed = content
        main_options = Options(self.options, self.defaults)
        for ref_dict in main_options['reference']:
            ref_options = Options(ref_dict, defaults=DEFAULT_REF_DICT)
            pattern = re.compile(ref_options['regex'])
            processed = pattern.sub(_sub, processed)

        return processed

    @allow_fail('Failed to process reference. Skipping.')
    def get_api_link_for_reference(self, ref: Reference) -> tuple or None:
        """
        Gets relevant API object from self.apis if prefix is defined, or searches
        all APIs for reference if prefix is not defined. Returns full link to
        method description from found API.

        May raise BadConfigError, GenURLError, ReferenceNotFoundError.

        :param ref: Reference object to be found.

        :returns: tuple (<API object>, <full url>) if reference is found, or
                  None if not.
        """

        if ref.prefix:
            api = self.get_api_by_prefix(ref)
            link = api.get_link_by_reference(ref)
            return api, link
        else:
            return self.find_api_link_for_reference(ref)

    def get_api_by_prefix(self, ref: Reference):
        """
        Get relevant API object from self.apis by prefix.

        May raise BadConfigError if api is present in config but not in self.apis.
        May raise GenURLError if prefix is not defined.

        :param ref: Reference object by which prefix API should be found.

        :returns: found API object.
        """

        if self.is_prefix_defined(ref.prefix):
            api = self.apis[ref.prefix.lower()]
            return api
        else:
            config_prefixes = [*self.options.get('API', {}).keys(), self.options['prefix_to_ignore']]
            set_up_prefixes = [*self.apis.keys(), self.options['prefix_to_ignore'].lower()]
            if ref.prefix in config_prefixes:
                raise BadConfigError(f'API "{ref.prefix}" is not properly configured')
            else:
                raise GenURLError(f'"{ref.prefix}" is a wrong prefix. Should be one of: '
                                  f'{", ".join(set_up_prefixes)}.')

    def find_api_link_for_reference(self, ref: Reference) -> tuple or None:
        """
        Search for reference in all defined APIs whose mode doesn't start with
        'generate' (these APIs should only work for reference with prefixes).

        If reference is not found in any API, returns None.
        If reference is found in multiple APIs raises GetURLError.

        :param ref: Reference object to be found.

        :returns: tuple (<API object>, <full url>) if reference is found, or
                  None if not.

        """
        found = []
        for api in self.apis.values():
            if api.mode.startswith('generate'):
                continue
            try:
                link = api.get_link_by_reference(ref)
                found.append((api, link,))
            except ReferenceNotFoundError:
                continue
        if len(found) == 1:
            return found[0]
        elif len(found) > 1:
            raise GenURLError(f'{ref.source} is present in several APIs'
                              f' ({", ".join(f[0].name for f in found)}). Please, use prefix.')
        else:
            self._warning(f'Cannot find reference {ref.source}.')

    def trim_prefixes(self, content: str) -> str:
        def _sub(block) -> str:
            '''
            Replaces each occurence of the reference to API method (described
            by regex in 'ref-regex' option) with its trimmed version.

            Only those references are replaced which prefixes are defined in
            config + prefix-to-ignore. All the others are left unchanged.
            '''
            ref = Reference()
            ref.init_from_match(block)
            self.logger.debug(f'Found ref {ref}')
            if not self.is_prefix_defined(ref.prefix):
                return ref.source
            result = ref_options['trim_template'].format(**ref.__dict__)
            self.logger.debug(f'Trimming to {result}')
            return result

        processed = content
        main_options = Options(self.options, self.defaults)
        for ref_dict in main_options['reference']:
            ref_options = Options(ref_dict, defaults=DEFAULT_REF_DICT)
            pattern = re.compile(ref_options['regex'])
            processed = pattern.sub(_sub, processed)

        return processed

    def apply(self):
        self.logger.info('Applying preprocessor')
        if not self.options['targets'] or\
                self.context['target'] in self.options['targets']:
            self._process_all_files(self.process_links, 'Converting references')

        if self.context['target'] in self.options['trim_if_targets']:
            self._process_all_files(self.trim_prefixes, 'Trimming prefixes')

        self.logger.info(f'Preprocessor applied. {self.counter} links were added')
