# main.py
from app import app
from layout import serve_layout
import callbacks  # This registers the callbacks

app.layout = serve_layout()

if __name__ == '__main__':
    app.run_server(debug=True)
