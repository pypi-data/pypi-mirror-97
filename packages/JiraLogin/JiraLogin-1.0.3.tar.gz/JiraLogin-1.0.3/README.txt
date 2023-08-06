===========
Jira Login
===========

Jira Login provides an easy solution for signing into Jira as it stores and references local credentials for each instance accessed. Note that stored passwords are encoded for obfuscation purposes, but should not be considered to be highly secure. Stored credentials will be used until an unauthorized response is received from Jira. From here, you'll need to re-enter your credentials which will be stored once again for future use.

Reference the Python Jira library documentation for usage after using Jira Login to sign in - https://jira.readthedocs.io/en/master/

Typical usage often looks like this::

    from jiralogin import JiraLogin

    jl = JiraLogin.JiraLogin(r'<Link to your Jira server>')
    jira = jl.login()
	issue = jira.search_issues(jql_str='key = PROJECT-1000', json_result=True, fields='key, summary')
	print(issue)