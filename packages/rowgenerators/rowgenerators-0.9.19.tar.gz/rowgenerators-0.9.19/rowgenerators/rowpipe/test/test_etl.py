from __future__ import print_function

import unittest

from rowgenerators.rowpipe.pipeline import Pipeline, Pipe, PrintRows, Sample, Head, SelectRows, Slice


def cast_str(v):
    return str(v)


def cast_int(v):
    return int(v)


def cast_float(v):
    return float(v)


class Test(unittest.TestCase):

    def test_sample_head(self):

        class Source(Pipe):

            def __iter__(self):
                yield ['int', 'int']

                for i in range(10000):
                    yield ([i, i])

        # Sample
        pl = Pipeline(
            source=Source(),
            first=Sample(est_length=10000),
            last=PrintRows(count=50)
        )

        pl.run()

        # head
        self.assertIn([7, 7], pl[PrintRows].rows)
        self.assertIn([2018, 2018], pl[PrintRows].rows)
        self.assertIn([9999, 9999], pl[PrintRows].rows)

        pl = Pipeline(
            source=Source(),
            first=Head(10),
            last=PrintRows(count=50)
        )

        pl.run()

        self.assertEquals(10, len(pl[PrintRows].rows))

        print(pl)

    def test_select(self):

        class Source(Pipe):
            def __iter__(self):
                yield ['a', 'b']

                for i in range(10000):
                    yield ([i, i])

        pl = Pipeline(
            source=Source(),
            first=SelectRows('row.a == 100 or row.b == 1000'),
            last=PrintRows(count=50)
        )

        pl.run()

        rows = pl[PrintRows].rows

        self.assertEqual(2, len(rows))
        self.assertEqual(100, rows[0][0])
        self.assertEqual(1000, rows[1][1])

    def test_slice(self):

        self.assertEquals('lambda row: tuple(row[0:3])+tuple(row[10:13])+(row[9],)+(row[-1],)',
                          Slice.make_slicer((0, 3), (10, 13), 9, -1)[1])

        self.assertEquals('lambda row: tuple(row[0:3])+tuple(row[10:13])+(row[9],)+(row[-1],)',
                          Slice.make_slicer("0:3,10:13,9,-1")[1])

        return

        class Source(Pipe):
            def __iter__(self):
                yield ['col' + str(j) for j in range(20)]

                for i in range(10000):
                    yield [j for j in range(20)]

        # Sample
        pl = Pipeline(
            source=[Source(), Slice((0, 3), (10, 13), 9, -1)],
            last=PrintRows(count=50)
        )

        pl.run()

        self.assertEquals(
            [1, 0, 1, 2, 10, 11, 12, 9, 19],
            pl[PrintRows].rows[0])
        self.assertEquals(
            ['col0', 'col1', 'col2', 'col10', 'col11', 'col12', 'col9', 'col19'],
            pl[PrintRows].headers)

        self.assertEqual(
            [('0', '3'), ('10', '13'), 9, -1],
            Slice.parse("0:3,10:13,9,-1"))

        pl = Pipeline(
            source=[Source(), Slice("0:3,10:13,9,-1")],
            last=PrintRows(count=50)
        )

        pl.run()

        self.assertEquals([1, 0, 1, 2, 10, 11, 12, 9, 19], pl[PrintRows].rows[0])
        self.assertEquals(
            ['col0', 'col1', 'col2', 'col10', 'col11', 'col12', 'col9', 'col19'],
            pl[PrintRows].headers)

    def test_multi_source(self):

        class Source(Pipe):

            def __init__(self, start):
                self.start = start

            def __iter__(self):

                for i in range(self.start, self.start + 10):
                    if i == self.start:
                        yield ['int', 'int']  # header

                    yield ([self.start, i])

            def __str__(self):
                return 'Source {}'.format(self.start)

        # Sample
        pl = Pipeline(last=PrintRows(count=50))

        pl.run(source_pipes=[Source(0), Source(10), Source(20)])

        self.assertIn([0, 2], pl[PrintRows].rows)
        self.assertIn([10, 18], pl[PrintRows].rows)
        self.assertIn([20, 21], pl[PrintRows].rows)
