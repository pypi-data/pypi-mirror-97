#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#This file is part of newdle
#Copyright © 2020 Nokia Corporation and/or its subsidiary(-ies). All rights reserved. *
#
# Authors:
#   Marc-Olivier Buob <marc-olivier.buob@nokia-bell-labs.com>
#   Mélanie Cambus    <melanie.cambus@nokia.com>

import re

def make_css(color :str = "white", background :str = "#99B92C", width :str = "100%") -> str:
    return """
        <!-- https://www.alsacreations.com/article/lire/1335-html5-details-summary.html -->
        <style>

        details {
            width   : %(width)s;   /* Box width */
            margin  : 10px 0; /* Vertical space between two boxes */
        }
        
        summary {
            color: %(color)s;        /* Font color */
            background: %(background)s; /* Background color */
            border-radius: 5px;  /* Rounded corners */
            padding: 5px;        /* Padding inside each box */
            cursor: pointer;     /* Change cursor */
        }

        .children {
            margin-left: 20px;   /* Horizontal left indent */
        }
        
        .document {
            font-size: medium;
            text-align: left;
            margin: 5px;        /* Space between documents */
            padding: 5px;       /* Inside each document box */
            position: relative;
            word-wrap: break-word;
        }

        .document p {
            margin-block-start: 0em;
            margin-block-end: 0;
        }

        .document .contents {
            font-size: small;
        }

        .document details:hover {
            outline-right: 3px;
            outline-color: blue;
        }

        .document table {
          font-family: arial, sans-serif;
          border-collapse: collapse;
          width: 100%%;
        }

        .document td, th {
          border: 1px solid #dddddd;
          text-align: left;
          padding: 8px;
        }

        </style>
        """ % {
            "color" : color,
            "background" : background,
            "width" : width
        }

CSS = make_css()

def html(s :str): 
   """ 
    Evaluate HTML code in a Jupyter Notebook. 
    Args: 
        s: A str containing HTML code. 
    """ 
   from IPython.display import display, HTML 
   chart = HTML(s)
   # or chart = charts.plot(...) 
   display(chart)

class FormatKeywords:
    def __init__(self, keywords, callback):
        self.regexp = re.compile(
            r"\b" \
            + "(%s)" % "|".join([
                re.escape(keyword) for keyword in set(keywords)
            ]) \
            + r"\b"
        ) if keywords else None
        self.callback = callback
    def __call__(self, text :str) -> str:
        return self.regexp.sub(
            self.callback(r"\1"),
            text
        ) if self.regexp else text
    
def boldize(word :str) -> str:
    return "<b>%s</b>" % word

def colorize(s :str, color) -> str:
    return "<font color='%s'>%s</font>" % (color, s)

def make_html(node :dict, pairs = None) -> str:
    def format_text(text :str):
        for (node_to_keywords, callback) in pairs:
            keywords = node_to_keywords(node)
            format_keywords = FormatKeywords(keywords, callback)
            text = format_keywords(text)
        return text

    text = node.get("text")
    return \
        """
        <details>
          <summary>%(text)s</summary>
          <a href="%(url)s">link to document</a>
          <div class="children">
              %(children)s
          </div>
        </details>
        """ % {
            "text"     : (
                ""   if not text  else
                text if not pairs else
                format_text(text)
            ),
            "children" : "".join([
                make_html(child, pairs)
                for child in node.get("children", list())
            ]),
            "url" : node.get("url")
        }
