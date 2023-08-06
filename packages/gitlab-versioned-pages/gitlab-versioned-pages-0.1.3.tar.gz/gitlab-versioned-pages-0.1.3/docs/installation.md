# Installation

## Stable release

To install `gitlab-versioned-pages`, run this command in your terminal:

```bash
conda install gitlab-versioned-pages -c ostrokach-forge
```

This is the preferred method to install `gitlab-versioned-pages`, as it will always install the most recent stable release.

If you don't have [conda] installed, this [Python installation guide] can guide
you through the process.

[conda]: https://conda.io
[Python installation guide]: https://conda.io/docs/user-guide/install/index.html

## From sources

The sources for `gitlab-versioned-pages` can be downloaded from the [GitLab repo].

You can either clone the public repository:

```bash
git clone git://gitlab.com/ostrokach/gitlab-versioned-pages
```

Or download the [tarball]:

```bash
curl -OL https://gitlab.com/ostrokach/gitlab-versioned-pages/repository/master/archive.tar
```

Once you have a copy of the source, you can install it with:

```bash
python setup.py install
```

[GitLab repo]: https://gitlab.com/ostrokach/gitlab-versioned-pages
[tarball]: https://gitlab.com/ostrokach/gitlab-versioned-pages/repository/master/archive.tar
