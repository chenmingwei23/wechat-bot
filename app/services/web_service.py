"""
Web service for the WeChat Group Chat Assistant, providing a web interface for users.
"""
import os
import logging
import threading
from flask import Flask, render_template, jsonify, request, Response
from flask_cors import CORS

import config as cfg
from app.services.message_service import MessageService

logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(
    __name__, 
    template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
    static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
)
CORS(app)

# Initialize services
message_service = MessageService()

@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html')

@app.route('/api/rooms')
def get_rooms():
    """API endpoint to get list of rooms/groups."""
    try:
        # Create a database session
        session = message_service.Session()
        
        # Query rooms from database
        from app.models.database import Room
        rooms = session.query(Room).all()
        
        # Convert to list of dictionaries
        room_list = []
        for room in rooms:
            room_list.append({
                'id': room.room_id,
                'topic': room.topic,
                'created_at': room.created_at.isoformat()
            })
        
        return jsonify({
            'success': True,
            'data': room_list
        })
    except Exception as e:
        logger.error(f"Error retrieving rooms: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        if session:
            session.close()

@app.route('/api/messages')
def get_messages():
    """API endpoint to get messages, optionally filtered by room."""
    try:
        room_id = request.args.get('room_id')
        limit = request.args.get('limit', 100, type=int)
        
        # Get messages from service
        messages = message_service.get_recent_messages(
            room_id=room_id,
            limit=limit
        )
        
        return jsonify({
            'success': True,
            'data': messages
        })
    except Exception as e:
        logger.error(f"Error retrieving messages: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/summaries')
def get_summaries():
    """API endpoint to get message summaries, optionally filtered by room."""
    try:
        room_id = request.args.get('room_id')
        limit = request.args.get('limit', 10, type=int)
        
        # Get summaries from service
        summaries = message_service.get_message_summaries(
            room_id=room_id,
            limit=limit
        )
        
        return jsonify({
            'success': True,
            'data': summaries
        })
    except Exception as e:
        logger.error(f"Error retrieving summaries: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/status')
def get_status():
    """API endpoint to get system status."""
    try:
        # Create a database session
        session = message_service.Session()
        
        # Get count of messages, rooms, and users
        from app.models.database import Message, Room, User, MessageSummary
        message_count = session.query(Message).count()
        room_count = session.query(Room).count()
        user_count = session.query(User).count()
        summary_count = session.query(MessageSummary).count()
        
        return jsonify({
            'success': True,
            'data': {
                'message_count': message_count,
                'room_count': room_count,
                'user_count': user_count,
                'summary_count': summary_count,
                'status': 'running'
            }
        })
    except Exception as e:
        logger.error(f"Error retrieving status: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        if session:
            session.close()

def start_web_server():
    """Start the web server in a separate thread."""
    def run_server():
        logger.info(f"Starting web server at {cfg.WEB_HOST}:{cfg.WEB_PORT}")
        app.run(
            host=cfg.WEB_HOST,
            port=cfg.WEB_PORT,
            debug=cfg.DEBUG,
            use_reloader=False  # Disable reloader when running in a thread
        )
    
    # Start server in a thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    return server_thread 