test = {
  'name': 'smallest-int-count',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          sqlite> SELECT * FROM smallest_int_count LIMIT 50;
          0|2
          1|22
          2|6
          3|2
          4|5
          5|3
          6|2
          7|5
          8|4
          9|3
          12|1
          13|2
          14|5
          15|1
          17|2
          18|1
          19|3
          22|1
          26|1
          29|2
          31|4
          37|1
          39|2
          40|1
          43|1
          47|1
          49|1
          55|1
          93|1
          108|1
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'ordered': False,
      'scored': True,
      'setup': r"""
      sqlite> .read lab13_extra.sql
      """,
      'teardown': '',
      'type': 'sqlite'
    }
  ]
}
