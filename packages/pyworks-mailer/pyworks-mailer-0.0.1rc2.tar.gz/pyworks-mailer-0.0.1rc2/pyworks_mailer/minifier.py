import argparse
import codecs
import locale
import io
import sys
from htmlmin import Minifier


def minify(input_file, output_file):
    minifier = Minifier()
    default_encoding = 'utf-8'

    if input_file:
        inp = codecs.open(input_file, encoding=default_encoding)
    else:
        encoding = sys.stdin.encoding or locale.getpreferredencoding() or default_encoding
        inp = io.open(sys.stdin.fileno(), encoding=encoding)

    for line in inp.readlines():
        minifier.input(line)

    if output_file:
        codecs.open(
        output_file, 'w', encoding=default_encoding).write(minifier.output)
    else:
        encoding = encoding or sys.stdout.encoding or locale.getpreferredencoding() or default_encoding
        io.open(sys.stdout.fileno(), 'w', encoding=encoding).write(minifier.output)
