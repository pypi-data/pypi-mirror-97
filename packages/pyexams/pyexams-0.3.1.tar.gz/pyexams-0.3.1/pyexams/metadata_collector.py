# -*- coding: utf-8 -*-

from appdirs import user_config_dir
from pydal import DAL, Field

VERSION = '2020/11/13 v0.1'
EXERCISE_TYPES = ('open', 'numeric', 'schoice', 'mchoice', 'cloze')
EXERCISE_DB = 'mysql://sageexam:XcZekPWZbPoJtTaQOIiB@localhost/sageexamdb'

class MetadataCollector(object):
    """docstring for MetadataCollector."""

    def __init__(self, arg):
        super(MetadataCollector, self).__init__()
        self.arg = arg
        self.db = self.database()

    def database(self):
        #TODO: read from ~/.config/sageexam.config file or similar
        # => use appdirs https://pypi.org/project/appdirs/
    #    config_file = user_config_dir('pyexams')
    #    with open(config_file) as json_data_file:
    #        data = json.load(json_data_file)

        db = DAL(EXERCISE_DB)
        db.define_table('degree',
            Field('name', 'string', length=255, unique=True)
        )
        db.define_table('subject',
            Field('name', 'string', length=255, unique=True)
        )
        db.define_table('exam',
            #examid is a string that should identify the exam uniquely, but can be empty
            Field('examid', 'string'),
            Field('exam_date', 'date'),
            Field('degree', db.degree),
            Field('course', 'integer'),
            Field('subject', db.subject),
            Field('examinstructions', 'text'),
            Field('examdata', 'text'),
        )
        db.define_table('collection',
            Field('name', unique=True, nonempty=True, requires=IS_NOT_EMPTY()),
            Field('folder','string')
        )
        db.define_table('exercise',
            Field('name', requires=IS_NOT_EMPTY()),
            Field('variant', 'integer'),
            Field('collection', db.collection),
            # No need to store code, questions and answers separately
            Field('content', 'text'),
            # All metadata
            Field('score', 'double'),
            Field('type', 'text', requires=IS_IN_SET(EXERCISE_TYPES)),
            Field('solution', 'text')
        )
        db.define_table('exerciseXexam',
            Field('exercise', db.exercise),
            Field('exam', db.exam),
        )
        db.define_table('tag',
            Field('name', 'text', length=20)
        )
        db.define_table('skill',
            Field('name', 'text', length=20)
        )
        db.define_table('exerciseXtag',
            Field('exercise', db.exercise),
            Field('tag', db.tag)
        )
        db.define_table('exerciseXskill',
            Field('exercise', db.exercise),
            Field('skill', db.skill),
            Field('points', 'double')
        )
        return db

    def _collect_from_exercise(self, ex):
        db = self.db
        # Find examinstructions and exercises, store them in the database
        content = str(ex)
        fields = dict(name=None, variant=None, type=None, solution=None, score=None)
        tags = []
        skills = {}
        for texdef in examdata.find_all('def'):
            if texdef.args[0]=='tags':
                tags = texdef.args[1].split(',')
            if texdef.args[0]=='skills':
                tags = dict(pair.split(':') for pair in texdef.args[1].replace(' ','').split(','))
            else:
                fields[texdef.args[0]] = texdef.args[1]
        exercise = db.exercise(name=fields['name'], variant=fields['variant'])
        if exercise:
            exam.update_record(**fields)
            #This is the number of the record in the database, not the string from the teacher
            id_exam = exam.id
        else:
            id_exam = db.exam.insert(**field)

    def collect(self, tex_source):
        from TexSoup import TexSoup
        soup = TexSoup(tex_source, skip_envs=('exercise',))
        db = self.db
        # Find examinstructions and exercises, store them in the database
        examdata = soup.find('examdata')
        instructions = soup.find('examinstructions')
        fields = dict(date=None, degree=None, course=None, subject=None, examid=None)
        for texdef in examdata.find_all('def'):
            if texdef.args[0]=='date':
                date = datetime.date(*[int(n) for n in texdef.args[1].split('-')])
            elif texdef.args[0] in fields:
                fields[texdef.args[0]] = texdef.args[1]
        examid = fields['examid']
        if not examid:
            examid = hash(tuple(field.items()))
            exam = None
        else:
            exam = db.exam(examid=examid)
        if exam:
            exam.update_record(**fields)
            #This is the number of the record in the database, not the string from the teacher
            id_exam = exam.id
        else:
            id_exam = db.exam.insert(**field)
        for exercise in soup.find_all('exercise'):
            _collect_from_exercise(exercise)
