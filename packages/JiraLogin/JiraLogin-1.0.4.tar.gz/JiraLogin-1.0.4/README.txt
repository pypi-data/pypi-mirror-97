===========
JiraLogin
===========

JiraLogin provides an easy solution for signing into Jira as it stores and references local credentials for each instance accessed. Note that stored passwords are encoded for obfuscation purposes, but should not be considered to be highly secure. Stored credentials will be used until an unauthorized response is received from Jira. From here, you'll need to re-enter your credentials which will be stored once again for future use.

Reference the Python Jira library documentation for usage after using JiraLogin to sign in - https://jira.readthedocs.io/en/master/

Typical usage often looks like this::

    from jiralogin import JiraLogin

	jira = JiraLogin.JiraLogin(r'https://issues.pokemon.com').login()
	issues = jira.search_issues(jql_str='Project = MyProject', fields='key, summary')
	for i in issues:
		print(i.key)