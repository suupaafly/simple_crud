import uvicorn

if __name__ == '__main__':
    import main
    uvicorn.run(main.app, host='0.0.0.0', port=8000)
