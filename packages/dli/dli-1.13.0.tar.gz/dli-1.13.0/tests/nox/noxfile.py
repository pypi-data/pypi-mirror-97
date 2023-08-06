import nox
import os


def test_existing_requirements(session):
    session.install('-r', '../../requirements.txt')
    session.install('-r', '../../requirements-test.txt')
    os.chdir('../../')
    session.run('pytest', '-m', 'not integration', '--verbose')


def test_requirements_sc0(session):
    """
        Smoke test - single unittest, no integration tests.
        Integration tests are run in test_requirements_offset_scenarios.
    """
    TEST_FILES = ['./tests/models/test_structured_dataset.py']
    session.install('-r', '../../requirements.txt')
    session.install('-r', '../../requirements-test.txt')
    os.chdir('../../')
    session.run('pytest', '-m', "'not integration'", '--verbose', *TEST_FILES)


def test_requirements_offset_scenarios(session):
    """
        Run all unit tests and integration tests
        using modified requirements.txt, where for each
        package>=version_number, version_number is found given its
        proximity to MIN_DATE environment variable.
    """
    scenario = os.environ.get('NOX_SCENARIO')
    min_date = os.environ.get('MIN_DATE')
    install_betas: bool = os.environ.get('INSTALL_BETAS', None) == 'True'

    if scenario == '1':
        print('Not using a min_date')
        min_date = None
    from_file = '../../requirements.txt'
    to_file = f'requirements-{scenario}.txt'

    rm = RequirementsModifier(from_file)
    rm.modify_requirements(from_file, to_file, min_date)
    if install_betas:
        print('Install beta versions of dependencies')
        session.install('-r', f'requirements-{scenario}.txt', '--pre')
        session.install('-r', '../../requirements-test.txt', '--pre')
    else:
        print('Install release versions of dependencies')
        # TODO scott: a bit of tech debt - we didn't need to write to a file,
        #  doing a session.install you can install a dependency just like
        #  you would with pip. So instead of adding a line to a file, just
        #  session install and print what version and date you are using and
        #  the command line will print the result of the install anyway).
        session.install('-r', f'requirements-{scenario}.txt')
        session.install('-r', '../../requirements-test.txt')

    session.run('pip', 'list', '--format', 'columns')
    os.chdir('../../')
    session.run('pytest', '-m', 'not integration', '--verbose')


PYTHON_VERSIONS_LIST = [
    '3.6.10',
    '3.7',
    '3.8.1',
    # '3.9.1', # Not yet supported by Pyarrow
]
PIP_VERSIONS_LIST = [
    '19.0',  # Oldest pip working with pyarrow 3.0.0. 22nd January 2019.
    '21.0.1',  # Latest pip on 30th January 2021.
]


def test(session, pip_version):
    session.run('pip', 'install', '-U', 'pip=={}'.format(pip_version))

    scenarios_dict = {
        '0': test_requirements_sc0,
        '1': test_requirements_offset_scenarios,
        '2': test_requirements_offset_scenarios,
    }
    scenario = os.environ.get('NOX_SCENARIO')
    print('NOX_SCENARIO=', scenario)
    if scenario in scenarios_dict:
        scenarios_dict[scenario](session)
    else:
        test_existing_requirements(session)


@nox.session(python=PYTHON_VERSIONS_LIST)
@nox.parametrize('pip_version', PIP_VERSIONS_LIST)
def test_python36_python37(session, pip_version):
    min_date = os.environ.get('MIN_DATE')
    if session.python == '3.8.1' and min_date <= '2020-02-01':
        print(
            'Skip as Python 3.8.1 was not supported by our dependencies before'
            f'this date. Python {session.python}, min_date {min_date}'
        )
        session.skip()

    test(session, pip_version)


class RequirementsModifier:

    def __init__(self, from_file):
        self.requirements = from_file
        self.altered_reqs = []

        # Following set for each individual package.
        self.package = None
        self.current_version = None
        self.date_to_version = None
        self.version_to_date = None
        self.dates_lst = None
        self.version_lst = None
        self.min_date = None
        self.passed_constraints = False

        # Temporary dicts to seek out potential versioning issues
        self.version_limits = None
        self.version_override = None
        self.version_omit = None

    def set_known_issues(self):
        # these constraints should be added to requirements.txt
        # if they help avoid versioning error

        # These are the earliest versions of the dependencies that we can
        # support e.g. we cannot support numpy below `1.16.0rc1` because
        # pandas would not be compatible.
        # package<version
        self.version_limits = {
            'numpy': '1.16.0rc1',  # 2018-12-20
            'Flask': '1.0.2',  # 2018-05-02
            'pyarrow': '0.11.1',  # 2018-10-24
            'keyring': '17.1.1',  # 2018-12-23
            'pypermedia': '0.4.2',  # 2016-02-18
            'python-json-logger': '0.1.10',  # 2018-11-07
            'requests': '2.22.0',  # 2019-05-16
            'deprecated': '1.2.4',  # 2019-05-16
            'tqdm': '4.28.1',  # 2018-10-21
            'pyjwt': '1.7.1',  # 2018-12-07
            'requests-toolbelt': '0.8.0',  # 2017-05-20
            'pandas': '0.25.3',  # 2019-11-01
            'tabulate': '0.8.2',  # 2017-11-26
            'pyhumps': '0.5.1',  # 2018-10-30
            'wrapt': '1.10.11',  # 2017-08-11
            'ipywidgets': '7.4.2',  # 2018-09-14
            'ipython': '7.2.0',  # 2018-11-30
            'python-dateutil': '2.7.5',  # 2018-10-27
            's3transfer': '0.1.13',  # 2018-02-15
            # IPV6_ADDRZ_RE should be available in urllib3 1.25.4 forward
            # which is the lowest version of the library botocore supports.
            # https://github.com/boto/botocore/issues/2186#issuecomment-712449171
            'urllib3': '1.25.4',  # 2019-05-02
            'botocore': '1.12.156',  # 2019-05-04 Allows urllib 1.25.4
            'boto3': '1.9.71',  # 2018-12-21
            'boto': '2.49.0',  # 2018-07-11
        }

        # package==version
        self.version_override = {}

        # Ignore these versions as they have breakages e.g. numpy `1.20.0rc1`
        # is not compatible with pyarrow/pandas released at the same time.
        # package!=version
        self.version_omit = {
            'numpy': '1.20.0rc2',
            'pyarrow': '0.13.0',
        }

    def set_requirement_details(self):
        import requests
        dc = requests.get(f'https://pypi.org/pypi/{self.package}/{self.current_version}/json').json()
        releases = dc['releases']
        date_to_version, dates_lst = self.get_requirement_date_to_version(
            releases)
        version_to_date, version_lst = self.get_requirement_version_to_date(
            releases)

        self.date_to_version = date_to_version
        self.version_to_date = version_to_date
        self.dates_lst = dates_lst
        self.version_lst = version_lst

    def get_requirements_list(self, file):
        with open(file) as f:
            ls = f.readlines()
            ln = []
            for l in ls:
                sl = l.split(' ')
                if len(sl) == 1:
                    sl = l.split('\n')
                ln.append(sl[0])
        return ln

    def get_requirement_date_to_version(self, releases):
        dates_lst = []
        dates_dct = {}
        for k, v in releases.items():
            try:
                dates_dct[v[0]['upload_time']] = k
                dates_lst.append(v[0]['upload_time'])
            except Exception:
                try:
                    dates_dct[k] = v['upload_time']
                    dates_lst.append(v[0]['upload_time'])
                except Exception:
                    pass
                    # print(f'No release information for {k}, date to version')
        dates_lst.sort(reverse=True)
        return dates_dct, dates_lst

    def get_requirement_version_to_date(self, releases):
        versions_lst = []
        versions_dict = {}
        for k, v in releases.items():
            try:
                versions_dict[k] = v[0]['upload_time']
                versions_lst.append(k)
            except Exception:
                try:
                    versions_dict[v['upload_time']] = k
                    versions_lst.append(k)
                except Exception:
                    pass
                    # print(f'No release information for {k}, version to date')
        versions_lst.sort(reverse=True)
        return versions_dict, versions_lst

    def write_requirements(self, reqs, file):
        with open(file, 'w') as f:
            f.writelines(reqs)

    def print_requirements_diff(self):
        print('requirements diff:')
        rlen = len(self.altered_reqs)
        r = 0
        while r < rlen:
            print(f'{self.requirements[r]} -> {self.altered_reqs[r]}')
            r += 1

    def get_closest_earlier_date(self, min_date):
        for date in self.dates_lst:
            if date < min_date:
                upd_vrsn = self.date_to_version[date]
                return upd_vrsn, date

        last_date = self.dates_lst[-1:][0]
        return self.date_to_version[last_date], last_date

    def get_earlier_version_with_offset(self, vrsn, offset):
        # 1. get date for existing version
        try:
            date = self.version_to_date[vrsn]
        except Exception:
            for v in self.version_lst:
                if v.startswith(vrsn):
                    # print(f'Using {v} instead of {vrsn} for package: {pckg}')
                    vrsn = v
                    date = self.version_to_date[vrsn]

        year = int(date[:4]) - int(offset[:4])
        month = int(date[5:7]) - int(offset[5:7])
        if month < 10:
            month = f'0{month}'
        day = int(date[8:10]) - int(offset[8:10])
        if day < 10:
            day = f'0{day}'

        udate = f'{year}-{month}-{day}'

        self.min_date = os.environ.get('MIN_DATE')
        if self.min_date is not None and udate < self.min_date:
            udate = self.min_date

        return self.get_closest_earlier_date(udate)

    def find_acceptable_version(self, constraints_dict):
        from packaging import version  # installed to base image

        def run_all_constraint_checks(alt_vrsn, alt_date):
            # Check constraints within requirements.txt
            if ('!=' in constraints_dict and
                    any(v == alt_vrsn for v in constraints_dict['!='])):
                # move down 1 version
                alt_vrsn, alt_date = not_equal(alt_vrsn)

            if ('<=' in constraints_dict and
                    version.parse(alt_vrsn) > version.parse(constraints_dict['<='][0])):
                alt_vrsn, alt_date = smaller_equal()

            if ('<' in constraints_dict and
                    version.parse(alt_vrsn) >= version.parse(constraints_dict['<'][0])):
                alt_vrsn, alt_date = smaller()

            # Apply temporary nox testing constraints
            # 1. check if req has a known issue / limit in version number for
            # nox tests
            if (self.package in self.version_limits and
                    version.parse(alt_vrsn) < version.parse(self.version_limits[self.package])):
                alt_vrsn = self.version_limits[self.package]
                alt_date = self.version_to_date[alt_vrsn]

            # 2. override modification to specific version
            if self.package in self.version_override:
                alt_vrsn = self.version_override[self.package]
                alt_date = self.version_to_date[alt_vrsn]
                print(
                    'override modification to specific version. '
                    f'alt_vrsn {alt_vrsn}, alt_date {alt_date}'
                )

            # 3. for pckg!=version find an earlier version number
            if (self.package in self.version_omit and
                    alt_vrsn == self.version_omit[self.package]):
                alt_vrsn, alt_date = self.get_closest_earlier_date(alt_vrsn)

            self.passed_constraints = True
            return alt_vrsn, alt_date

        def skip_modification():
            # skip modification and check existing version in requirements.txt
            # is valid for ==
            # not all ~=versionA would work with ==versionA!
            try:
                alt_date = self.version_to_date[self.current_version]
                alt_vrsn = self.current_version
                self.passed_constraints = True
                return alt_vrsn, alt_date

            except:
                # req with ~= might be missing a subversion
                # number so we find correct version
                for v in self.version_lst:
                    if self.current_version in v:  # 1.2 in 1.2.9
                        alt_date = self.version_to_date[v]
                        alt_vrsn = v
                        return alt_vrsn, alt_date

        def smaller_equal():  # <=
            # altered req is too small, boundary condition,
            alt_vrsn = constraints_dict['<='][0]
            self.passed_constraints = False
            return alt_vrsn, alt_date

        def smaller():  # <
            # altered req is too small, boundary condition,
            # this occurs when the existing req is 1 off from being too small
            alt_vrsn, alt_date = skip_modification()
            self.passed_constraints = False
            return alt_vrsn, alt_date

        def not_equal(alt_vrsn):  # !=
            # skip the erroneous version
            alt_vrsn, alt_date = self.get_closest_earlier_date(self.version_to_date[alt_vrsn])
            self.passed_constraints = False
            return alt_vrsn, alt_date

        # Get valid version
        if self.min_date is None:
            alt_vrsn, alt_date = skip_modification()

        else:
            # Find a valid earlier date than the environment variable min_date
            alt_vrsn, alt_date = self.get_closest_earlier_date(self.min_date)

            while self.passed_constraints is False:
                alt_vrsn_, alt_date = run_all_constraint_checks(alt_vrsn, alt_date)

                # a new alt_vrsn must be tested again with the constraints
                if alt_vrsn_ != alt_vrsn:
                    self.passed_constraints = False
                alt_vrsn = alt_vrsn_

        return alt_vrsn, alt_date

    def modify_requirements(self, from_file, to_file, min_date):
        # init overrides and set lower limits for package versions to avoid
        # known issues and incompatibilities.
        self.set_known_issues()
        self.min_date = min_date
        # fetch original requirements to modify.
        self.requirements = self.get_requirements_list(from_file)

        for req in self.requirements:
            # I. process a line of the requirements.txt file
            cmpsymbols = ['<=', '>=', '==', '!=', '~=', '*', '<', '>']

            def get_cmpsym(sub):
                for c in cmpsymbols:
                    if c in sub:
                        return c

            L = req.split(' ')
            if L[0].startswith('#'):
                continue
            subexpr = L[0].split(',')

            # subexpr[0] for nox modifications (>=, ==, ~=)
            se = subexpr.pop(0)
            cmpsym = get_cmpsym(se)
            E = se.split(cmpsym)
            self.package = E[0]
            self.current_version = E[-1]

            # request all versions and release dates of a given requirement as helper variables.
            self.set_requirement_details()

            # subexpr[1].. constraints for erroneous versions (<=, !=)
            cntr_dict = {}
            for se in subexpr:
                c = get_cmpsym(se)
                E = se.split(c)
                if c not in cntr_dict:
                    cntr_dict[c] = []
                cntr_dict[c].append(E[-1])

            # II. Do modification to package version.
            self.passed_constraints = False
            alt_vrsn, alt_date = self.find_acceptable_version(cntr_dict)

            if self.min_date is None:
                if self.package in self.version_omit:
                    # Edge case where we are testing betas and we find that
                    # a beta causes a problem so we neeed to exclude it.
                    self.altered_reqs.append(f'{self.package}>={alt_vrsn},!={self.version_omit[self.package]}    # {alt_date[:10]}\n')
                else:
                    self.altered_reqs.append(f'{self.package}>={alt_vrsn}    # {alt_date[:10]}\n')
            else:
                self.altered_reqs.append(f'{self.package}=={alt_vrsn}    # {alt_date[:10]}\n')

        # III. write modified requirements to file for nox testing
        self.write_requirements(self.altered_reqs, to_file)
        self.print_requirements_diff()
