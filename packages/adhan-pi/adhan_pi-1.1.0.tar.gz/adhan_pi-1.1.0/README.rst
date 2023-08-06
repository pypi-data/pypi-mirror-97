adhan-pi
=======================


Developing
----------

.. -code-begin-

.. code-block:: bash

   >>> sudo dnf install ffmpeg # install ffmpeg on your system (if not installed)
   >>> sudo ln -s ~/adhan-pi /opt/adhan-pi
   >>> python3 -m venv /opt/adhan-pi/env
   >>> source /opt/adhan-pi/env/bin/activate
   >>> cd /opt/adhan-pi
   >>> pip install -e '.[dev]'
   >>> tox -e lint && tox


Setting up Cron env
-------------------

   >>> source /opt/adhan-pi/env/bin/activate
   >>> pip install -e '.[cron]'


Setting up Cron
---------------

Add this to your cronjob (with your user) (crontab -e)

    @daily /opt/adhan-pi/env/bin/schedule_prayer_cron --query "New York, NY" --user salah

set up crons manually

   >>> source /opt/adhan-pi/env/bin/activate
   >>> /opt/adhan-pi/env/bin/schedule_prayer_cron --query "New York, NY" --user salah
