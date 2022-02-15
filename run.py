from hibike import app, db
import sys
if __name__ == '__main__':
    app.run(debug=True, port=sys.argv[1])
