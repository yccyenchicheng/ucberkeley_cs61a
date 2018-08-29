test = {
  'name': 'matchmaker',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          sqlite> SELECT * FROM matchmaker LIMIT 10;
          dog|Kendrick Farmar|blue|white
          lion|Beets by Dre|blue|yellow
          dog|Tyler, the Cultivator|yellow|blue
          dolphin|The Roots|turquoise|purple
          dog|The Roots|yellow|grey
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
