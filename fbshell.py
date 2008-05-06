import os
import sys
import fogbugz
import cmd

from getch import getch

CONFIG_FILE = 'shell.ini'

class Shell(cmd.Cmd):
    _ixbug = None
    _sfilter = None
    
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'FB > '
        run_config = False
        try:
            config = {}
            f = open(CONFIG_FILE, 'r')
            for sLine in f.readlines():
                opt, val = map(lambda s: s.strip(), sLine.split('='))
                config[opt] = val
            f.close()
            self._fb = fogbugz.FogBugz(config['url'])
            self._fb._token = config['token']
        except IOError:
            run_config = True
        except KeyError:
            run_config = True

        if run_config:            
            f = open(CONFIG_FILE, 'w')
            sys.stdout.write('FogBugz URL: ')
            url = sys.stdin.readline().strip()
            f.write('url = %s\n' % url)
            sys.stdout.write('Email: ')
            email = sys.stdin.readline().strip()
            sys.stdout.write('Password: ')
            password = ""
            while True:
                ch = getch()
                if ch == '\n' or ch == '\r':
                    break
                print ch
                password += ch
            self._fb = fogbugz.FogBugz(url)
            self._fb.logon(email, password)
            f.write('token = %s\n' % self._fb._token)
            f.close()

    def list_cases(self, **kwargs):
        r = self._fb.search(**kwargs)
        if r.description is not None:
            print 'Filter:', r.description.string
            print
        for case in r.findAll('case'):
            print case['ixbug'].rjust(8), case.stitle.string
            print "    ", case.events.event.evtdescription.string
            print

    def do_list(self, line):
        """list
        Lists cases in the current filter."""
        self.list_cases(cols='sTitle,latestEvent')

    def do_search(self, line):
        """search [query]
        Lists cases returned by the search."""
        self.list_cases(q=line, cols='sTitle,latestEvent')

    def get_case(self, ixbug):
        r = self._fb.search(q=ixbug, cols='sTitle,sProject,sArea,sFixFor,sPersonAssignedTo,events')
        return r.cases.case

    def print_case_info(self, case):
        print '-' * 70
        print "Case %s: %s" % (case['ixbug'], case.stitle.string)
        print "Project: %s | Area: %s" % (case.sproject.string, case.sarea.string)
        print "Fix for: %s" % (case.sfixfor.string,)
        print "Assigned to: %s" % (case.spersonassignedto.string,)
        print '-' * 70

    def print_events(self, events):
        for event in events:
            print event.dt.string.strip()
            print event.evtdescription.string.strip()
            if event.schanges and event.schanges.string:
                print event.schanges.string.strip()
            if event.s and event.s.string:
                print
                print event.s.string.strip()
            print '-' * 40

    def do_view(self, line):
        """view [ixBug]
        Shows all of the events in the case history. If no case is specified, the current case is used.
        If one is specified, the current case is set to the new case."""
        ixbug = line.split()[0]
        if self._ixbug:
            case = self.get_case(self._ixbug)
            self.print_case_info(case)
            self.print_events(case.events.findAll('event'))
        else:
            print "No current case. Specify a case number."

    def do_filter(self, line):
        if len(line) == 0:
            

    def do_filters(self, line):
        r = self._fb.listFilters()
        for filter in r.findAll('filter'):
            if filter.get('status', '') == 'current':
                print "* %s" % filter.string
            else:
                print "  %s" % filter.string

    def do_exit(self, line):
        """exit
        Exit the shell."""
        return True

def main():
    shell = Shell()
    shell.cmdloop()

if __name__ == "__main__":
    main()