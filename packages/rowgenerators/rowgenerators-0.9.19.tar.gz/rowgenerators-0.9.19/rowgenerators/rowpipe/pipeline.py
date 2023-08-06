# Copyright (c) 2016 Civic Knowledge. This file is licensed under the terms of the
# MIT License, included in this distribution as LICENSE.txt

"""Pipes, pipe segments and piplines, for flowing data from sources to partitions.

"""



class PipelineError(Exception):

    def __init__(self, pipe, *args, **kwargs):
        from rowgenerators.util import qualified_class_name

        super(PipelineError, self).__init__(*args, **kwargs)
        self.pipe = pipe
        self.exc_name = qualified_class_name(self)
        self.extra = ''
        self.extra_section = ''

        assert isinstance(pipe, Pipe), "Got a  type: " + str(type(pipe))

    def __str__(self):
        return "Pipeline error: {}; {}".format(self.exc_name, self.message)

    def details(self):
        from rowgenerators.util import qualified_class_name

        return """
======================================
Pipeline Exception: {exc_name}
Message:         {message}
Pipeline:        {pipeline_name}
Pipe:            {pipe_class}
Source:          {source_name}, {source_id}
Segment Headers: {headers}
{extra}
-------------------------------------
{extra_section}
Pipeline:
{pipeline}
""".format(message=self.message, pipeline_name=self.pipe.pipeline.name, pipeline=str(self.pipe.pipeline),
           pipe_class=qualified_class_name(self.pipe), source_name=self.pipe.source.name,
           source_id=self.pipe.source.vid,
           headers=self.pipe.headers, exc_name=self.exc_name, extra=self.extra,
           extra_section=self.extra_section)


class BadRowError(PipelineError):
    def __init__(self, pipe, row, *args, **kwargs):
        super(BadRowError, self).__init__(pipe, *args, **kwargs)

        self.row = row

    def __str__(self):
        self.extra = 'Last Row       : {}'.format(self.row)
        return super(BadRowError, self).__str__()


class MissingHeaderError(PipelineError):
    def __init__(self, pipe, table_headers, header, table, *args, **kwargs):
        super(MissingHeaderError, self).__init__(pipe, *args, **kwargs)

        self.table_headers = table_headers
        self.header = header
        self.table = table

    def __str__(self):
        self.extra = \
            """
Missing Header:  {header}
Table headers :  {table_headers}
""".format(header=self.header, table_headers=self.table_headers)

        self.extra_section = \
            """
{table_columns}
-------------------------------------
""".format(table_columns=str(self.table))

        return super(MissingHeaderError, self).__str__()


class BadSourceTable(PipelineError):
    def __init__(self, pipe, source_table, *args, **kwargs):
        super(BadSourceTable, self).__init__(pipe, *args, **kwargs)

        self.source_table = source_table

    def __str__(self):
        self.extra = \
            """
Bad/Missing Table:  {source_table}
""".format(source_table=self.source_table)
        return super(BadSourceTable, self).__str__()


class StopPipe(Exception):
    pass


class Pipe(object):
    """A step in the pipeline"""

    _source_pipe = None
    _source = None

    bundle = None
    partition = None  # Set in the Pipeline
    segment = None  # Set to the name of the segment
    pipeline = None  # Set to the name of the segment
    headers = None
    limit = None
    indent = '    '  # For __str__ formatting

    scratch = {}  # Data area for the casters and derived values to use.

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source_pipe):
        raise NotImplemented("Use set_source_pipe instead")

    @property
    def source_pipe(self):
        assert bool(self._source_pipe)
        return self._source_pipe

    def set_source_pipe(self, source_pipe):
        self._source_pipe = source_pipe
        self._source = source_pipe.source if source_pipe and hasattr(source_pipe, 'source') else None

        return self

    def process_header(self, headers):
        """Called to process the first row, the header. Must return the header,
        possibly modified. The returned header will be sent upstream"""

        return headers

    def process_body(self, row):
        """Called to process each row in the body. Must return a row to be sent upstream"""
        return row

    def finish(self):
        """Called after the last row has been processed"""
        pass

    def __iter__(self):
        rg = iter(self._source_pipe)
        self.row_n = 0
        self.headers = self.process_header(next(rg))

        yield self.headers

        header_len = len(self.headers)

        try:
            for row in rg:
                row = self.process_body(row)

                if row:  # Check that the rows have the same length as the header
                    self.row_n += 1
                    if len(row) != header_len:
                        m = 'Header width mismatch in row {}. Row width = {}, header width = {}'.format(
                            self.row_n, len(row), header_len)

                        self.bundle.error(m)
                        raise BadRowError(self, row, m)

                    yield row
        except StopIteration:
            return
        except Exception as e:
            if self.bundle:
                pass
                # self.bundle.error("Exception during pipeline processing, in pipe {}: {} "
                #                   .format(qualified_class_name(self), e))
            raise

        self.finish()

    def log(self, m):

        if self.bundle:
            self.bundle.logger.info(m)

    def error(self, m):

        if self.bundle:
            self.bundle.logger.error(m)

    def print_header(self):

        from rowgenerators.util import qualified_class_name

        return qualified_class_name(self)

    def __str__(self):
        return self.print_header()


class DatafileSourcePipe(Pipe):
    """A Source pipe that generates rows from an MPR file.  """

    def __init__(self, bundle, source):
        self.bundle = bundle

        if isinstance(source, str):
            source = bundle.source(source)

        self._source = source

        self._datafile = source.datafile
        # file_name is for the pipeline logger, to generate a file
        self.file_name = source.name
        self.path = self._datafile.path

    def __iter__(self):

        self.start()

        if self.limit:
            raise NotImplementedError()

        with self._datafile.reader as r:

            if r.n_rows == 0:
                return

            # Gets the headers from the source table, which assumes that the
            # source table was created in ingestion.
            self.headers = self._source.headers

            # No? then get the headers from the datafile
            if not self.headers:
                self.headers = r.headers

            yield self.headers

            for row in r.rows:
                yield row

        self.finish()

    def start(self):
        pass

    def finish(self):
        pass

    def __str__(self):
        from ..util import qualified_class_name

        return '{}; {} {}'.format(qualified_class_name(self), type(self.source), self.path)


class SourceFileSourcePipe(Pipe):
    """A source pipe that read from the original data file, but skips rows according to the sources's
    row spec"""

    def __init__(self, bundle, source_rec, source_file):
        """

        :param bundle:
        :param source_rec:
        :param source_file:
        :return:
        """
        self.bundle = bundle

        self._source = source_rec
        self._file = source_file

        try:
            self.path = self._file.path
        except AttributeError:
            self.path = self._source.name

        self.file_name = self._source.name

    def __iter__(self):

        self.start()

        self.headers = self._source.headers

        # No? then get the headers from the datafile
        if not self.headers:
            self.headers = self._file.headers

        itr = iter(self._file)

        start_line = self._source.start_line or 0

        # Throw away data before the data start line,
        for i in range(start_line):
            next(itr)

        yield self.headers

        if self.limit:

            if self._source.end_line:
                for i in range(start_line, self._source.end_line):
                    if i > self.limit:
                        break
                    yield next(itr)
            else:
                for i, row in enumerate(itr):
                    if i > self.limit:
                        break
                    yield row


        else:

            if self._source.end_line:
                for i in range(start_line, self._source.end_line):
                    yield next(itr)
            else:
                for row in itr:
                    yield row

        self.finish()

    def start(self):
        pass

    def finish(self):
        pass

    def __str__(self):
        from ..util import qualified_class_name

        return '{}; {} {}'.format(qualified_class_name(self), type(self.source), self.path)


class RowGenerator(object):
    """Base class for generator objects"""
    def __init__(self, bundle, source=None):

        self._bundle = bundle
        self._source = source



class PartitionSourcePipe(Pipe):
    """Base class for a source pipe that implements it own iterator """

    def __init__(self, bundle, source, partition):

        self.bundle = bundle
        self._source = source
        self._partition = partition

        self._partition.localize()

        # file_name is for the pipeline logger, to generate a file
        self.file_name = self._source.name

    def __iter__(self):

        self.start()

        if self.limit:
            raise NotImplementedError()

        yield [c.name for c in self._partition.table.columns]

        for row in iter(self._partition):
            yield row

        self.finish()

    def start(self):
        pass

    def finish(self):
        pass

    def __str__(self):
        from ..util import qualified_class_name
        return 'Partition {}'.format(qualified_class_name(self))


class Sink(Pipe):
    """ A final stage pipe, which consumes its input and produces no output rows. """

    def __init__(self, count=None, callback=None, callback_freq=1000):
        self._count = count
        self._callback = callback
        self._callback_freq = callback_freq
        self.i = 0
        self._start_time = None

    def run(self, count=None,  *args, **kwargs):
        from time import time

        self._start_time = time()

        count = count if count else self._count
        cb_count = self._callback_freq
        for i, row in enumerate(self._source_pipe):
            self.i = i
            if count and i == count:
                break

            if cb_count == 0:
                cb_count = self._callback_freq
                self._callback(self, i)
            cb_count -= 1



    def report_progress(self):
        """
        This function can be called from a higher level to report progress. It is usually called from an alarm
        signal handler which is installed just before starting an operation:

        :return: Tuple: (process description, #records, #total records, #rate)
        """
        from time import time

        # rows, rate = pl.sink.report_progress()
        return (self.i, round(float(self.i) / float(time() - self._start_time), 2))


class IterSource(Pipe):
    """Creates a source from an Iterator"""

    def __init__(self, iterator, header=None):
        self.iterator = iterator
        self.header = header

    def __iter__(self):

        itr = iter(self.iterator)

        if self.header:
            yield self.header
        else:
            # Create a header from the datatypes
            first = next(itr)
            yield [type(e).__name__ for e in first]
            yield first

        for row in itr:
            yield row


class OnlySource(Pipe):
    """Only allow iteration on a named source. """

    def __init__(self, sources):

        if not isinstance(sources, (list, tuple)):
            sources = [sources]
        else:
            sources = list(sources)

        self.sources = sources

    def process_header(self, row):

        if self.source.name not in self.sources:
            raise StopPipe

        self.headers = row
        return row


class Nullify(Pipe):
    """Turn all column values that don't represent a real value, such as SPACE, empty string, or None,
    into a real None value"""

    def __init__(self):
        """
        Construct with one or more 2-element tuple or a string, in a similar format to what
        __getitem__ accepts

        >>> s = Slice((2,3), (6,8))
        >>> s = Slice("2:3,6:8")

        :param args: One or more slice objects
        :return:
        """

        self.row_processor = None

    def process_header(self, row):
        code = ','.join(['nullify(row[{}])'.format(i) for i, _ in enumerate(row)])

        self.row_processor = eval('lambda row: [{}]'.format(code), self.bundle.exec_context())

        return row

    def process_body(self, row):
        return self.row_processor(row)

    def __str__(self):
        from ..util import qualified_class_name
        return '{} '.format(qualified_class_name(self))


class Slice(Pipe):
    """Select a slice of the table, using a set of tuples to represent the start and end positions of each
    part of the slice."""

    def __init__(self, *args):
        """
        Construct with one or more 2-element tuple or a string, in a similar format to what
        __getitem__ accepts

        >>> s = Slice((2,3), (6,8))
        >>> s = Slice("2:3,6:8")

        :param args: One or more slice objects
        :return:
        """

        self._args = args
        self.code = None

    @staticmethod
    def parse(v):
        """
        Parse a slice string, of the same form as used by __getitem__

        >>> Slice.parse("2:3,7,10:12")

        :param v: Input string
        :return: A list of tuples, one for each element of the slice string
        """

        parts = v.split(',')

        slices = []

        for part in parts:
            p = part.split(':')

            if len(p) == 1:
                slices.append(int(p[0]))
            elif len(p) == 2:
                slices.append(tuple(p))
            else:
                raise ValueError("Too many ':': {}".format(part))

        return slices

    @staticmethod
    def make_slicer(*args):

        if len(args) == 1 and isinstance(args[0], str):
            args = Slice.parse(args[0])

        parts = []

        for slice in args:
            parts.append('tuple(row[{}:{}])'.format(slice[0], slice[1])
                         if isinstance(slice, (tuple, list)) else '(row[{}],)'.format(slice))

            code = 'lambda row: {}'.format('+'.join(parts))
            func = eval(code)

        return func, code

    def process_header(self, row):

        args = self._args

        if not args:
            args = self.source.segment

        try:
            self.slicer, self.code = Slice.make_slicer(args)
        except Exception as e:
            raise PipelineError(self, 'Failed to eval slicer for parts: {} for source {} '
                                      .format(args, self.source.name))

        try:
            self.headers = self.slicer(row)
            return self.headers
        except Exception as e:

            raise PipelineError(self, "Failed to run slicer: '{}' : {}".format(self.code, e))

    def process_body(self, row):

        return self.slicer(row)

    def __str__(self):
        from ..util import qualified_class_name

        return '{}; Slice Args = {}'.format(qualified_class_name(self), self.code)


class Head(Pipe):
    """ Pass-through only the first N rows
    """

    def __init__(self, N=20):
        self.N = N
        self.i = 0

    def process_body(self, row):
        if self.i >= self.N:
            raise StopIteration

        self.i += 1
        return row

    def __str__(self):
        return '{}; N={}; i={}'.format(super(Head, self).__str__(), self.N, self.i)


class Sample(Pipe):
    """ Take a sample of rows, skipping rows exponentially to end at the est_length input row, with
    count output rows.
    """

    def __init__(self, count=20, skip=5, est_length=10000):

        from math import log, exp
        self.skip = float(skip)
        self.skip_factor = exp(log(est_length / self.skip) / (count - 1))
        self.count = count
        self.i = 0

    def process_body(self, row):

        if self.count == 0:
            raise StopIteration

        if self.i % int(self.skip) == 0:
            self.count -= 1
            self.skip = self.skip * self.skip_factor

        else:
            row = None

        self.i += 1
        return row


class Ticker(Pipe):
    """ Ticks out 'H' and 'B' for header and rows.
    """

    def __init__(self, name=None):
        self._name = name

    def process_body(self, row):
        print(self._name if self._name else 'B')
        return row

    def process_header(self, row):
        print('== {} {} =='.format(self.source.name, self._name if self._name else ''))
        return row


class SelectRows(Pipe):
    """ Pass-through only rows that satisfy a predicate. The predicate may be
    specified as a callable, or a string, which will be evaled. The predicate has the signature f(source, row)
    where row is a RowProxy object.

    """

    def __init__(self, pred):
        """

        >>> Select(' row.id == 10 or source.grain == 20 ')

        :param pred: Callable or string. If a string, it must be just an expression which can take arguments source and row
        :return:
        """
        if isinstance(pred, str):
            self.pred_str = pred
            self.pred = eval('lambda source, row: {}'.format(pred))
        else:
            self.pred = pred
            self.pred_str = str(pred)

        self._row_proxy = None

    def process_body(self, row):

        if self.pred(self.source, self._row_proxy.set_row(row)):
            return row
        else:
            return None

    def process_header(self, row):

        from rowgenerators.rowproxy import RowProxy

        self._row_proxy = RowProxy(row)
        return row

    def __str__(self):

        from rowgenerators.util import qualified_class_name

        return qualified_class_name(self) + ': pred = {} '.format(self.pred_str)


class MatchPredicate(Pipe):
    """Store rows that match a predicate. THe predicate is a function that takes the row as its
    sole parameter and returns true or false.

    Unlike the Select pipe, MatchPredicate passes all of the rows through and only stores the
    ones that match

    The matches can be retrieved from the pipeline via the ``matches`` property
    """

    def __init__(self, pred):
        self._pred = pred
        self.i = 0
        self.matches = []

    def process_body(self, row):
        if self._pred(row):
            self.matches.append(row)

        return row


class AddHeader(Pipe):
    """Adds a header to a row file that doesn't have one. If no header is specified in the
     constructor, use the source table. """

    def __init__(self, headers=None):

        self._added_headers = headers

    def __iter__(self):

        if not self._added_headers:
            self._added_headers = [c.name for c in self.source.source_table.columns]

        yield self._added_headers

        for row in self._source_pipe:
            yield row


class AddDestHeader(Pipe):
    """Adds a header to a row file that doesn't have one. If no header is specified in the constructor,
     use the destination table, excluding the first ( id ) column."""

    def __init__(self, headers=None):

        self._added_headers = headers

    def __iter__(self):

        rg = iter(self._source_pipe)

        if not self._added_headers:
            self._added_headers = [c.name for c in self.source.dest_table.columns][1:]

        self.headers = self._added_headers
        yield self._added_headers

        for row in rg:
            yield row


class AddSourceHeader(Pipe):
    """Uses the source table header for the header row"""

    def __init__(self):
        pass

    def __iter__(self):

        rg = iter(self._source_pipe)

        yield [c.name for c in self.source.source_table.columns]

        for row in rg:
            yield row


class ReplaceWithDestHeader(Pipe):
    """Replace the incomming header with the destination header, excluding the destination tables
     first column, which should be the id"""

    def __init__(self):
        pass

    def process_header(self, headers):
        """Ignore the incomming header and replace it with the destination header"""

        return [c.name for c in self.source.dest_table.columns][1:]


class MapHeader(Pipe):
    """Alter the header using a map"""

    def __init__(self, header_map):
        self._header_map = header_map

    def __iter__(self):
        rg = iter(self._source_pipe)

        self.headers = [self._header_map.get(c, c) for c in next(rg)]

        yield self.headers

        for row in rg:
            yield row


class CastSourceColumns(Pipe):
    """Cast a row from the source to the types described in the source  """

    def __init__(self, error_on_fail=False):

        self.processor = None

    def process_header(self, headers):
        st = self.source.source_table

        def cast_maybe(type_, v):
            try:
                return type_(v)
            except:
                return v

        from dateutil import parser

        def date(v):
            return parser.parse(v).date()

        def datetime(v):
            return parser.parse(v)

        def time(v):
            return parser.parse(v).time()

        inner_code = ','.join(['cast_maybe({},row[{}])'
                               .format(c.datatype, i)
                               for i, c in enumerate(st.columns)])

        self.processor = eval('lambda row: [{}]'.format(inner_code), locals())

        return headers

    def process_body(self, row):
        return self.processor(row)

    def __str__(self):

        from rowgenerators.util import qualified_class_name

        return qualified_class_name(self)


class MapSourceHeaders(Pipe):
    """Alter the header using the source_header and dest_header in the source table. The primary
     purpose of this pipe is to normalize multiple sources to one header structure, for instance,
      there are multiple year releases of a file that have column name changes from year to year. """

    def __init__(self, error_on_fail=False):

        self.error_on_fail = error_on_fail
        self.map = {}

    def process_header(self, headers):

        is_generator = False
        is_partition = isinstance(self._source_pipe, PartitionSourcePipe)

        if len(list(self.source.source_table.columns)) == 0:

            if is_generator or is_partition:
                # Generators or relations are assumed to return a valid, consistent header, so
                # if the table is missing, carry on.

                assert headers
                return headers

            else:

                raise PipelineError(
                    self,
                    "Source table {} has no columns, can't map header".format(self.source.source_table.name))

        else:

            dest_headers = [c.dest_header for c in self.source.source_table.columns]

            if len(headers) != len(dest_headers):
                raise PipelineError(self, ('Source headers not same length as source table for source {}.\n'
                                           'Table : {} headers: {}\n'
                                           'Source: {} headers: {}\n')
                                    .format(self.source.name, len(dest_headers), dest_headers,
                                            len(headers), headers))

        return dest_headers

    def process_body(self, row):

        return super(MapSourceHeaders, self).process_body(row)

    def __str__(self):

        from rowgenerators.util import qualified_class_name

        return qualified_class_name(self) + ': map = {} '.format(self.map)


class NoOp(Pipe):
    """Do Nothing. Mostly for replacing other pipes to remove them from the pipeline"""


class MangleHeader(Pipe):
    """"Alter the header so the values are well-formed, converting to alphanumerics and underscores"""

    def mangle_column_name(self, i, n):
        """
        Override this method to change the way that column names from the source are altered to
        become column names in the schema. This method is called from :py:meth:`mangle_header` for each column in the
        header, and :py:meth:`mangle_header` is called from the RowGenerator, so it will alter the row both when the
        schema is being generated and when data are being inserted into the partition.

        Implement it in your bundle class to change the how columsn are converted from the source into database-friendly
        names

        :param i: Column number
        :param n: Original column name
        :return: A new column name
        """
        raise NotImplementedError

    def mangle_header(self, header):

        return [self.mangle_column_name(i, n) for i, n in enumerate(header)]

    def __iter__(self):

        itr = iter(self.source_pipe)

        headers = next(itr)

        self.headers = self.mangle_header(headers)
        yield self.headers

        while True:
            yield next(itr)


class MergeHeader(Pipe):
    """Strips out the header comments and combines multiple header lines to emit a
    single header line"""

    footer = None
    data_start_line = 1
    data_end_line = None
    header_lines = [0]
    header_comment_lines = []
    header_mangler = None

    headers = None
    header_comments = None
    footers = None

    initialized = False

    def init(self):
        """Deferred initialization b/c the object con be constructed without a valid source"""
        from itertools import chain

        def maybe_int(v):
            try:
                return int(v)
            except ValueError:
                return None

        if not self.initialized:

            self.data_start_line = 1
            self.data_end_line = None
            self.header_lines = [0]

            if self.source.start_line:
                self.data_start_line = self.source.start_line
            if self.source.end_line:
                self.data_end_line = self.source.end_line
            if self.source.header_lines:
                self.header_lines = list(map(maybe_int, self.source.header_lines))
            if self.source.comment_lines:
                self.header_comment_lines = list(map(maybe_int, self.source.comment_lines))

            max_header_line = max(chain(self.header_comment_lines, self.header_lines))

            if self.data_start_line <= max_header_line:
                self.data_start_line = max_header_line + 1

            if not self.header_comment_lines:
                min_header_line = min(chain(self.header_lines))
                if min_header_line:
                    self.header_comment_lines = list(range(0, min_header_line))

            self.headers = []
            self.header_comments = []
            self.footers = []

            self.initialized = True
            self.i = 0

    def coalesce_headers(self):
        self.init()

        if len(self.headers) > 1:

            # If there are gaps in the values in the first header line, extend them forward
            hl1 = []
            last = None
            for x in self.headers[0]:
                if not x:
                    x = last
                else:
                    last = x

                hl1.append(x)

            self.headers[0] = hl1

            header = [' '.join(col_val.strip() if col_val else '' for col_val in col_set)
                      for col_set in zip(*self.headers)]
            header = [h.strip() for h in header]

            return header

        elif len(self.headers) > 0:
            return self.headers[0]

        else:
            return []

    def __iter__(self):
        self.init()

        if len(self.header_lines) == 1 and self.header_lines[0] == 0:
            # This is the normal case, with the header on line 0, so skip all of the
            # checks

            # NOTE, were also skiping the check on the data end line, which may sometimes be wrong.

            for row in self._source_pipe:
                yield row

        else:

            max_header_line = max(self.header_lines)

            for row in self._source_pipe:

                if self.i < self.data_start_line:
                    if self.i in self.header_lines:
                        self.headers.append(
                            [_to_ascii(x) for x in row])

                    if self.i in self.header_comment_lines:
                        self.header_comments.append(
                            [_to_ascii(x) for x in row])

                    if self.i == max_header_line:
                        yield self.coalesce_headers()

                elif not self.data_end_line or self.i <= self.data_end_line:
                    yield row

                elif self.data_end_line and self.i >= self.data_end_line:
                    self.footers.append(row)

                self.i += 1

    def __str__(self):

        from rowgenerators.util import qualified_class_name

        return qualified_class_name(self) + ': header = {} ' \
            .format(','.join(str(e) for e in self.header_lines))


class AddDeleteExpand(Pipe):
    """Edit rows as they pass through

    The constructor can take four types of functions:

    add: a list of headers, or a dict of functions, each of which will add a new column to the table
    delete: A list of headers of columns to remove from the table
    edit: A dict of functions to each the values in a row
    expand: Like add, but adds multiple values.

    Many of the arguments take a dict, with each key being the name of a header and the value being a function
    to produce a value for the row. In all cases, the function signature is:

        f(pipe, row, value)

    However, the value is only set for edit entries

    >>> pl = b.pipeline('source','dimensions')
    >>> pl.last.append(AddDeleteExpand(
    >>>     delete = ['time','county','state'],
    >>>     add={ "a": lambda e,r: r[4], "b": lambda e,r: r[1]},
    >>>     edit = {'stusab': lambda e,r,v: v.lower(), 'county_name' : lambda e,v: v.upper() },
    >>>     expand = { ('x','y') : lambda e, r: [ parse(r[1]).hour, parse(r[1]).minute ] } ))

    The ``add`` argument may also take a list, which is the names of the headers to add. The column value will be None.

    """

    def __init__(self, add=[], delete=[], edit={}, expand={}, as_dict=False):
        """

        :param add: List of blank columns to add, by header name, or dict of
            headers and functions to create the column value
        :param delete: List of headers names of columns to delete
        :param edit: Dict of header names and functions to alter the value.
        :return:
        """

        from collections import OrderedDict

        self.add = add
        self.delete = delete
        self.edit = edit
        self.expand = expand

        self.as_dict = as_dict

        if isinstance(self.add, (list, tuple)):
            # Convert the list of headers into a sets of functins that
            # just produce None
            self.add = OrderedDict((k, lambda e, r, v: None) for k in self.add)

        self.edit_header = None
        self.edit_header_code = None
        self.edit_row = None
        self.edit_row_code = None
        self.expand_row = None
        self.expand_row_code = None

        self.edit_functions = None  # Turn dict lookup into list lookup

        self._row_proxy = None

    def process_header(self, row):

        from rowgenerators.rowproxy import RowProxy

        self.edit_functions = [None] * len(row)

        header_parts = []
        row_parts = []
        for i, h in enumerate(row):

            if h in self.delete:
                pass
            elif h in self.edit:
                self.edit_functions[i] = self.edit[h]
                row_parts.append('self.edit_functions[{i}](self,r, r[{i}])'.format(i=i))
                header_parts.append('r[{}]'.format(i))
            else:
                row_parts.append('r[{}]'.format(i))
                header_parts.append('r[{}]'.format(i))

        for f in self.add.values():
            self.edit_functions.append(f)
            i = len(self.edit_functions) - 1
            assert self.edit_functions[i] == f
            row_parts.append('self.edit_functions[{i}](self,r, None)'.format(i=i))

        # The expansions get tacked onto the end, after the adds.
        header_expansions = []
        row_expanders = []  # The outputs of the expanders are combined, outputs must have same length as header_expansions
        self.expand_row = lambda e: []  # Null output

        for k, f in self.expand.items():
            self.edit_functions.append(f)
            i = len(self.edit_functions) - 1
            assert self.edit_functions[i] == f
            header_expansions += list(k)  # k must be a list or tuple or other iterable.
            row_expanders.append('self.edit_functions[{i}](self,r, None)'.format(i=i))

        if header_expansions:
            self.expand_row_code = "lambda r,self=self: ({})".format('+'.join(row_expanders))
            self.expand_row = eval(self.expand_row_code)

        # Maybe lookups in tuples is faster than in lists.
        self.edit_functions = tuple(self.edit_functions)

        header_extra = ["'{}'".format(e) for e in (list(self.add.keys()) + header_expansions)]

        # Build the single function to edit the header or row all at once
        self.edit_header_code = "lambda r: [{}]".format(','.join(header_parts + header_extra))
        self.edit_header = eval(self.edit_header_code)
        # FIXME: Should probably use itemgetter() instead of eval
        self.edit_row_code = "lambda r,self=self: [{}]".format(','.join(row_parts))
        self.edit_row = eval(self.edit_row_code)

        # Run it!
        headers = self.edit_header(row)

        self._row_proxy = RowProxy(headers)

        return headers

    def process_body(self, row):

        rp = self._row_proxy.set_row(row)

        try:
            r1 = self.edit_row(rp)
        except:
            # Todo, put this into the exception
            print('EDIT ROW CODE', self.edit_row_code)
            raise

        try:
            r2 = self.expand_row(rp)
        except:
            # FIXME: put this into the exception
            print('EXPAND ROW CODE: ', self.expand_row_code)
            raise

        return r1 + r2

    def __str__(self):
        from ..util import qualified_class_name

        return (qualified_class_name(self) + '\n' +
                self.indent + 'H:' + str(self.edit_header_code) + '\n' +
                self.indent + 'B:' + str(self.edit_row_code))


class Add(AddDeleteExpand):
    """Add fields to a row"""

    def __init__(self, add):
        """Add fields using a dict of lambdas. THe new field is appended to the end of the row.

        >>> pl = Pipeline()
        >>> pl.last = Add({'source_id': lambda pipe,row: pipe.source.sequence_id })

        """
        super(Add, self).__init__(add=add)


class Expand(AddDeleteExpand):
    """Add columns to the header"""

    def __init__(self, expand, as_dict=False):
        super(Expand, self).__init__(expand=expand, as_dict=as_dict)


class Delete(AddDeleteExpand):
    """Delete columns. """

    def __init__(self, delete):
        super(Delete, self).__init__(delete=delete)

    def __str__(self):
        from rowgenerators.util import qualified_class_name


        return qualified_class_name(self) + 'delete = ' + ', '.join(self.delete)


class SelectColumns(AddDeleteExpand):
    """Pass through only the sepcified columns, deleting all others.  """

    def __init__(self, keep):
        super(SelectColumns, self).__init__()

        self.keep = keep

    def process_header(self, row):
        self.delete = filter(lambda e: e not in self.keep, row)

        return super(SelectColumns, self).process_header(row)

    def __str__(self):
        from rowgenerators.util import qualified_class_name

        return qualified_class_name(self) + ' keep = ' + ', '.join(self.keep)


class Edit(AddDeleteExpand):
    def __init__(self, edit, as_dict=False):
        super(Edit, self).__init__(edit=edit, as_dict=as_dict)


class PassOnlyDestColumns(Delete):
    """Delete any columns that are not in the destination table"""

    def __init__(self):
        super(PassOnlyDestColumns, self).__init__(delete=[])

    def process_header(self, row):
        dest_cols = [c.name for c in self.source.dest_table.columns]

        self.delete = [h for h in row if h not in dest_cols]

        return super(Delete, self).process_header(row)


class CastColumns(Pipe):
    """Composes functions to map from the source table, to the destination table, with potentially
    complex transformations for each column.

    The CastColumns pipe uses the transformation values in the destination schema ,
    datatype, nullify, initialize, typecast, transform and exception, to transform the source rows to destination
    rows. The output rows have the lenghts and column types as speciefied in the destination schema.

    """

    def __init__(self):

        super(CastColumns, self).__init__()

        self.row_processors = []
        self.orig_headers = None
        self.new_headers = None
        self.row_proxy_1 = None # Row proxy with  source headers
        self.row_proxy_2 = None # Row proxy with dest headers

        self.accumulator = {}
        self.errors = None

        self.row_n = 0

    def process_header(self, headers):

        from rowgenerators.rowproxy import RowProxy

        self.orig_headers = headers
        self.row_proxy_1 = RowProxy(self.orig_headers)

        if len(self.source.dest_table.columns) <= 1:
            raise PipelineError(self, "Destination table {} has no columns, Did you run the schema phase?"
                                .format(self.source.dest_table.name))

        # Return the table header, rather than the original row header.

        self.new_headers = [c.name for c in self.source.dest_table.columns]

        self.row_proxy_2 = RowProxy(self.new_headers)

        self.row_processors = self.bundle.build_caster_code(self.source, headers, pipe=self)

        self.errors = {}

        for h in self.orig_headers + self.new_headers:
            self.errors[h] = set()

        return self.new_headers

    def process_body(self, row):

        from rowgenerators.rowpipe.exceptions import CastingError, TooManyCastingErrors

        scratch = {}
        errors = {}

        # Start off the first processing with the source's source headers.
        rp = self.row_proxy_1

        try:
            for proc in self.row_processors:
                row = proc(rp.set_row(row), self.row_n, self.errors, scratch, self.accumulator,
                           self, self.bundle, self.source)

                # After the first round, the row has the destinatino headers.
                rp = self.row_proxy_2
        except CastingError as e:
            raise PipelineError(self, "Failed to cast column in table {}, row {}: {}"
                                .format(self.source.dest_table.name, self.row_n, e))
        except TooManyCastingErrors:
            self.report_errors()


        return row

    def report_errors(self):

        from rowgenerators.rowpipe.exceptions import TooManyCastingErrors

        if sum(len(e) for e in self.errors.values()) > 0:
            for c, errors in self.errors.items():
                for e in errors:
                    self.bundle.error(u'Casting Error: {}'.format(e))

            raise TooManyCastingErrors()

    def finish(self):
        super(CastColumns, self).finish()

        self.report_errors()



    def __str__(self):

        from rowgenerators.util import qualified_class_name

        o = qualified_class_name(self) + '{} pipelines\n'.format(len(self.row_processors))

        return o


class Modify(Pipe):
    """Base class to modify a whole row, as a dict. Does not modify the header. Uses a slower method
    than other editing pipes. """

    def __iter__(self):
        from collections import OrderedDict

        rg = iter(self._source_pipe)

        self.headers = self.process_header(next(rg))

        yield self.headers

        for row in rg:

            row = self.process_body(OrderedDict(list(zip(self.headers, row))))

            if row:
                yield list(row.values())


class RemoveBlankColumns(Pipe):
    """Remove columns that don't have a header"""

    def __init__(self):
        self.editor = None

    def process_header(self, row):

        header_parts = []
        for i, h in enumerate(row):
            if h.strip():
                header_parts.append('r[{}]'.format(i))

        if header_parts:
            # FIXME: Should probably use itemgetter() instead of eval
            self.editor = eval("lambda r: [{}]".format(','.join(header_parts)))
            return self.editor(row)
        else:
            # If there are no header parts, replace the process_body() method with a passthrough.
            self.process_body = lambda self, row: row
            return row

    def process_body(self, row):
        return self.editor(row)


class Skip(Pipe):
    """Skip rows of a table that match a predicate """

    def __init__(self, pred, table=None):
        """

        :param pred:
        :param table:
        :return:
        """

        self.pred = pred

        try:
            self.table = table.name
        except AttributeError:
            self.table = table

        self._check = False

        self.skipped = 0
        self.passed = 0
        self.ignored = 0
        self.env = None
        self.code = None

    def process_header(self, headers):
        from .codegen import calling_code

        from rowgenerators.rowproxy import RowProxy

        self.env = self.bundle.exec_context(source=self.source, pipe=self)


        if self.pred in self.env:
            self.code = 'lambda pipe, bundle, source, row: {}'.format(calling_code(self.env[self.pred], self.pred))
            self.pred = eval(self.code, self.env)

        elif not callable(self.pred):
            self.code = 'lambda pipe, bundle, source, row: {}'.format(self.pred)
            self.pred = eval(self.code, self.env)

        else:
            self.code = self.pred
            pass  # The predicate is a callable but not in the environment.

        # If there is no table specified, always run the predicate, but if the table
        # is specified, only run the predicate for that table.
        if self.table is None:
            self._check = True
        else:
            self._check = self.table == self.source.dest_table.name

        self.row_proxy = RowProxy(headers)

        return headers

    def __str__(self):
        return 'Skip. {} skipped, {} passed, {} ignored'.format(self.skipped, self.passed, self.ignored)

    def process_body(self, row):

        try:
            if not self._check:
                self.ignored += 1
                return row
            elif self.pred(self, self.bundle, self.source, self.row_proxy.set_row(row)):
                self.skipped += 1
                return None
            else:
                self.passed += 1
                return row
        except Exception as e:
            self.bundle.error("Failed to process predicate in Skip pipe: '{}' ".format(self.code))
            raise


class Collect(Pipe):
    """Collect rows so they can be viewed or processed after the run. """

    def __init__(self):
        self.rows = []

    def process_body(self, row):
        self.rows.append(row)
        return row

    def process_header(self, row):
        return row


class LogRate(Pipe):
    def __init__(self, output_f, N, message=None):
        raise NotImplementedError()
        #self.lr = init_log_rate(output_f, N, message)

    def process_body(self, row):
        self.lr()
        return row


class PrintRows(Pipe):
    """A Pipe that collects rows that pass through and displays them as a table when the pipeline is printed. """

    def __init__(self, count=10, columns=None, offset=None, print_at=None):
        self.columns = columns
        self.offset = offset
        self.count_inc = count
        self.count = count
        self.rows = []
        self.i = 1

        try:
            self.print_at_row = int(print_at)
            self.print_at_end = False

        except:
            self.print_at_row = None
            self.print_at_end = bool(print_at)

    def process_body(self, row):
        orig_row = list(row)

        if self.i < self.count:
            append_row = list(row)

            self.rows.append(append_row[self.offset:self.columns])

        if self.i == self.print_at_row:
            print(str(self))

        self.i += 1

        return orig_row

    def finish(self):

        if self.print_at_end:
            print(str(self))

        # For multi-run pipes, the count is the number of rows per source.
        self.count += self.count_inc

    def process_header(self, row):
        return row

    def __str__(self):

        from tabulate import tabulate

        from rowgenerators.util import qualified_class_name

        if self.rows:
            aug_header = ['0'] + ['#' + str(j) + ' ' + str(c) for j, c in enumerate(self.headers)]

            return (qualified_class_name(self) +
                    ' {} rows total\n'.format(self.i) +
                    tabulate([[i] + row for i, row in enumerate(self.rows)],
                             headers=aug_header[self.offset:self.columns], tablefmt='pipe'))
        else:
            return qualified_class_name(self) + ' 0 rows'


class PrintEvery(Pipe):
    """Print a row every N rows. Always prints the header. """

    def __init__(self, N=1):
        self.N = N
        self.i = 0

    def process_header(self, row):
        print('Print Header: ', row)
        return row

    def process_body(self, row):
        if self.i % self.N == 0:
            print('Print Row   :', row)
        self.i += 1
        return row


class Reduce(Pipe):
    """Like works like reduce() on the body rows, using the function f(accumulator,row) """

    def __init__(self, f, initializer=None):
        self._f = f
        self._initializer = initializer
        self.accumulator = None

    def __iter__(self):

        it = iter(self._source_pipe)

        # Yield the header
        self.headers = next(it)
        yield self.headers

        if self._initializer is None:
            try:
                self.accumulator = self._f(None, next(it))
            except StopIteration:
                raise TypeError('reduce() of empty sequence with no initial value')
        else:
            self.accumulator = self._initializer

        for row in it:
            self.accumulator = self._f(self.accumulator, row)
            yield row


def make_table_map(table, headers):
    """Create a function to map from rows with the structure of the headers to the structure of the table."""

    header_parts = {}
    for i, h in enumerate(headers):
        header_parts[h] = 'row[{}]'.format(i)

    body_code = 'lambda row: [{}]'.format(','.join(header_parts.get(c.name, 'None') for c in table.columns))
    header_code = 'lambda row: [{}]'.format(
        ','.join(header_parts.get(c.name, "'{}'".format(c.name)) for c in table.columns))

    return eval(header_code), eval(body_code)


class PipelineSegment(list):
    def __init__(self, pipeline, name, *args):
        list.__init__(self)

        self.pipeline = pipeline
        self.name = name

        for p in args:
            assert not isinstance(p, (list, tuple))
            self.append(p)

    def __getitem__(self, k):
        import inspect

        # Index by class
        if inspect.isclass(k):

            matches = [e for e in self if isinstance(e, k)]

            if not matches:
                raise IndexError('No entry for class: {}'.format(k))

            k = self.index(matches[0])  # Only return first index

        return super(PipelineSegment, self).__getitem__(k)

    def append(self, x):
        self.insert(len(self), x)
        return self

    def prepend(self, x):
        self.insert(0, x)
        return self

    def insert(self, i, x):
        import inspect

        assert not isinstance(x, (list, tuple))

        if inspect.isclass(x):
            x = x()

        if isinstance(x, Pipe):
            x.segment = self
            x.pipeline = self.pipeline

        assert not inspect.isclass(x)

        super(PipelineSegment, self).insert(i, x)

    @property
    def source(self):
        return self[0].source


from collections import OrderedDict

class Pipeline(OrderedDict):
    """Hold a defined collection of PipelineGroups, and when called, coalesce them into a single pipeline """

    bundle = None
    name = None
    phase = None
    dest_table = None
    source_table = None
    source_name = None
    final = None
    sink = None

    _group_names = ['source', 'source_map', 'first', 'map', 'cast', 'body',
                    'last', 'select_partition', 'write', 'final']

    def __init__(self, bundle=None, *args, **kwargs):

        super(Pipeline, self).__init__()
        super(Pipeline, self).__setattr__('bundle', bundle)
        super(Pipeline, self).__setattr__('name', None)
        super(Pipeline, self).__setattr__('phase', None)
        super(Pipeline, self).__setattr__('source_table', None)
        super(Pipeline, self).__setattr__('dest_table', None)
        super(Pipeline, self).__setattr__('source_name', None)
        super(Pipeline, self).__setattr__('final', [])
        super(Pipeline, self).__setattr__('stopped', False)
        super(Pipeline, self).__setattr__('sink', None)

        for k, v in kwargs.items():
            if k not in self._group_names:
                raise IndexError('{} is not a valid pipeline section name'.format(k))

        for group_name in self._group_names:
            gs = kwargs.get(group_name, [])
            if not isinstance(gs, (list, tuple)):
                gs = [gs]

            self.__setitem__(group_name, PipelineSegment(self, group_name, *gs))

        if args:
            self.__setitem__('body', PipelineSegment(self, 'body', *args))

    def _subset(self, subset):
        """Return a new pipeline with a subset of the sections"""

        pl = Pipeline(bundle=self.bundle)
        for group_name, pl_segment in self.items():
            if group_name not in subset:
                continue
            pl[group_name] = pl_segment
        return pl

    def configure(self, pipe_config):
        """Configure from a dict"""

        # Create a context for evaluating the code for each pipeline. This removes the need
        # to qualify the class names with the module

        # ambry.build comes from ambry.bundle.files.PythonSourceFile#import_bundle
        eval_locals = dict()

        replacements = {}

        def eval_pipe(pipe):
            if isinstance(pipe, str):
                try:
                    return eval(pipe, {}, eval_locals)
                except SyntaxError as e:
                    raise SyntaxError("SyntaxError while parsing pipe '{}' from metadata: {}"
                                      .format(pipe, e))
            else:
                return pipe

        def pipe_location(pipe):
            """Return a location prefix from a pipe, or None if there isn't one """
            if not isinstance(pipe, str):
                return None

            elif pipe[0] in '+-$!':
                return pipe[0]

            else:
                return None

        for segment_name, pipes in list(pipe_config.items()):
            if segment_name == 'final':
                # The 'final' segment is actually a list of names of Bundle methods to call afer the pipeline
                # completes
                super(Pipeline, self).__setattr__('final', pipes)
            elif segment_name == 'replace':
                for frm, to in pipes.items():
                    self.replace(eval_pipe(frm), eval_pipe(to))
            else:

                # Check if any of the pipes have a location command. If not, the pipe
                # is cleared and the set of pipes replaces the ones that are there.
                if not any(bool(pipe_location(pipe)) for pipe in pipes):
                    # Nope, they are all clean
                    self[segment_name] = [eval_pipe(pipe) for pipe in pipes]
                else:
                    for i, pipe in enumerate(pipes):

                        if pipe_location(pipe):  # The pipe is prefixed with a location command
                            location = pipe_location(pipe)
                            pipe = pipe[1:]
                        else:
                            raise PipelineError(
                                'If any pipes in a section have a location command, they all must'
                                ' Segment: {} pipes: {}'.format(segment_name, pipes))

                        ep = eval_pipe(pipe)

                        if location == '+':  # append to the segment
                            self[segment_name].append(ep)
                        elif location == '-':  # Prepend to the segment
                            self[segment_name].prepend(ep)
                        elif location == '!':  # Replace a pipe of the same class

                            if isinstance(ep, type):
                                repl_class = ep
                            else:
                                repl_class = ep.__class__

                            self.replace(repl_class, ep, segment_name)

    def replace(self, repl_class, replacement, target_segment_name=None):
        """Replace a pipe segment, specified by its class, with another segment"""

        for segment_name, pipes in self.items():

            if target_segment_name and segment_name != target_segment_name:
                raise Exception()

            repl_pipes = []
            found = False
            for pipe in pipes:
                if isinstance(pipe, repl_class):
                    pipe = replacement
                    found = True

                repl_pipes.append(pipe)

            if found:
                found = False
                self[segment_name] = repl_pipes

    @property
    def file_name(self):
        try:
            return self.source[0].file_name
        except Exception:
            raise

    def __setitem__(self, k, v):

        # If the caller tries to set a pipeline segment with a pipe, translte
        # the call to an append on the segment.

        if isinstance(v, (list, tuple)):
            v = list(filter(bool, v))

        empty_ps = PipelineSegment(self, k)

        if isinstance(v, Pipe) or (isinstance(v, type) and issubclass(v, Pipe)):
            # Assignment from a pipe is appending
            self[k].append(v)
        elif v is None:
            # Assignment from None
            super(Pipeline, self).__setitem__(k, empty_ps)
        elif isinstance(v, (list, tuple)) and not v:
            # Assignment from empty list
            super(Pipeline, self).__setitem__(k, empty_ps)
        elif isinstance(v, PipelineSegment):
            super(Pipeline, self).__setitem__(k, v)
        elif isinstance(v, (list, tuple)):
            # Assignment from a list
            super(Pipeline, self).__setitem__(k, PipelineSegment(self, k, *v))
        else:
            # This maybe should be an error?
            super(Pipeline, self).__setitem__(k, v)

        assert isinstance(self[k], PipelineSegment), 'Unexpected type: {} for {}'.format(type(self[k]), k)

    def __getitem__(self, k):

        # Index by class. Looks through all of the segments for the first pipe with the given class
        import inspect
        if inspect.isclass(k):

            chain, last = self._collect()

            matches = [e for e in chain if isinstance(e, k)]

            if not matches:
                raise IndexError("No entry for class: {} in {}".format(k, chain))

            return matches[0]
        else:
            return super(Pipeline, self).__getitem__(k)

    def __getattr__(self, k):
        if not (k.startswith('__') or k.startswith('_OrderedDict__')):
            return self[k]
        else:
            return super(Pipeline, self).__getattr__(k)

    def __setattr__(self, k, v):
        if k.startswith('_OrderedDict__') or k in (
                'name', 'phase', 'sink', 'dest_table', 'source_name', 'source_table', 'final'):
            return super(Pipeline, self).__setattr__(k, v)

        self.__setitem__(k, v)

    def _collect(self):
        import inspect

        chain = []

        # This is supposed to be an OrderedDict, but it doesn't seem to want to
        # retain the ordering, so we force it on output.

        for group_name in self._group_names:

            assert isinstance(self[group_name], PipelineSegment)

            for p in self[group_name]:
                chain.append(p)

        if len(chain):
            last = chain[0]

            for p in chain[1:]:
                assert not inspect.isclass(p)
                try:
                    p.set_source_pipe(last)
                    last = p
                except:
                    print(p)
                    raise
        else:
            last = None

        for p in chain:
            p.bundle = self.bundle

        return chain, last

    def run(self, count=None, source_pipes=None, callback=None, limit = None):

        try:

            self.sink = Sink(count=count, callback=callback)

            if source_pipes:
                for source_pipe in source_pipes:

                    if self.bundle:
                        self.bundle.logger.info(
                            'Running source {} in a multi-source run'.format(source_pipe.source.name))

                    self['source'] = [source_pipe]  # Setting as a scalar appends, as a list will replace.

                    chain, last = self._collect()

                    self.sink.set_source_pipe(last)

                    self.sink.run(limit=limit)

            else:
                chain, last = self._collect()

                self.sink.set_source_pipe(last)

                self.sink.run(limit=limit)

        except StopPipe:
            super(Pipeline, self).__setattr__('stopped', True)

        return self

    def iter(self):

        chain, last = self._collect()

        # Iterate over the last pipe, which will pull from all those before it.
        for row in last:
            yield row

    def __str__(self):

        out = []
        chain, last = self._collect()

        for pipe in chain:
            segment_name = pipe.segment.name if hasattr(pipe, 'segment') else '?'
            out.append('{}: {}'.format(segment_name, pipe))

        out.append('final: ' + str(self.final))

        return 'Pipeline {}\n'.format(self.name if self.name else '') + '\n'.join(out)

    def headers_report(self):

        from tabulate import tabulate

        from rowgenerators.util import qualified_class_name

        out = []
        chain, last = self._collect()
        for pipe in chain:

            seg_name = pipe.segment.name if hasattr(pipe, 'segment') else '?'

            if not hasattr(pipe, 'headers') or not pipe.headers:
                out.append([seg_name, qualified_class_name(pipe)])
            else:
                try:
                    v = [seg_name, qualified_class_name(pipe),
                         len(pipe.headers)] + [str(e)[:10] for e in pipe.headers if e]
                    out.append(v)

                except AttributeError:
                    pass

        if not out:
            return None

        # Make all lines the same length
        ll = max(len(e) for e in out)
        for i in range(len(out)):
            if len(out[i]) < ll:
                out[i] += [''] * (ll - len(out[i]))

        return tabulate(out)


def augment_pipeline(pl, head_pipe=None, tail_pipe=None):
    """
    Augment the pipeline by adding a new pipe section to each stage that has one or more pipes. Can be used for debugging

    :param pl:
    :param DebugPipe:
    :return:
    """

    for k, v in pl.items():
        if v and len(v) > 0:
            if head_pipe and k != 'source':  # Can't put anything before the source.
                v.insert(0, head_pipe)

            if tail_pipe:
                v.append(tail_pipe)


def _to_ascii(s):
    """ Converts given string to ascii ignoring non ascii.
    Args:
        s (text or binary):

    Returns:
        str:
    """
    # TODO: Always use unicode within ambry.


    if isinstance(s, str):
        ascii_ = s.encode('ascii', 'ignore')
    elif isinstance(s, bytes):
        ascii_ = s.decode('utf-8').encode('ascii', 'ignore')
    else:
        raise Exception('Unknown text type - {}'.format(type(s)))
    return ascii_
