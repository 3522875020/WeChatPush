from itchat.config import (BLOCK_NAME, MES_THROUGH, LOG_LEVEL, 
                           DINGTALK_APP_KEY, DINGTALK_APP_SECRET,
                           DINGTALK_ROBOT_CODE, DINGTALK_OPEN_CONVERSATION_ID)
import requests
import json
import logging

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class farpush:
    def __init__(self):
        self.block = BLOCK_NAME
        self.through = MES_THROUGH
        self.robot_code = DINGTALK_ROBOT_CODE
        self.open_conversation_id = DINGTALK_OPEN_CONVERSATION_ID
        self.access_token = self._get_access_token()
        logger.debug(f"Initialized with access_token: {self.access_token}")

    def _get_access_token(self):
        url = "https://oapi.dingtalk.com/gettoken"
        params = {
            "appkey": DINGTALK_APP_KEY,
            "appsecret": DINGTALK_APP_SECRET
        }
        logger.debug(f"Getting access token with params: {params}")
        response = requests.get(url, params=params)
        if response.status_code == 200:
            token = response.json().get("access_token")
            logger.info(f"Successfully obtained access token: {token[:10]}...")
            return token
        else:
            logger.error(f"Failed to get access token: {response.status_code} {response.text}")
            return None

    def push(self, sender, content):
        return self.push_text(sender, content)

    def push_text(self, sender, content):
        for check in self.block:
            if check in content:
                logger.info(f"Message blocked: {content}")
                return
        
        # 查找第一个冒号的位置
        colon_index = content.find(':')
        
        if colon_index != -1:
            # 如果找到冒号，分别提取title和content
            title = content[:colon_index].strip()
            content = content[colon_index + 1:].strip()
        else:
            # 如果没有找到冒号，使用发送者名称作为title
            title = sender
            content = content.strip()
        
        msg_param = json.dumps({
            "content": f"\"title\" : \"{title}\"\n\"content\" : \"{content}\""
        })
        self._send_to_dingtalk(msg_param, "sampleText")

    def _send_to_dingtalk(self, msg_param, msg_key):
        url = "https://api.dingtalk.com/v1.0/robot/groupMessages/send"
        headers = {
            'x-acs-dingtalk-access-token': self.access_token,
            'Content-Type': 'application/json;charset=utf-8'
        }
        data = {
            "robotCode": self.robot_code,
            "msgKey": msg_key,
            "msgParam": msg_param,
            "openConversationId": self.open_conversation_id
        }
        
        try:
            logger.debug(f"Sending message to DingTalk: URL={url}, Headers={headers}, Data={json.dumps(data)}")
            r = requests.post(url, headers=headers, json=data)
            logger.debug(f"Response status code: {r.status_code}")
            logger.debug(f"Response content: {r.text}")
            r.raise_for_status()
            response_data = r.json()
            if 'processQueryKey' in response_data:
                logger.info(f"Message sent to DingTalk successfully. ProcessQueryKey: {response_data['processQueryKey']}")
            else:
                logger.error(f"Unexpected response from DingTalk: {response_data}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send message to DingTalk: {e}")
            logger.error(f"Response content: {e.response.text if e.response else 'No response'}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode response from DingTalk: {e}")
