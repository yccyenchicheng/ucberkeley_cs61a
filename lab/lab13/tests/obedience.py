test = {
  'name': 'obedience',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          sqlite> SELECT * FROM obedience LIMIT 10;
          I do what I want.|Image 2
          Choose this option instead.|Image 4
          YOLO!|Image 1
          I do what I want.|Image 4
          the number 7|Image 3
          Choose this option instead.|Image 1
          7|Image 4
          the number 7|Image 3
          Choose this option instead.|Image 2
          the number 7|Image 4
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'ordered': False,
      'scored': True,
      'setup': r"""
      sqlite> .read lab13.sql
      """,
      'teardown': '',
      'type': 'sqlite'
    }
  ]
}
