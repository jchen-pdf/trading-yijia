from os import environ

SESSION_CONFIGS = [
    dict(
        name='otc_trading',
        display_name="OTC Market Experiment",
        app_sequence=['otc_trading'],
        num_demo_participants=4,
        treatment='OTC',
    ),
  #  dict(
  #      name='da_trading',
  #      display_name="Double Auction Market Experiment",
   #     app_sequence=['da_trading'],
   #     num_demo_participants=4,
    #    treatment='Double Auction',
  #  ),
   # dict(
    #    name='cm_trading',
     #   display_name="Call Market Experiment",
      #  app_sequence=['cm_trading'],
       # num_demo_participants=4,
      #  treatment='Call Market',
  #  ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.00,
    participation_fee=0.00,
    doc="",
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 Class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(
        name='live_demo',
        display_name='Live Demo Room',
    ),
]

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'your_secret_key_here'


