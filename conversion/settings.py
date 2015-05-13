# Default file configuration

preamble = r"""\documentclass[13pt]{beamer}
\geometry{paperwidth=64mm, paperheight=105mm, landscape}
\useoutertheme{infolines}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}{
  \leavevmode%
  \hbox{%
  \begin{beamercolorbox}[wd=.85\paperwidth,left]{title in head/foot}%
    \hspace*{1em}%
    \usebeamerfont{title in head/foot}\insertshorttitle\ \insertshortsubtitle%
  \end{beamercolorbox}%
  \begin{beamercolorbox}[wd=.15\paperwidth,ht=2.25ex,dp=1ex,center]{title in head/foot}%
    \insertframenumber{} / \inserttotalframenumber\hspace*{1em}
  \end{beamercolorbox}}%
  \vskip0pt%
}
\setbeamerfont{footline}{size=\fontsize{9}{11}\selectfont}
\setbeamersize{text margin left=30pt, text margin right=25pt}
\date{}
\usepackage{xltxtra}
\usepackage{libertine}
\usepackage{microtype}
\usepackage{polyglossia}
\setmainlanguage{danish}
"""
