# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.40.x  | :white_check_mark: |
| 0.39.x  | :white_check_mark: |
| < 0.39  | :x:                |

## Reporting a Vulnerability

We take the security of Cancrizans seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please Do Not

- **Do not** open a public GitHub issue for security vulnerabilities
- **Do not** discuss the vulnerability in public forums, chat rooms, or social media

### Please Do

1. **Email us directly** at: security@cancrizans-project.org (or open a private security advisory on GitHub)
2. **Provide detailed information** including:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)
3. **Allow time** for us to address the issue before public disclosure

## What to Expect

- **Acknowledgment**: We will acknowledge receipt of your vulnerability report within 48 hours
- **Updates**: We will send you regular updates about our progress
- **Timeline**: We aim to release a fix within 90 days of initial report
- **Credit**: If you wish, we will credit you in the security advisory and release notes

## Security Update Process

When we receive a security report:

1. **Confirmation**: We confirm the vulnerability and determine affected versions
2. **Fix Development**: We develop and test a fix in a private repository
3. **Advisory**: We prepare a security advisory with details and mitigation steps
4. **Release**: We release patched versions for all supported versions
5. **Disclosure**: We publish the security advisory

## Security Best Practices for Users

### When Using Cancrizans

1. **Keep Updated**: Always use the latest version
2. **Validate Input**: When processing MIDI/MusicXML files from untrusted sources:
   - Use `validate_import()` before processing
   - Set size limits on uploaded files
   - Run in sandboxed environments for untrusted files
3. **Dependencies**: Keep all dependencies updated
4. **Permissions**: Run with minimal required permissions

### File Handling

```python
from cancrizans import load_score, validate_import
from pathlib import Path

# Validate before loading untrusted files
file_path = Path("untrusted.mid")

# Check file size
if file_path.stat().st_size > 10 * 1024 * 1024:  # 10MB limit
    raise ValueError("File too large")

# Validate structure
if not validate_import(file_path):
    raise ValueError("Invalid file structure")

# Now safe to load
score = load_score(file_path)
```

### Known Security Considerations

1. **MIDI/MusicXML Parsing**
   - music21 is used for parsing music files
   - Large or malformed files may consume excessive memory
   - Always validate file size and structure

2. **LilyPond Integration**
   - LilyPond output may execute system commands
   - Only render LilyPond from trusted sources
   - Use sandboxed environments for untrusted content

3. **Audio Synthesis**
   - FluidSynth integration requires system resources
   - May be subject to denial-of-service via resource exhaustion
   - Set appropriate resource limits

4. **Python Code Execution**
   - Never execute user-provided Python code
   - Validate all input parameters
   - Use type hints and runtime validation

## Security Scanning

We use the following tools to scan for vulnerabilities:

- **Bandit**: Python security linter
- **Safety**: Dependency vulnerability scanner
- **Ruff**: Code quality and security checks
- **Dependabot**: Automated dependency updates
- **CodeQL**: Semantic code analysis (GitHub)

Run security scans locally:

```bash
# Install security tools
pip install bandit safety

# Run Bandit security scanner
bandit -r cancrizans -f json -o bandit-report.json

# Check for vulnerable dependencies
safety check --json

# Check code quality
ruff check cancrizans
```

## Security-Related Configuration

### Dependency Management

We pin dependencies in `pyproject.toml` with minimum versions to ensure security updates are applied.

### CI/CD Security

- All secrets are stored in GitHub Secrets
- No credentials are logged in CI output
- Security scans run on every PR
- Failed security checks block merges

## Disclosure Policy

- **Private Disclosure Period**: 90 days from initial report
- **Public Disclosure**: After patch is released or 90 days (whichever comes first)
- **CVE Assignment**: We will request a CVE for significant vulnerabilities
- **Credits**: Security researchers will be credited unless they prefer anonymity

## Contact

- **Security Issues**: security@cancrizans-project.org
- **General Issues**: https://github.com/cancrizans-project/cancrizans-prototype/issues
- **Discussions**: https://github.com/cancrizans-project/cancrizans-prototype/discussions

## Hall of Thanks

We thank the following security researchers for responsibly disclosing vulnerabilities:

<!-- This section will be updated as we receive and address security reports -->

---

**Last Updated**: 2025-01-18
**Version**: 1.0
