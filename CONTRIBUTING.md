# Contributing to Planetary Hours Calculator

Thank you for considering contributing to the Planetary Hours Calculator! This document outlines how you can contribute to this project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How Can I Contribute?

### Reporting Bugs

- Check if the bug has already been reported in the Issues section
- Use the bug report template to create a new issue
- Provide detailed steps to reproduce the bug
- Include screenshots if applicable
- Describe what you expected to happen
- Describe what actually happened

### Suggesting Enhancements

- Check if the enhancement has already been suggested in the Issues section
- Use the feature request template to create a new issue
- Provide a clear description of the enhancement
- Explain why this enhancement would be useful

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements-local.txt
   ```
3. Configure the database:
   ```bash
   export DATABASE_URL=postgresql://username:password@localhost/planetary_hours
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Coding Guidelines

- Follow PEP 8 style guidelines for Python code
- Write meaningful commit messages
- Add comments to explain complex logic
- Test your changes thoroughly before submitting

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.