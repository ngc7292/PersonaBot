from src.demo_main_control.main_control import MainControl
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os
import asyncio



# Create a Web Server
# using Flask instance and specify the template and static folder locations
#app = Flask(__name__, template_folder='web_server/templates', static_folder='web_server/static')
template_dir = os.path.abspath('web_server/templates')
static_dir = os.path.abspath('web_server/static')
print(f"Template directory: {template_dir}")
print(f"Static directory: {static_dir}")
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


# Create Robot Control Logic
socketio = SocketIO(app)
main_control = MainControl()




@app.route('/')
def index():
    return render_template('index.html')


# Link Robot Control with Web GUI
@socketio.on('command')
def handle_command(data):
    command = data.get('command')
    button_id = data.get('buttonId')
    print(f"Received command: {command}, from button: {button_id}")
    #socketio.start_background_task(main_control.state_control.handle_command, command)
    asyncio.run(main_control.state_control.handle_command(command))



if __name__ == '__main__':
    try:
        socketio.start_background_task(main_control.run)
        socketio.run(app, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
    finally:
        main_control.shutdown()