test = {
  'name': 'What Would Scheme Display?',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (cons 1 2)
          (1 . 2)
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (cons 1 (cons 2 nil))
          (1 2)
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (car (cons 1 (cons 2 nil)))
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (cdr (cons 1 (cons 2 nil)))
          (2)
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (list 1 2 3)
          (1 2 3)
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (list 1 (cons 2 3))
          (1 (2 . 3))
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> '(1 2 3)
          (1 2 3)
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> '(2 . 3)
          (2 . 3)
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> '(2 . (3))               ; Recall dot notation rule
          (2 3)
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (eq? '(1 . (2 . 3)) (cons 1 (cons 2 (cons 3 nil))))
          False
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (eq? '(1 . (2 . 3)) (cons 1 (cons 2 3)))
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (eq? '(1 . (2 . 3)) (list 1 (cons 2 3)))
          False
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (cons 1 '(list 2 3))     ; Recall quoting
          (1 list 2 3)
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      
      """,
      'teardown': '',
      'type': 'scheme'
    }
  ]
}
