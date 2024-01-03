import application

app = application.web

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='run:app', host="0.0.0.0", log_level='debug', port=8000)
