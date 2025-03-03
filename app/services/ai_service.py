"""
AI service for analyzing WeChat messages using OpenAI GPT.
"""
import logging
import datetime
import json
from typing import List, Dict, Any, Optional
import openai

import config as cfg
from app.services.message_service import MessageService

logger = logging.getLogger(__name__)

class AiService:
    """Service for AI-powered message analysis and summarization."""
    
    def __init__(self):
        """Initialize the AI service."""
        # Configure OpenAI
        openai.api_key = cfg.OPENAI_API_KEY
        
        # Initialize message service for storing results
        self.message_service = MessageService()
    
    async def analyze_messages(self, messages: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Analyze a list of messages using AI.
        
        Args:
            messages: List of message dictionaries to analyze
            
        Returns:
            Dictionary containing analysis results or None if analysis failed
        """
        if not messages:
            logger.warning("No messages to analyze")
            return None
        
        try:
            # Group messages by room
            room_messages = {}
            for msg in messages:
                room_id = msg.get('room_id')
                if room_id not in room_messages:
                    room_messages[room_id] = []
                room_messages[room_id].append(msg)
            
            # Analyze each room's messages
            results = {}
            for room_id, msgs in room_messages.items():
                if len(msgs) > 5:  # Only analyze rooms with sufficient messages
                    room_result = await self._analyze_room_messages(room_id, msgs)
                    if room_result:
                        results[room_id] = room_result
            
            return results
            
        except Exception as e:
            logger.error(f"Error analyzing messages: {e}", exc_info=True)
            return None
    
    async def _analyze_room_messages(self, room_id: str, 
                                  messages: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Analyze messages from a specific room.
        
        Args:
            room_id: The ID of the room/group
            messages: List of message dictionaries from the room
            
        Returns:
            Dictionary containing analysis results or None if analysis failed
        """
        try:
            # Sort messages by timestamp
            sorted_messages = sorted(
                messages, 
                key=lambda x: datetime.datetime.fromisoformat(x.get('created_at', ''))
            )
            
            if not sorted_messages:
                return None
            
            # Get room information
            room_topic = sorted_messages[0].get('room_topic', 'Unknown Group')
            
            # Prepare messages for GPT processing
            conversation = []
            for msg in sorted_messages:
                user_name = msg.get('user_name', 'Unknown')
                content = msg.get('content', '')
                
                if content and content.strip():
                    conversation.append(f"{user_name}: {content}")
            
            # Skip if no valid messages
            if not conversation:
                return None
            
            # Get time range
            start_time = datetime.datetime.fromisoformat(sorted_messages[0].get('created_at', ''))
            end_time = datetime.datetime.fromisoformat(sorted_messages[-1].get('created_at', ''))
            
            # Generate summary using GPT
            summary = await self._generate_summary(room_topic, conversation)
            
            # Extract keywords
            keywords = await self._extract_keywords(conversation)
            
            # Store summary in database
            if summary:
                self.message_service.store_message_summary(
                    room_id=room_id,
                    summary=summary,
                    start_time=start_time,
                    end_time=end_time
                )
            
            # Return analysis results
            return {
                'room_id': room_id,
                'room_topic': room_topic,
                'summary': summary,
                'keywords': keywords,
                'message_count': len(messages),
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing room messages: {e}", exc_info=True)
            return None
    
    async def _generate_summary(self, room_topic: str, 
                             conversation: List[str]) -> Optional[str]:
        """
        Generate a summary of the conversation using GPT.
        
        Args:
            room_topic: The topic/name of the room
            conversation: List of formatted message strings
            
        Returns:
            Summary text or None if generation failed
        """
        try:
            # Limit conversation length to avoid token limits
            if len(conversation) > 100:
                # Take beginning, middle, and end of conversation
                start = conversation[:30]
                middle = conversation[len(conversation)//2-15:len(conversation)//2+15]
                end = conversation[-30:]
                conversation = start + ['...'] + middle + ['...'] + end
            
            # Combine messages into a single text
            conversation_text = "\n".join(conversation)
            
            # Create prompt for GPT
            prompt = f"""
            The following is a conversation from a WeChat group named "{room_topic}".
            
            {conversation_text}
            
            Please provide a concise summary of the key points and important information 
            shared in this conversation. Focus on:
            1. Main topics discussed
            2. Key questions and answers
            3. Important information, links, or resources shared
            4. Action items or decisions made (if any)
            
            Format your summary in bullet points where appropriate.
            """
            
            # Call GPT API
            response = await openai.Completion.acreate(
                engine=cfg.OPENAI_MODEL,
                prompt=prompt,
                max_tokens=500,
                temperature=0.5,
                top_p=0.95
            )
            
            # Extract summary from response
            summary = response.choices[0].text.strip()
            
            logger.info(f"Generated summary for {room_topic} ({len(conversation)} messages)")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}", exc_info=True)
            return None
    
    async def _extract_keywords(self, conversation: List[str]) -> List[str]:
        """
        Extract keywords from the conversation using GPT.
        
        Args:
            conversation: List of formatted message strings
            
        Returns:
            List of keywords or empty list if extraction failed
        """
        try:
            # Combine messages into a single text
            conversation_text = "\n".join(conversation)
            
            # Create prompt for GPT
            prompt = f"""
            Extract 5-10 key topics or keywords from this conversation:
            
            {conversation_text}
            
            Return only the keywords as a JSON array of strings.
            """
            
            # Call GPT API
            response = await openai.Completion.acreate(
                engine=cfg.OPENAI_MODEL,
                prompt=prompt,
                max_tokens=200,
                temperature=0.3,
                top_p=0.95
            )
            
            # Extract keywords from response
            keywords_text = response.choices[0].text.strip()
            
            # Try to parse as JSON
            try:
                # Find JSON array in response
                start_idx = keywords_text.find('[')
                end_idx = keywords_text.rfind(']') + 1
                
                if start_idx >= 0 and end_idx > start_idx:
                    json_text = keywords_text[start_idx:end_idx]
                    keywords = json.loads(json_text)
                    return keywords
                else:
                    # Fallback: split by commas or newlines
                    return [k.strip() for k in keywords_text.replace('\n', ',').split(',') if k.strip()]
            except:
                # If JSON parsing fails, just split by commas or newlines
                return [k.strip() for k in keywords_text.replace('\n', ',').split(',') if k.strip()]
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}", exc_info=True)
            return [] 