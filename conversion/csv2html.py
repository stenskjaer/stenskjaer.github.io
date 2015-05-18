#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv, re
import settings
import subprocess, os, shutil

class Conversion:
    """Handles conversion of the input csv-files to html or tex-format
    
    Returns:
    -- List of formatted content. One list item for each csv-file
    -- List of filenames in the same order as the formatted content.
    """
    def __init__(self, input_dir, output_type):
        self.input_dir = input_dir
        self.output_type = output_type

    def create_output_slides(self):
        """Main function for conversion. 
        
        Keyword Arguments:
        input_dir   -- 
        output_type -- 
        """
        
        content_list = [os.path.join(self.input_dir, f)
                        for f in os.listdir(self.input_dir)
                        if f.endswith('.csv')]

        csv_list, file_list = self.prepare_CSVs(content_list)
        
        if self.output_type == "html":
            return(self.csv_to_html(csv_list), file_list)
        elif self.output_type == "tex" or self.output_type == "pdf":
            return(self.csv_to_tex(csv_list), file_list)
            
                          
    def prepare_CSVs(self, content_list):
        """Prepare list of csv's for conversion: Find title and return list with
        questions, answers and locations

        Keyword Arguments:
        self     -- 
        filename --

        """
        # Init the return list
        return_list = []
        file_list = []

        for item in content_list:
            with open(item) as f:
                filename = os.path.basename(f.name)
                
                # Init the list of this csv
                item_list = []
                
                # Get the file length
                length = sum(1 for row in f) + 1

                # reset counter and init csv.reader
                f.seek(0)           
                reader = csv.reader(f)

                # Get title from first row and put in list
                title = reader.next()[0]

                # Get the question-answer sets and return html
                for i, row in enumerate(reader):

                    # First, set location
                    location = str(i + 1) + ' / ' + str(length - 2)

                    for cell in row:
                        # unicode(cell, 'utf-8')
                        question = row[0]
                        answer = row[1]

                    # Add items as nested list
                    item_list.append([question, answer, location, title])

                return_list.append(item_list)
                file_list.append(filename)
        
        return(return_list, file_list)

                
    def csv_to_html(self, csv_list):
        """Return a nested list of html-buffers from input csv-list
        
        Keyword Arguments: filename --

        """

        decks = []        
        for deck in csv_list:
            
            # Add the prefatory HTML to the list
            frames = []
            frames.append(settings.html_pre)
            
            for card in deck:
                # Put all the question-answer sets in a list called frames
                
                question_answer = ""
                
                # Fontify the strings
                question, answer, location, title = card
                question, answer, location, title = self.fontify_html(
                    question, answer, location, title)

                # Create html
                question_answer += str("""
                <figure class="question">
                <h4>Spørgsmål</h4>
                <p>{0}</p>
                <span class="title">{1}</span>
                <span class="location">{2}</span>
                <div class="close"><a href="../../index.html">&#10005;</a></div>
                </figure>
                """.format(question, title, location))
                question_answer += str("""
                <figure class="answer">
                <h4>Svar</h4>
                <p>{0}</p>
                <span class="title">{1}</span>
                <span class="location">{2}</span>
                <div class="close"><a href="../../index.html">&#10005;</a></div>
                </figure>
                """.format(answer, title, location))

                # Collect all the frames in one list (one deck)
                frames.append(question_answer)

            # Add the remaining HTML to the list
            frames.append(settings.html_post)
                        
            # Collect the complete html-buffer to the list of decs
            decks.append(frames)
                                
        return(decks)
        
    def csv_to_tex(self, csv_list):
        """Return a nested list of tex-buffers from input csv-list
        
        Keyword Arguments: filename --

        """
        
        decks = []
        for deck in csv_list:

            frames = []
            
            # Add preamble
            frames.append(settings.preamble)

            for card in deck:
            # Put all the question-answer sets in a list called frames

                question_answer = ""

                # Fontify the strings
                question, answer, location, title = card
                question, answer, location, title = self.fontify_tex(
                    question, answer, location, title)

                question_answer = r"""
                \begin{frame}\Large
                \only<1>{0}
                \only<2>{1}
                \end{frame}
                """

                # Collect the frames in one deck
                frames.append(question_answer)

            # Close the document
            frames.append("\\end{document}")

            # Collect decks in list of decks
            decks.append(frames)

        return(decks)

    
    def fontify_html(self, *args):
        """Convert input to HTML compliant output:

        Keyword Arguments: *args -- any amount of input strings returned
        in list, reformated.
        """

        output = []
        for string in args:
            # Set boldface
            string = re.sub(r'\*([^\*]+)\*', r'<strong>\1</strong>', string)

            # Set quotation marks
            string = re.sub(r'\'([^\']+)\'', r"&lsquo;\1&rsquo;", string)

            # Set en-hyphens
            string = string.replace('--', '–')

            # Set ldots
            string = string.replace('...', '&hellip;')

            # Set linebreaks
            string = string.replace('\\\\', '<br />')

            output.append(string)

        return(output)


    def fontify_tex(self, *args):
        """ Convert input to LaTeX compliant output:
        *content* -> \textbf{content};
        'content' -> `content';
        ... -> \ldots

        Keyword Arguments:
        string -- The input string.
        """

        output = []
        for string in args:

            # Set boldface
            string = re.sub(r'\*([^\*]+)\*', r'\\textbf{\1}', string)

            # Set quotation marks
            string = re.sub(r'\'([^\']+)\'', r"`\1'", string)

            # Set ldots
            string = re.sub(r'\.{3}', r'\ldots{}', string)

            output.append(string)
        
        return(output)


class CreateFiles:
    
    def __init__(self, content, output_dir, output_type, filenames):
        self.output_dir = output_dir
        self.content = content
        self.filenames = filenames
        self.output_type = output_type
    
        # Create output dir if necessary
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        self.file_content_list = zip(self.filenames, self.content)
    
    def create_files(self):
        """Creates the output in specified directory
        
        Keyword Arguments:
        content_list -- 
        """
        
        for item in self.file_content_list:

            content = ' '.join(item[1])

            # Create file 
            basename = os.path.basename(item[0][:-4])
            if self.output_type == "html":
                file_ending = '.html'
            elif self.output_type == "tex" or self.output_type == "pdf":
                file_ending = '.tex'
                
            new_filename = os.path.join(self.output_dir, basename + file_ending)

            with open(new_filename, 'w') as f:
                f.write(content)


    def compile_tex(self):
        """Compile the tex files and put pdf's in $output_dir/pdf

        """

        # Create temp and pdf directory in output-dir
        temp = os.path.join(self.output_dir, 'temp')
        if not os.path.exists(temp):
            os.mkdir(temp)

        pdf_dir = os.path.join(self.output_dir, 'pdf')
        if not os.path.exists(pdf_dir):
            os.mkdir(pdf_dir)

        # Create list of tex-files to be compiled
        orig_filelist = [os.path.join(self.output_dir, f)
                    for f in os.listdir(self.output_dir)
                    if f.endswith('.tex')]

        # Create copy in temp-dir of tex-files
        for file in orig_filelist: shutil.copy(file, temp)

        temp_filelist = [os.path.join(temp, f) for f in os.listdir(temp)
                         if f.endswith('.tex')]
        
        for file in temp_filelist:
            args = ['latexmk', '-pdf', '-xelatex', file]
            print file
            subprocess.call(args, cwd=temp)
            
            # Move pdf to output dir
            current_pdf = file[:-4] + '.pdf'
            new_pdf = os.path.join(pdf_dir,
                                   os.path.basename(current_pdf))
            os.rename(current_pdf, new_pdf)


        # After last tex-file, remove temp-dir
        shutil.rmtree(temp)
                

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

    output_type = "html"
    conversion_object = Conversion(directory, output_type)
    content, filenames = conversion_object.create_output_slides()
    
    output_object = CreateFiles(content, output, output_type, filenames)
    output_object.create_files()

if __name__ == "__main__":
    __main__()
