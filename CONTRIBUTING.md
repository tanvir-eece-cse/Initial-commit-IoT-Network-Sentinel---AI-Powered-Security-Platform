# Contributing to IoT Network Sentinel

First off, thank you for considering contributing to IoT Network Sentinel! It's people like you that make this project such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible.
* **Provide specific examples to demonstrate the steps**.
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**
* **Include screenshots and animated GIFs** if possible.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. Create an issue and provide the following information:

* **Use a clear and descriptive title** for the issue to identify the suggestion.
* **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
* **Provide specific examples to demonstrate the steps**.
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
* **Explain why this enhancement would be useful** to most users.

### Pull Requests

Please follow these steps to have your contribution considered by the maintainers:

1. Follow all instructions in the template
2. Follow the [styleguides](#styleguides)
3. After you submit your pull request, verify that all status checks are passing

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker and Docker Compose
- Git

### Setting Up Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/tanvir-eece-cse/iot-network-sentinel.git
   cd iot-network-sentinel
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up the ML service**
   ```bash
   cd ../ml-service
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Set up the frontend**
   ```bash
   cd ../frontend
   npm install
   ```

5. **Start with Docker Compose**
   ```bash
   cd ..
   docker-compose up -d
   ```

### Running Tests

**Backend:**
```bash
cd backend
pytest --cov=app -v
```

**ML Service:**
```bash
cd ml-service
pytest --cov=app -v
```

**Frontend:**
```bash
cd frontend
npm run test
```

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Consider starting the commit message with an applicable emoji:
    * 🎨 `:art:` when improving the format/structure of the code
    * 🐎 `:racehorse:` when improving performance
    * 🚱 `:non-potable_water:` when plugging memory leaks
    * 📝 `:memo:` when writing docs
    * 🐛 `:bug:` when fixing a bug
    * 🔥 `:fire:` when removing code or files
    * 💚 `:green_heart:` when fixing the CI build
    * ✅ `:white_check_mark:` when adding tests
    * 🔒 `:lock:` when dealing with security
    * ⬆️ `:arrow_up:` when upgrading dependencies
    * ⬇️ `:arrow_down:` when downgrading dependencies

### Python Styleguide

* Follow [PEP 8](https://pep8.org/)
* Use [Black](https://black.readthedocs.io/) for code formatting
* Use [Ruff](https://docs.astral.sh/ruff/) for linting
* Use type hints for all function parameters and return values
* Write docstrings for all public functions and classes

### TypeScript/React Styleguide

* Use TypeScript for all new code
* Follow the [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
* Use functional components with hooks
* Use TailwindCSS for styling
* Write meaningful component names

### Documentation Styleguide

* Use [Markdown](https://guides.github.com/features/mastering-markdown/)
* Reference functions and classes in backticks: \`functionName()\`
* Include code examples where helpful

## Security

If you discover a security vulnerability, please send an email to tanvir.eece.mist@gmail.com instead of opening a public issue.

## Questions?

Feel free to reach out:
- **Email:** tanvir.eece.mist@gmail.com
- **LinkedIn:** [tanvir-eece](https://www.linkedin.com/in/tanvir-eece/)
- **GitHub:** [tanvir-eece-cse](https://github.com/tanvir-eece-cse)

Thank you for contributing! 🙏
