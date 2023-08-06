from atelier.invlib import setup_from_tasks
ns = setup_from_tasks(
    globals(), "lino_welcht",
    languages=['en', 'de', 'fr'],
    doc_trees=['docs', 'frdocs'],
    # tolerate_sphinx_warnings=True,
    blogref_url='http://luc.lino-framework.org',
    revision_control_system='git',
    locale_dir='lino_welcht/locale',
    cleanable_files=['docs/api/lino_welcht.*'])

    # apidoc_exclude_pathnames:
    # - lino_welfare/projects
