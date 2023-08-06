#!/usr/bin/env python

import sys

import radical.saga  as rs
import radical.utils as ru


# ------------------------------------------------------------------------------
#
def main():

    js  = None
    rep = ru.Reporter('radical.saga.test')

    try:
        js   = rs.job.Service('noop://localhost')
        jobs = list()
        n    = 1024 * 4

        rep.progress_tgt(n, label='submit')
        for i in range(n):
            jobs.append(js.run_job('sleep 2'))
            rep.progress()
        rep.progress_done()

        rep.progress_tgt(n, label='wait')
        for job in jobs:
            job.wait()
            rep.progress()
        rep.progress_done()


    finally:
        if js:
            js.close()


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    sys.exit (main())


# ------------------------------------------------------------------------------

