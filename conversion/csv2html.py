#!/usr/bin/env python
import csv, re
import settings
import subprocess, os, shutil

def list_csv_files(directory):
    """
    Keyword Arguments:
    directory -- input directory to be traversed.

    Adds all csv-files in given directory to list.
    """

    files_in_dir = []
    for f in os.listdir(directory):
        if f.endswith('.csv'):
            files_in_dir.append(os.path.join(directory, f))
    return files_in_dir

def create_main_tex_file(directory, output, compilation, title):
    """Creates a main tex file in directory with same name as var
    filename.

    Returns the latex document as a string.

    Keyword Arguments:
    content  -- String formatted as latex. Document content.
    filename --
    """

    # First: List all csv-files in input directory
    content_list = list_csv_files(directory)

    # Then read the csv-files
    for item in content_list:
        frames = csv_to_frames(item)

        # Create temp directory
        d = os.path.join(directory, 'temp')
        if not os.path.exists(d):
            os.mkdir(d)

        # Create .tex-file 
        basename = os.path.basename(item[:-4])
        filename = os.path.join(d, basename + '.tex')
        with open(filename, 'w') as f:
            preamble = settings.preamble
            if title:
                title = "\\title{%s}\n" %title
            else:
                title = ""
            subtitle = "\\subtitle{%s}\n" %basename
            begin_document = "\\begin{document}\n"
            end_document = "\\end{document}"
            complete_content = preamble + title + subtitle + \
                               begin_document + frames + end_document
            f.write(complete_content)

        # Output dir handling
        output_dir = os.path.join(os.path.dirname(filename),
                                  os.pardir, output)
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

        # Either compile tex and put pdf in output, or put tex out dir
        if compilation:
            compile_latex(filename)

            # Move pdf to output dir
            current_pdf = filename[:-4] + '.pdf'
            new_pdf = os.path.join(output,
                                   os.path.basename(current_pdf))
            os.rename(current_pdf, new_pdf)

        else:
            os.rename(filename,
                      os.path.join(output_dir,
                                   os.path.basename(filename)))

    # After last csv, clean up temp directory
    shutil.rmtree(d)


def compile_latex(filename):
    args = ['latexmk', '-pdf', filename]
    subprocess.call(args, cwd=os.path.dirname(filename))


def set_font_commands(string):
    """ Convert input to LaTeX compliant output:
    *content* -> \textbf{content};
    'content' -> `content';
    ... -> \ldots

    Keyword Arguments:
    string -- The input string.
    """

    # Set boldface
    # string = re.sub(r'\*([^\*]+)\*', r'\\textbf{\1}', string)

    # Set quotation marks
    string = re.sub(r'\'([^\']+)\'', r"`\1'", string)

    # Set ldots
    string = re.sub(r'\.{3}', r'\ldots{}', string)

    return(string)

    
def csv_to_frames(filename):
    """
    Put cells of csv in beamer frames.

    Return string: frames

    Keyword Arguments:
    filename -- input file
    """


    with open(filename) as f:
        reader = csv.reader(f)
        frames = ""
        for row in reader:
            for cell in row:
                unicode(cell, 'utf-8')
            question = row[0]
            answer = row[1]

            # Regex convert ~ to \textasciitilde{}
            question = re.sub('~', r"\\textasciitilde{}", question)
            answer = re.sub('~', r"\\textasciitilde{}", answer)

            # Convert *content* to \textbf{content}
            question = set_font_commands(question)
            answer = set_font_commands(answer)

            # Create latex page.
            frames += str("\\begin{frame}\\Large\n")
            frames += str("\\only<1>{%s}\n" % question)
            frames += str("\\only<2>{%s}\n" % answer)
            frames += str("\\end{frame}\n")

    return frames

def __main__():
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Convert one or more csv-files to html-slides ')
    parser.add_argument('directory', nargs='?',
                        help='The root directory to be scanned for '\
                        'csv-files. Default = current working '\
                        'directory')
    parser.add_argument('output',
                        help='Specify an output folder relative to '\
                        'the directory where the pages will be '\
                        'collected. Default = ./output',
                        nargs='?')
    parser.add_argument('--title', '-t',
                       help='Specify a general title that will appear'
                       'in all slides',
                       nargs='?')
    args = parser.parse_args()

    # Input directory
    directory = ''
    if args.directory:
        directory = args.directory
    else:
        directory = os.getcwd()

    # Output directory
    output = ''
    if args.output:
        output = args.output
    else:
        output = os.path.join(directory, 'output')

    # The csv to tex conversion.
    create_main_tex_file(directory, output,
                         args.compilation, args.title)

if __name__ == "__main__":
    __main__()
