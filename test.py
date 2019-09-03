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
  if 'etymology' in word:
    entry += ' ← ' + word['etymology']
  
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
        
        entry += '''
\hangindent=\parindent
\hangafter=1'''

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
  with open(filename, encoding='utf-8') as f:
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
      
    with open('./out.tex', 'w+', encoding='utf-8') as out:
      out.write('''\documentclass[openany, 12pt, twoside, twocolumn]{book}
\\usepackage[headheight=15pt,hmarginratio=1:1]{geometry}
\\usepackage{fontspec}
\\usepackage{fancyhdr}
\\usepackage[explicit]{titlesec}
\\titleformat{\section}{\Large\\bf}{}{0em}{#1}



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
\\author{''' + data['dictionary']['author'] + '''}
\\title{''' + data['dictionary']['title'] + '''}

\\frontmatter
\\maketitle
\\tableofcontents

\\mainmatter

'''
+ latex.rstrip('\\bigbreak') + '''

\\backmatter
% bibliography, glossary and index would go here.

\\end{document}''')

yamlToLatex('thing.yml')


# if __name__ == 'main':
#     # Yada yada cmd stuff
    

