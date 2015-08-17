# -*- coding: utf-8 -*-

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

html_pre = r"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="chrome=1">
    <meta name="description" content="Programmerede grammatikker : Repositorium til de programmerede latinske og græske grammatikker Vade Mecum og Echo">

    <link rel="stylesheet" type="text/css" media="screen" href="../../stylesheets/stylesheet.css">
    <link rel="stylesheet" type="text/css" media="screen" href="../../stylesheets/simple-slideshow-styles.css">
    <title>Programmerede grammatikker</title>
  </head>

  <body>
    <!-- MAIN CONTENT -->
    <div id="slide-wrap">
      <section id="slides">
        <div class="bss-slides num1" tabindex="1" autofocus="autofocus">
"""

html_post = """
        </div>
      </section>
    </div>

	<script src="../../js/better-simple-slideshow.js"></script> <!-- Main script for slideshow -->
	<script src="../../js/hammer.min.js"></script><!-- for swipe support on touch interfaces -->
	<script>
	  var opts = {
      auto : false,
      fullScreen : false, 
      swipe : true
	  };
	  makeBSS('.bss-slides', opts);
	</script>
        <script>
          (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
          (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
          m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
          })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

          ga('create', 'UA-66419604-1', 'auto');
          ga('send', 'pageview');

        </script>
  </body>
</html>
"""
