# pyexams

Generates variants of exam questions using [texsurgery](https://framagit.org/pang/texsurgery), keeps a question database, exports to pdf and moodle.

Much like [R exams](https://r-exams.org/), but with the following (main) differences:

 1. R-`exams` requires use of R for both creating exam variants and managing R-`exams` itself, while `pyexams` allows any language for exam creation and is called from a command which can be incorporated into your favorite LaTeX editor.
 2. R-`exams` keeps each question in a separate file, then use a simple R script to compose the whole exam, while `pyexams` use a single LaTeX file for the whole exam.
 3. Both R-`exams` and `pyexams` keep a record of past exam questions, but `pyexams` also keeps a database that can be queried in order to find, for instance, all questions with the tag `derivative` that appeared in exams at least two years ago. The question code is also saved in plain text and managed in a `git` repository, which simplifies the management of a shared question bank, whether group-private or totally open.
 4. Last but not least, R-`exams` is a mature and feature rich project, while `pyexams` is a very young project that still has to deliver.

Other important design decisions involved in `pyexams`:

 - The syntax for the questions is exactly that of [auto-multiple-choice](https://www.auto-multiple-choice.net/)
 - We will use [amc2moodle](https://github.com/nennigb/amc2moodle) (or a custom version of it) to generate the moodle question bank.
 - `pyexams` strives to feel as close to LaTeX as possible to its users, which paradoxically is better done through [texsurgery](https://framagit.org/pang/texsurgery) than through a LaTeX package.

## Warning: Alpha version

This is still an early version. Use with care.

## Installation

    python3 -m pip install pyexams

  - Install also a LaTeX distribution which exposes the command `pdflatex`.
  - At this moment, you may also have to install [auto-multiple-choice](https://auto-multiple-choice.net/). This will not be necessary in the future. It is not required to generate the moodle questions, but part of the pyexams experience is to compile the pdf often for quick feeedback.
  - You need to install the `jupyter` kernels you plan to use. The `python3` kernel gets installed when you pip install pyexams, but in order to run the example, you need to install `sympy` too:

    python3 -m pip install sympy

### Install the sagemath kernel (optional)

Right now the only example uses [sagemath](sagemath.org/). You need to install `sagemath`, and then proceed to install the `sagemath` kernel into your system's jupyter. True, the `sagemath` bundle comes with a jupyter server inside, but that won't do: you need to execute this command, if you installed `sagemath` as root:

    `sudo jupyter kernelspec install YOUR_SAGEMATH_INSTALLATION_PATH/local/share/jupyter/kernels/sagemath`

and this other command if you installed it as a regular user:

    `jupyter kernelspec install --user YOUR_SAGEMATH_INSTALLATION_PATH/local/share/jupyter/kernels/sagemath`

## Usage

```bash
cd examples
# generates a pdf for the first student in the list (useful for testing)
pyexams sympy_example.tex
# generates one pdf for each first student in the list (runs in parallel)
pyexams sympy_example -all
# generates two pdf files for each first student in the list (runs in parallel)
#  one with the exam statement
#  other with the correct answer and an explanation
pyexams sympy_example -all -both
# generates a moodle question bank
pyexams sympy_example -moodle  
# generates a moodle question bank with exactly 5 variants of each question
pyexams sympy_example -moodle -n 5
```

## How to use

### Moodle short questions

  1. Start with a template from the `examples` folder, make a copy, edit it.
  2. Use `pyexams your_source_file.tex` to test quickly if your code works.
  3. When happy with the result, run `pyexams your_source_file.tex -moodle -n 5` to generate a moodle question bank with exactly 5 variants of each question.
  4. Inspect `your_source_file.xml` for obvious errors.
  5. If the file looks fine, try to upload to *moodle*.

### Long written answer
  1. Start with a template from the `examples` folder, make a copy, edit it.
  2. Edit `students.csv` with the real data of your students.
  3. Use `pyexams your_source_file.tex` to test quickly if your code works.
  4. When happy with the results, run `pyexams your_source_file.tex -all -both` to generate two pdf files for each first student in the list:
    - one with the exam statement.
    - other with the correct answer and an explanation.
  5. Distribute the exam statements at the date and time of the exam.
  6. Collect the students' solutions using a *moodle task* or any similar tool.
  7. Distribute the exam solutions at the end of the exam.

We suggest two ways to distribute the exam statements:
  - Through moodle:
    1. Prepare a *moodle folder* activity in advance
    2. Prepare mock pdf files with the same filenames as the real exam statements.
    3. Zip all the mock exams into a single file, which you can upload to moodle and unzip to deliver all the mock exams quickly.
    4. Instruct your students to download the mock exam, as a check.
    5. At the date and time of the exam, upload a zip with the real exam stataments, and unzip it to replace the mock exams.
  - Through email:
    1. `pyexams -send emails_config.ini email_body_template` will send an email to each student with the exam statement, or the exam solution, or any other file, such as a `correction` with the teacher's comments to each exam. You can find examples in the `examples` folder.

## Talk at ENSEMAT II

The motivation behind this project and its design decision was presented (in spanish) at a talk at [ENSEMAT II](https://eventos.upm.es/56532/detail/ensemat-2020.-usos-y-avances-en-la-docencia-de-las-matematicas-en-las-ensenanzas-universitarias.html)

 - [Slides for the talk (in spanish)](https://dcain.etsin.upm.es/~pablo/etc/ENSEMATII_sobre_pyexams/pyexams.html)


## Thanks

To all our colleagues that gave feedback to the early versions, specially Fabricio from ETSIN.UPM and carlos from ETSIAAB.UPM
