test = {
  'name': 'lets-count',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          sqlite> SELECT * from sp17favnum;
          7|25
          sqlite> SELECT * from sp17favpets;
          dragon|20
          dog|14
          cat|8
          unicorn|7
          n/a|6
          panda|5
          dolphin|4
          tiger|4
          7|3
          bear|3
          sqlite> SELECT * from su17favpets;
          dog|10
          lion|5
          cat|3
          dolphin|3
          dragon|3
          tiger|3
          panda|2
          penguin|2
          a bird|1
          a dog|1
          sqlite> SELECT * from su17dog;
          dog|10
          sqlite> SELECT * from su17alldogs;
          doggo|12
          sqlite> SELECT * from obedienceimage;
          7|Image 1|15
          7|Image 2|3
          7|Image 3|5
          7|Image 4|7
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
