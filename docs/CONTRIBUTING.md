# Contributing to Financial Analysis System

## Getting Started
1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/fas-v2-0.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`

## Development Setup
1. Install Python 3.8 or higher
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Coding Standards
- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Write docstrings for all functions and classes
- Include type hints where appropriate
- Keep functions focused and under 50 lines
- Maintain test coverage above 80%

## Documentation
- Update documentation for any new features or changes
- Follow the documentation protocol in `.cursor/rules/protocols/documentation.mdc`
- Keep `__ai__.md` and `_change.logs` up to date in each folder
- Add examples and use cases for new features

## Testing
- Write unit tests for new features
- Update existing tests when modifying code
- Follow the testing protocol in `.cursor/rules/protocols/testing.mdc`
- Run the full test suite before submitting changes

## Pull Request Process
1. Update documentation and tests
2. Run linters and formatters
3. Create a pull request with a clear description
4. Reference any related issues
5. Wait for code review and address feedback

## Commit Messages
- Use clear, descriptive commit messages
- Follow the format: `type(scope): description`
- Types: feat, fix, docs, style, refactor, test, chore
- Example: `feat(data-processing): add support for CSV imports`

## Questions or Issues?
- Check the [FAQ](faq.md)
- Review existing issues before creating new ones
- Join our developer community for support

Thank you for contributing to the Financial Analysis System! 