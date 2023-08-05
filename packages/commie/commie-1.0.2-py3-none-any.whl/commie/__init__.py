from .detector import iter_comments_str, iter_comments_file, iter_comments
from .parsers.c_like_parser import extract_comments as iter_comments_c
from .parsers.c_regex_parser import extract_comments as iter_comments_sass
from .parsers.common import Comment, Span, FileError, UnterminatedCommentError
from .parsers.css_parser import extract_comments as iter_comments_css
from .parsers.go_parser import extract_comments as iter_comments_go
from .parsers.html_parser import extract_comments as iter_comments_html
from .parsers.python_parser import extract_comments as iter_comments_python
from .parsers.ruby_parser import extract_comments as iter_comments_ruby
from .parsers.shell_parser import extract_comments as iter_comments_shell
