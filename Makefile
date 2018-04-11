# Recruitment App Make file

help:
	@echo 'HELP!:'
	@echo 'There is no help at the moment'

setup_git_hooks:
	rm -f .git/hooks/pre-commit
	ln bin/pre-commit.sh .git/hooks/pre-commit
