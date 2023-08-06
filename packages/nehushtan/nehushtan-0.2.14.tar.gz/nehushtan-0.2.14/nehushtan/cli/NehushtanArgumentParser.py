import re


class NehushtanArgumentParser:

    def __init__(self, sys_arg_list: list):
        """

        :param sys_arg_list: Commonly `sys.argv[1:]`
        """
        self._sys_arg_list = sys_arg_list
        self._argument_dict = {}
        self._options_short = {}
        self._options_long = {}
        self._options_prefix = {}
        self._result_dict = {}
        self._usage_dict = {}

    def add_option(self, key: str, desc: str = '', short: str = '', long: str = '', prefix: str = ''):
        """

        :param desc:
        :param key: Any Name
        :param short: a -> `-a`
        :param long: alpha -> `--alpha`
        :param prefix: alef -> `--alef-`
        :return:
        """
        if short == '' and long == '' and prefix == '':
            return self

        usage = {
            'key': key,
            'desc': desc,
        }
        if short != '':
            self._options_short[f'-{short}'] = key
            usage['short'] = f'-{short} [VALUE]'
        if long != '':
            self._options_long[f'--{long}'] = key
            usage['long'] = f'--{long} [VALUE]'
        if prefix != '':
            self._options_prefix[f'--{prefix}-'] = key
            usage['prefix'] = f'--{prefix}-[KEY] [VALUE]'

        self._usage_dict[key] = usage
        return self

    def parse(self):
        current_key = None
        self._argument_dict = {}
        for item in self._sys_arg_list:
            if current_key is None:
                current_key = item
            else:
                self._argument_dict[current_key] = item
                current_key = None

        self._result_dict = {}
        for (key, value) in self._argument_dict.items():
            if self._options_short.get(key) is not None:
                self._result_dict[self._options_short[key]] = value
            elif self._options_long.get(key) is not None:
                self._result_dict[self._options_long[key]] = value
            else:
                for prefix, mapping_key in self._options_prefix.items():
                    matches = re.match(f'^{prefix}([A-Za-z0-9._-]+)$', key)
                    if matches is not None:
                        if self._result_dict.get(mapping_key) is None:
                            self._result_dict[mapping_key] = {}
                        self._result_dict[mapping_key][matches[1]] = value
                        break
        return self

    def get_raw_option_dict(self):
        return self._argument_dict

    def get_parsed_option_dict(self):
        return self._result_dict

    def get_usage_text(self):
        usage_text = ""
        for key, value in self._usage_dict.items():
            options = []
            if len(value.get('short', '')) > 0:
                options.append(value.get('short'))
            if len(value.get('long', '')) > 0:
                options.append(value.get('long'))
            if len(value.get('prefix', '')) > 0:
                options.append(value.get('prefix'))

            usage_text += f"{value['key']}" + "\t\t"
            usage_text += ", ".join(options)
            if len(value.get('desc', '')) > 0:
                usage_text += f"\n{value['desc']}"
            usage_text += "\n"

        return usage_text
