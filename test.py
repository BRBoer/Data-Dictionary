def dothings(index, word):
  entry = ''
  latex = ''
  try:
    entry = '\\noindent\\textbf{' + word['ortho'] + '}'
  except KeyError:
    raise KeyError('Key \'ortho\' does not exist, or is invalid') from None
  except TypeError:
    raise KeyError('Key \'ortho\' is blank') from None

  if 'ipa' in word:
    entry += ' - [' + word['ipa'] + ']'
  
  entry += '''
\hangindent=\parindent
\hangafter=1
'''
  if 'definitions' in word:
    definitions = word['definitions']
    for definition in definitions:
      if 'pos' in definition:
        entry +='\n\\textbf{' + posToAbbrev(definition['pos']) + '.}'
      
      if 'meaning' in definition:
        entry += '\\enspace '+ definition['meaning'] + '\n'

  # if dictionary.index(word) != len(dictionary)-1:
  entry += '\\bigbreak'
  # aggregate entries
  latex += entry
  return latex

# Data is imported now
import yaml

# TODO: Implement abbreviation collapsing
def posToAbbrev(pos):
  return pos


def yamlToLatex(filename):
  entry = ''
  latex = ''
  with open(filename) as f:
    # use safe_load instead load
    data = yaml.safe_load(f)
    dictionary = data['dictionary']
    if 'sections' in dictionary:
      sections = dictionary['sections']
      for section in sections:
        entry += '\\section{' + section['name'] + '}'
        for index, word in enumerate(section['words']):
          entry += dothings(index, word)
    else:
      dictionary = dictionary['words']
      for index, word in enumerate(dictionary):
        entry += dothings(index, word)
    latex += entry
      
    with open('./out.tex', 'w+') as out:
      out.write('''\documentclass[openany, 12pt, twoside]{book}
\\usepackage[headheight=15pt,hmarginratio=1:1]{geometry}
\\usepackage{fontspec}
\\usepackage{fancyhdr}

\\fancypagestyle{plain}{
  \\fancyhf{} % clear all header and footers
  \\renewcommand{\headrulewidth}{0pt} % remove the header rule
  \\fancyfoot[LE, RO]{\\thepage} % Left side on Even pages; Right side on Odd pages
}

\pagestyle{fancy}
\\fancyfoot{}

\\fancyfoot[LE, RO]{\\thepage}

\\setmainfont{Linux Libertine O}
\\begin{document}
\\author{Name}
\\title{Proto-Wei: Comprehensive Dictionary}

\\frontmatter
\\maketitle
\\tableofcontents

\\mainmatter
\\chapter{Lexemeber}

'''
+ latex.rstrip('\\bigbreak') + '''

\\backmatter
% bibliography, glossary and index would go here.

\\end{document}''')

yamlToLatex('thing.yml')


# if __name__ == 'main':
#     # Yada yada cmd stuff
    

