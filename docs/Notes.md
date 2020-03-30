# Developer Notes

## File and directory permissions

Use this command to set file and directory permissions on files before pushing to github.

```bash
find . -type d -exec chmod 0750 {} \; && find . -type f -exec chmod 0640 {} \;
```

Use this command to rsync project files from host to guest for QA testing

```bash
rsync -avz ~/ansible/cte/ cte:~/ansible/cte/
```
