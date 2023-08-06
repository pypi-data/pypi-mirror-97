# Delphix Integration CLI and Library (dxi)
dxi is a solution from Delphix, 
built to facilitate simpler and seamless integration of Delphix Platform Operations into your existing workflows. 
dxi offers a feature rich command line interface (cli) for users who prefer to use their terminals or shell scripts to trigger data operations. 
dxi is also a Python Library and can be used by those who need to control their data through code or integrate data operations into their existing applications.
​

## What is Delphix? 
Delphix is a platform that provides you with the ability to securely copy and share datasets. 
Using virtualization, you will ingest your data sources and create any number of virtual data copies, 
which are full read-write capable database instances that use an infinitesimally small fraction of the 
resources that normal database copy would require. ​

Learn mode about [Delphix](http://www.delphix.com)

## Where can I get dxi?
dxi is currently available as a controlled distribution from Delphix via our download portal. 
If you are an existing Delphix customer, reach out to your out to your Delphix POC for a download link.
​

## How do I learn more about dxi? 
For a detailed dxi documentation, visit [Delphix Integrations](https://integrations.delphix.com/)
​

## <a id="contribute"></a>Contribute
​
We have decided to keep this project internal for a brief period of time, and hence, we are not accepting any '
external contributions.
We look forward to changing that in the near future and build together as a community.
​


### Formatting
​
This repository uses the `tox` and `pre-commit` tools to run
autoformatters on the entire repository. These two tools are the
industry standard for Python. 
The goal of these formatters is to
delegate issues of formatting to the machine so that develeopers and
code-reviewers can focus on more important things.
​
The two main autoformatters that we use are
 - `black`: General Python formatting
 - `isort`: Import sorting
​
## Running the formatting
​
The formatting is automatically run remotely on every Github pull
request and on every push to Github.
​
It is possible to run these locally in two ways. Automatically before
every push and manually.
​
To have the checks run automatically before every push you can enable
`pre-commit`.
​
```
tox
.tox/format/bin/pre-commit install --hook-type pre-push
```
​
To run the checks manually:
On the entire repository
```
	tox -- --all-files
```
on a specific file
```
	tox -- --file <file-name>
```
On every file in the most recent commit
```
    git diff-tree --no-commit-id --name-only -r HEAD | xargs tox -- --files
```
​