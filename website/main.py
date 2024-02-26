from __init__ import create_app
from context_processors import delivery_info_context_processor

app = create_app()
app.context_processor(delivery_info_context_processor)



if __name__ == '__main__':
    app.run(debug=True)