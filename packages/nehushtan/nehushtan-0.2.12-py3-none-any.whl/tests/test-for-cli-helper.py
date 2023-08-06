import sys

from nehushtan.cli.NehushtanArgumentParser import NehushtanArgumentParser

cli = NehushtanArgumentParser(sys.argv[1:]) \
    .add_option(key='Shovel Name', desc="The name of Shovel", short='s', long='shovel') \
    .add_option(key='Task ID', desc='The Task ID', short='t', long='task') \
    .add_option(key='Extra', desc='Extra Options', prefix='extra') \
    .parse()

print('usage')
print(cli.get_usage_text())
print('parsed')
print(cli.get_parsed_option_dict())
print('raw')
print(cli.get_raw_option_dict())
