git; Mirror Upstream to Local to Downstream (muld)
==================================================

.. image:: https://img.shields.io/pypi/v/muld.svg
   :target: https://pypi.org/project/muld
   :alt: PyPI

If you use git submodules, then you might have faced the issue that a user of
your project does not have access to the remotes that your submodules point to.

You can then provide a full source-tarball to them instead, however, that is
not always ideal. Sometimes, other infrastructure such as GitLAB, or BitBucket
can provide automatic mirroring your third-party dependencies but if they
cannot access that either, well then that is not really a solution either.

So, one might need to manually maintain some **downstream** mirrors, based on
the actual **upstream** repositories. This is an annoyingly manual tasks,
however, this command ``muld`` takes most of the heavy lifting out of it, such
that you only have to fix issues when mirroring for some reason fails, but it
will otherwise run happily in a cron-job.

**NOTE**, what ``muld`` does, could probably be done with 10 lines of Bash.
But, using Python for the task is 1000 times more fun. Also, ``muld`` does
plain ``git clone``, does not use ``--bare``, ``--mirror`` or ``--recursive``.

Usage
-----

Provide a list of repository upstream/downstream pairs such as::

  repos:
    - name: "spdk"
      upstream: "https://github.com/spdk/spdk"
      downstream: "ssh://git@example.com/somewhere/else/spdk.git"
    - name: "dpdk"
      upstream: "https://github.com/spdk/dpdk.git"
      downstream: "ssh://git@example.com/somewhere/else/dpdk.git"

In a file and name it as e.g. ``muld.yml``. Then invoke ``muld``::

  muld --mirrors $HOME/mirrors --conf muld.yml

Behaviour
---------

It will initially clone the **upstream** repository, when it exists then just
fetch and prune. Regardless, after it will then push tags and branches to
**downstream**.

If ``--conf`` is not given, then it assumes that a file named ``muld.yml``
exists inside the directory pointed to by ``--mirrors``.

If ``--mirrors`` is not given, then it uses the current-working-directory.

Thus, in case you have prepared a home for mirrors with a config inside it, for
example like so::

  # Setup
  mkdir $HOME/mirrors
  echo "repos: [{upstream: 'https://github.com/spdk/spdk'}]" > muld.yml
  cd $HOME/mirrors

Then you can just go to the directory and run ``muld``::

  # Run it...
  cd $HOME/mirrors
  muld

Regarding the config-file, only ``upstream`` is required. When ``name`` is left
out, then ``muld`` will produce a named based on the given ``upstream`` URL.

If ``downstream`` is left out, then it simply won't push anywhere, it will just
clone, prune and fetch.
