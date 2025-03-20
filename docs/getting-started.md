# Getting Started with Financial Analysis System

## Prerequisites
- Python 3.8 or higher
- Git
- Web browser (Chrome, Firefox, or Edge recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fas-v2-0.git
cd fas-v2-0
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

2. Update the environment variables in `.env`:
```env
DEBUG=True
SECRET_KEY=your-secret-key
API_KEY=your-api-key
```

## Running the Application

1. Start the application:
```bash
cd ai-data-tool/frontend
streamlit run app.py
```

2. Open your web browser and navigate to:
```
http://localhost:8501
```

## First Steps

1. Upload a financial dataset (CSV or Excel format)
2. Explore the data visualization options
3. Try the AI-powered analysis features
4. Check the console for any warnings or errors

## Troubleshooting

If you encounter any issues:
1. Check the logs in `docs/logs/console/`
2. Review the FAQ in `docs/faq.md`
3. Search existing issues on GitHub
4. Create a new issue if needed

## Next Steps
- Read the [Usage Guide](usage.md) for detailed features
- Review the [API Reference](api-reference.md)
- Check out the [Contributing Guidelines](CONTRIBUTING.md)

## Support
For additional help:
- Join our community forum
- Check the [FAQ](faq.md)
- Contact support@fas-v2-0.com 