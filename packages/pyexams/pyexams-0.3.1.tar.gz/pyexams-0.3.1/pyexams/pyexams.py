#!/usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess
import sys
import os
import shutil
import csv

#import logging
#logging.basicConfig()
#logger = logging.getLogger()

from joblib import Parallel, delayed

from texsurgery.texsurgery import TexSurgery
#from pyexams.metadata_collector import MetadataCollector

class Exams(object):
    """Exams is the main class for reading a source tex file and then
    - reading all metadata and storing it into the database
    - exporting the questions in pdf or moodle format
    - grading the pdf forms
    - sending the statements, or solutions, or commented exams to the students
    - this list will probably grow
    """

    def __init__(self, tex_path):
        self.path = tex_path
        self.basename = os.path.splitext(tex_path)[0]
        with open(tex_path, 'r') as tex_file:
            self.src = tex_file.read()
        self.ts = TexSurgery(self.src)
        #self.question_list is a lazy property
        self._question_list = None

    @property
    def question_list(self):
        if not self._question_list:
            el = self._question_list = dict()
            for qtype, opts, qtext in self.ts.findall(
                'question{qid},questionmult{qid},questionmultx{qid}'):
                qid = opts['qid']
                el[qid] = (qtype, qid, qtext)
        return self._question_list

    def _try_command(self, command):
        process = subprocess.Popen(command, bufsize=-1,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutdata, stderrdata = process.communicate()
        exit_code = process.returncode
        if exit_code:
            print('-'*10)
            print(stdoutdata)
            print('-'*10)
            print(stderrdata)
            print('-'*10)
            sys.exit(exit_code)

    def to_moodle(self, n):
        tex_source, tex_path = self.src, self.path
        basename = os.path.splitext(tex_path)[0]
        tmp_base_path = '%s_moodle_tmp'%(basename)
        tmp_path = tmp_base_path + '.tex'
        xml_tmp_path = tmp_base_path + '.xml'
        xml_output_file = basename + '.xml'

        file = open('students.csv', 'r')
        student_list = list(csv.reader(file, skipinitialspace=True))
        field_names = student_list[0]
        extra_fields = field_names[4:]
        # These variables are only used in the pdf, they do not get exported into moodle
        # (unless the author includes them within the exercises, which she shouldn't)
        # but we will them with dummy values so that amc2moodle does not complain
        dummy = dict(
            name='name', surname='surname',
            include_solution='include_solution',
            index=0, seed=0,
            ncopies=n)
        dummy.update(dict(zip(extra_fields, extra_fields)))
        questions = self.question_list
        useamc = r'\usepackage[bloc,completemulti,pdfform,nowatermark]{automultiplechoice}'
        _,lastpackage = self.ts.findall('\\usepackage{pkgname}')[-1]
        ts = self.ts \
            .insertAfter('\\usepackage{pkgname}[pkgname=%s]'%lastpackage['pkgname'], useamc) \
            .data_surgery(dummy)

        for j,(qtype, qid, qtext) in enumerate(questions.values()):
            #copy and paste each exercise n-1 times, to create the n variants
            # each question has a different index, no need to do anything special
            # for random questions
            variants = '\n'.join(
                r'\begin{{{0}}}{{{1}}}{2}\end{{{0}}}'.format(
                    qtype,
                    qid+'-v'+str(j),
                    TexSurgery(qtext).data_surgery(dict(index=j)).src)
                for j in range(1,n))
            ts.insertAfter('{0}{{qid}}[qid={1}]'.format(qtype, qid), variants)
        tex_out = ts.code_surgery().src
        del ts
        with open(tmp_path, 'w') as tmp_file:
            tmp_file.write(tex_out)
        self._try_command( ['amc2moodle', tmp_path])
        if os.path.exists(xml_output_file):
            os.remove(xml_output_file)
        os.rename(xml_tmp_path, xml_output_file)
        for ext in ('.tex', '.log', '.aux', '.amc', '.out'):
            if os.path.exists(tmp_base_path + ext):
                os.remove(tmp_base_path + ext)

    def to_pdf(self, with_statement, with_solution, do_all, shufflechoices=True):
        types = []
        if with_statement:
#            statements_file = open('email_list_statements', 'w')
            statements_file = None
            types.append(('question', False, statements_file))
        if with_solution:
#            solutions_file = open('email_list_solutions', 'w')
            solutions_file = None
            types.append(('solution', True, solutions_file))
        if do_all:
            for path,_,_ in types:
                if os.path.exists(path):
                    shutil.rmtree(path)
                os.mkdir(path)
        # TODO clean data file
    #    data_file = basename + '.data'
    #    if do_all and os.path.exists(data_file):
    #        os.remove(data_file)

        file = open('students.csv', 'r')
        field_names, *student_list = list(csv.reader(file, skipinitialspace=True))
        extra_fields = field_names[4:]
        if do_all:
            Parallel(n_jobs=8)(
                delayed(self.one_pdf)(
                    student, j, types, extra_fields,
                    do_all=True,
                    ncopies=len(student_list),
                    shufflechoices=shufflechoices)
                for j,student in enumerate(student_list))
            # Non-parallel version
            # for student in student_list:
            #     one_pdf(student, ...)
        else:
            self.one_pdf(student_list[1],
                         types=types,
                         extra_fields=extra_fields,
                         shufflechoices=shufflechoices)

    def one_pdf(self,
                student,
                index=0,
                types=[('question', False, None)],
                extra_fields=[],
                do_all=False,
                ncopies=1,
                shufflechoices=True):
        basename = self.basename
        name,surname,id,email,*extra_vals = student
        tmp_base_path = '%s_%s_tmp'%(basename,id)
        tmp_path = tmp_base_path + '.tex'
        pdf_tmp_path = '%s_%s_tmp.pdf'%(basename,id)
        pdf_output_file = basename + '.pdf'
        student_seed = id
        for (type, is_solution, output_file) in types:
            useamc = r'\usepackage[bloc,completemulti,pdfform,nowatermark%s]{automultiplechoice}'%(
                ',correc' if is_solution else ''
            )
            _,lastpackage = self.ts.findall('\\usepackage{pkgname}')[-1]
            self.src_for_pdf = TexSurgery(self.src)\
                .insertAfter('\\usepackage{pkgname}[pkgname=%s]'%lastpackage['pkgname'], useamc)\
                .src
            student_vars = dict(
                name=name, surname=surname, id=id, seed=id, index=index,
                ncopies=ncopies)
            student_vars.update(dict(zip(extra_fields, extra_vals)))
            #TODO: add import to load our own sty instead of automultiplechoice
            ts = TexSurgery(self.src_for_pdf)
            ts.data_surgery(student_vars).code_surgery()
            if shufflechoices:
                ts.shuffle('choices')
            #TODO: collect exam information
            tex_out = ts.src
            del ts
            with open(tmp_path, 'w') as tmp_file:
                tmp_file.write(tex_out)
            self._try_command( ['pdflatex', '-halt-on-error', '-output-directory', '.', tmp_path])
            if do_all:
                pdf_destination = '%s/%s_%s.pdf'%(type, type, id)
                os.rename(pdf_tmp_path, pdf_destination)
                #TODO: collect student data with joblib
#                output_file.write(','.join([email, pdf_destination])+'\n')
            else:
                if os.path.exists(pdf_output_file):
                    os.remove(pdf_output_file)
                os.rename(pdf_tmp_path, pdf_output_file)
            for ext in ('.tex', '.log', '.aux', '.amc', '.out'):
                if os.path.exists(tmp_base_path + ext):
                    os.remove(tmp_base_path + ext)
    #    for _,_,file in TYPES:
    #        file.close()
