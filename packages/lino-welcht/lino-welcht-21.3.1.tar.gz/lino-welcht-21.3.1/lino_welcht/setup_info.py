# -*- coding: UTF-8 -*-
# Copyright 2002-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

# This module is part of the Lino Welfare test suite.
# To test only this module:
#
#   $ python setup.py test -s tests.PackagesTests

import sys
PY2 = sys.version_info[0] == 2


requires = ['lino-welfare',
            'pytidylib',
            'django-iban', 'metafone',
            'cairocffi']
if PY2:
    requires.append('channels<2')
    requires.append('suds')
else:
    requires.append('channels')
    requires.append('suds-py3')
    # requires.append('suds-jurko')



SETUP_INFO = dict(
    name='lino-welcht',
    version='21.3.1',
    install_requires=requires,
    test_suite='tests',
    tests_require=['pytest'],
    include_package_data=True,
    zip_safe=False,
    description=u"A Lino Welfare for the PCSW of Châtelet",
    long_description=u"""\
**Lino Welfare Châtelet** is a
`Lino Welfare <http://welfare.lino-framework.org>`__
application developed and maintained for the PCSW of Châtelet in Belgium.

- The central project homepage is http://welcht.lino-framework.org

- For *introductions* and *commercial information*
  see `www.saffre-rumma.net
  <http://www.saffre-rumma.net/welfare/>`__.

- Technical specifications and test suites are in
  `Lino Welfare <http://welfare.lino-framework.org>`__.

- The `French project homepage <http://fr.welfare.lino-framework.org>`__
  contains release notes and end-user docs.

- Online demo site at http://welfare-demo.lino-framework.org

""",
    author='Hamza Khchine',
    author_email='hamza@lino-framework.org',
    url="http://welcht.lino-framework.org",
    license='BSD-2-Clause',
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Development Status :: 5 - Production/Stable
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: BSD License
Natural Language :: English
Natural Language :: French
Natural Language :: German
Operating System :: OS Independent
Topic :: Database :: Front-Ends
Topic :: Home Automation
Topic :: Office/Business
Topic :: Sociology :: Genealogy
Topic :: Education""".splitlines())

SETUP_INFO.update(packages=[
    'lino_welcht',
    'lino_welcht.lib',
    'lino_welcht.lib.courses',
    'lino_welcht.lib.courses.fixtures',
    'lino_welcht.lib.cv',
    'lino_welcht.lib.cv.fixtures',
    'lino_welcht.lib.isip',
    'lino_welcht.lib.pcsw',
    'lino_welcht.lib.pcsw.fixtures'
])

SETUP_INFO.update(message_extractors={
    'lino_welcht': [
        ('**/cache/**',          'ignore', None),
        ('**.py',                'python', None),
        ('**.js',                'javascript', None),
        ('**/config/**.html', 'jinja2', None),
        #~ ('**/templates/**.txt',  'genshi', {
        #~ 'template_class': 'genshi.template:TextTemplate'
        #~ })
    ],
})
SETUP_INFO.update(include_package_data=True)

# SETUP_INFO.update(package_data=dict())


# def add_package_data(package, *patterns):
#     l = SETUP_INFO['package_data'].setdefault(package, [])
#     l.extend(patterns)
#     return l
#
# add_package_data('lino_welfare.modlib.cbss',
#                  'WSDL/*.wsdl',
#                  'XSD/*.xsd',
#                  'XSD/SSDN/Common/*.xsd',
#                  'XSD/SSDN/OCMW_CPAS/IdentifyPerson/*.xsd',
#                  'XSD/SSDN/OCMW_CPAS/ManageAccess/*.xsd',
#                  'XSD/SSDN/OCMW_CPAS/PerformInvestigation/*.xsd',
#                  'XSD/SSDN/OCMW_CPAS/Loi65Wet65/*.xsd',
#                  'XSD/SSDN/Person/*.xsd',
#                  'XSD/SSDN/Service/*.xsd')
#
# add_package_data('lino_welfare.modlib.cbss',
#                  'config/cbss/RetrieveTIGroupsRequest/*.odt')
# add_package_data('lino_welfare.modlib.cbss',
#                  'config/cbss/IdentifyPersonRequest/*.odt')
# add_package_data('lino_welfare.modlib.cbss', 'fixtures/*.csv')
# add_package_data('lino_welfare.modlib.cbss', 'fixtures/*.xml')
# add_package_data('lino_welfare.modlib.debts', 'config/debts/Budget/*.odt')
# add_package_data('lino_welfare.modlib.courses', 'config/courses/Course/*.odt')
# add_package_data('lino_welfare.modlib.pcsw', 'config/pcsw/Client/*.odt')
# add_package_data('lino_welfare.modlib.cal', 'config/cal/Guest/*.odt')
# add_package_data('lino_welfare.modlib.jobs',
#                  'config/jobs/ContractsSituation/*.odt')
# add_package_data('lino_welfare.modlib.jobs',
#                  'config/jobs/OldJobsOverview/*.odt')
# add_package_data('lino_welfare.modlib.jobs', 'config/jobs/JobsOverview/*.odt')
# add_package_data('lino_welfare.settings', 'media/pictures/contacts.Person.jpg')
# add_package_data('lino_welfare', 'config/lino_welfare/ActivityReport/*.odt')
# add_package_data('lino_welfare', 'config/admin_main.html')
# l = add_package_data('lino_welfare.modlib.welfare')
# for lng in 'fr de nl'.split():
#     l.append('lino_welfare/modlib/welfare/locale/%s/LC_MESSAGES/*.mo' % lng)
#
