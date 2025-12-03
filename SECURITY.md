# Security Guidelines

## Credential Management

### DO ✅
- Keep your `.env` file locally only
- Use strong, unique API tokens
- Rotate tokens periodically
- Revoke tokens when leaving the project
- Use `.env.example` for documentation
- Report any credential leaks immediately

### DON'T ❌
- Commit `.env` files to git
- Share your personal tokens with others
- Hardcode credentials in source code
- Email or message credentials in plain text
- Screenshot files containing credentials
- Use the same token across multiple projects

## What to Do If Credentials Are Leaked

1. **Immediately revoke the exposed token** in the respective service (Jira/GitLab/Confluence)
2. **Generate a new token** and update your local `.env` file
3. **Notify your team lead** about the incident
4. **Check git history** - if committed, the repository may need to be cleaned

## Token Permissions

### Jira
- Minimum required: Read/Write access to projects

### GitLab
- Recommended scopes: `api`, `read_user`, `read_repository`, `write_repository`
- Avoid using tokens with `admin` scope unless necessary

### Confluence
- Minimum required: Read/Write access to spaces

## Regular Security Practices

- Review and rotate tokens every 90 days
- Use different tokens for different purposes
- Monitor access logs for unusual activity
- Keep your local machine secure (disk encryption, screen lock)

## Reporting Security Issues

If you discover a security vulnerability in this project, please report it to your team lead or security team immediately. Do not create public GitHub issues for security problems.
