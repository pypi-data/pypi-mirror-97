import argparse
import pinit
import pbuild
import pgen
import pclean




class commandline_parse:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog = 'hasiki')
        self.subparsers = self.parser.add_subparsers(title='Commands', dest='command')

        self.add_command('init', pinit.add_arguments, pinit.run,
                        help_msg='Init the easybuild')

        self.add_command('gen', pgen.add_arguments, pgen.run,
                        help_msg='Generate the ninja build file')

        self.add_command('build', pbuild.add_arguments, pbuild.run,
                        help_msg='Generate the ninja build file')

        self.add_command('clean', pclean.add_arguments, pclean.run,
                        help_msg='Generate the ninja build file')

    def add_command(self, name, add_arguments_func, run_func, help_msg, aliases=None):
        p = self.subparsers.add_parser(name, help=help_msg)
        add_arguments_func(p)
        p.set_defaults(run_func=run_func)

    def run(self):
        parser = self.parser
        options = parser.parse_args()    
        if options.command == None:
            print('please use "-h" to get help info.')
            return
        options.run_func(options)


def main():
    commandline_parse().run()



if __name__ == "__main__":
    main()


