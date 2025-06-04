import base64
import json
import asyncio
import time
import os
import websockets
from loguru import logger
from dotenv import load_dotenv
from XianyuApis import XianyuApis
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


from utils.xianyu_utils import generate_mid, generate_uuid, trans_cookies, generate_device_id, decrypt
from XianyuAgent import XianyuReplyBot
from context_manager import ChatContextManager


class EnvChangeHandler(FileSystemEventHandler):
    def __init__(self, xianyu_instance):
        self.xianyu_instance = xianyu_instance
        
    def on_modified(self, event):
        if event.src_path.endswith('.env'):
            print("检测到.env文件变化，重新加载cookie")
            # 重新加载dotenv
            load_dotenv(override=True)
            # 更新cookie
            new_cookies = os.getenv("COOKIES_STR")
            if new_cookies and new_cookies != self.xianyu_instance.cookies_str:
                self.xianyu_instance.cookies_str = new_cookies
                self.xianyu_instance.cookies = trans_cookies(new_cookies)
                print("Cookie已更新")


class KnowledgeBaseChangeHandler(FileSystemEventHandler):
    """监控知识库文件变化的处理器"""
    def __init__(self, bot_instance):
        self.bot_instance = bot_instance
        self.knowledge_file = os.path.join("prompts", "cursor_knowledge_base.txt")
        
    def on_modified(self, event):
        # 检查是否是目标文件
        if event.src_path.replace('\\', '/').endswith(self.knowledge_file.replace('\\', '/')):
            logger.info(f"检测到知识库文件变化: {event.src_path}")
            try:
                # 直接重新加载所有Agent的知识库
                for agent_name in ['price', 'tech', 'default']:
                    if agent_name in self.bot_instance.agents:
                        agent = self.bot_instance.agents[agent_name]
                        old_length = len(agent.cursor_knowledge) if hasattr(agent, 'cursor_knowledge') else 0
                        # 重新加载知识库
                        agent.cursor_knowledge = agent._load_cursor_knowledge()
                        new_length = len(agent.cursor_knowledge) if hasattr(agent, 'cursor_knowledge') else 0
                        logger.info(f"{agent_name.capitalize()}Agent知识库已重新加载: {old_length} -> {new_length} 字符")
                logger.info("所有Agent的知识库已成功重新加载")
            except Exception as e:
                logger.error(f"重新加载知识库时出错: {e}")


class XianyuLive:
    def __init__(self, cookies_str):
        self.xianyu = XianyuApis()
        self.base_url = 'wss://wss-goofish.dingtalk.com/'
        self.cookies_str = cookies_str
        self.cookies = trans_cookies(cookies_str)
        self.myid = self.cookies['unb']
        self.device_id = generate_device_id(self.myid)
        self.context_manager = ChatContextManager()
        # 创建回复机器人实例
        self.reply_bot = XianyuReplyBot()
        
        # 心跳相关配置
        self.heartbeat_interval = 15  # 心跳间隔15秒
        self.heartbeat_timeout = 5    # 心跳超时5秒
        self.last_heartbeat_time = 0
        self.last_heartbeat_response = 0
        self.heartbeat_task = None
        self.ws = None

        # 在XianyuLive实例创建后添加
        observer = Observer()
        # 监控.env文件变化
        env_handler = EnvChangeHandler(self)
        observer.schedule(env_handler, path='.', recursive=False)
        
        # 监控知识库文件变化
        knowledge_handler = KnowledgeBaseChangeHandler(self.reply_bot)
        observer.schedule(knowledge_handler, path='prompts', recursive=False)
        
        observer.start()
        logger.info("文件监控系统已启动: .env和知识库文件的变化将自动检测")

    async def send_msg(self, ws, cid, toid, text):
        text = {
            "contentType": 1,
            "text": {
                "text": text
            }
        }
        text_base64 = str(base64.b64encode(json.dumps(text).encode('utf-8')), 'utf-8')
        msg = {
            "lwp": "/r/MessageSend/sendByReceiverScope",
            "headers": {
                "mid": generate_mid()
            },
            "body": [
                {
                    "uuid": generate_uuid(),
                    "cid": f"{cid}@goofish",
                    "conversationType": 1,
                    "content": {
                        "contentType": 101,
                        "custom": {
                            "type": 1,
                            "data": text_base64
                        }
                    },
                    "redPointPolicy": 0,
                    "extension": {
                        "extJson": "{}"
                    },
                    "ctx": {
                        "appVersion": "1.0",
                        "platform": "web"
                    },
                    "mtags": {},
                    "msgReadStatusSetting": 1
                },
                {
                    "actualReceivers": [
                        f"{toid}@goofish",
                        f"{self.myid}@goofish"
                    ]
                }
            ]
        }
        await ws.send(json.dumps(msg))

    async def init(self, ws):
        token = self.xianyu.get_token(self.cookies, self.device_id)['data']['accessToken']
        msg = {
            "lwp": "/reg",
            "headers": {
                "cache-header": "app-key token ua wv",
                "app-key": "444e9908a51d1cb236a27862abc769c9",
                "token": token,
                "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 DingTalk(2.1.5) OS(Windows/10) Browser(Chrome/133.0.0.0) DingWeb/2.1.5 IMPaaS DingWeb/2.1.5",
                "dt": "j",
                "wv": "im:3,au:3,sy:6",
                "sync": "0,0;0;0;",
                "did": self.device_id,
                "mid": generate_mid()
            }
        }
        await ws.send(json.dumps(msg))
        # 等待一段时间，确保连接注册完成
        await asyncio.sleep(1)
        msg = {"lwp": "/r/SyncStatus/ackDiff", "headers": {"mid": "5701741704675979 0"}, "body": [
            {"pipeline": "sync", "tooLong2Tag": "PNM,1", "channel": "sync", "topic": "sync", "highPts": 0,
             "pts": int(time.time() * 1000) * 1000, "seq": 0, "timestamp": int(time.time() * 1000)}]}
        await ws.send(json.dumps(msg))
        logger.info('连接注册完成')

    def is_chat_message(self, message):
        """判断是否为用户聊天消息"""
        try:
            return (
                isinstance(message, dict) 
                and "1" in message 
                and isinstance(message["1"], dict)  # 确保是字典类型
                and "10" in message["1"]
                and isinstance(message["1"]["10"], dict)  # 确保是字典类型
                and "reminderContent" in message["1"]["10"]
            )
        except Exception:
            return False

    def is_sync_package(self, message_data):
        """判断是否为同步包消息"""
        try:
            return (
                isinstance(message_data, dict)
                and "body" in message_data
                and "syncPushPackage" in message_data["body"]
                and "data" in message_data["body"]["syncPushPackage"]
                and len(message_data["body"]["syncPushPackage"]["data"]) > 0
            )
        except Exception:
            return False

    def is_typing_status(self, message):
        """判断是否为用户正在输入状态消息"""
        try:
            return (
                isinstance(message, dict)
                and "1" in message
                and isinstance(message["1"], list)
                and len(message["1"]) > 0
                and isinstance(message["1"][0], dict)
                and "1" in message["1"][0]
                and isinstance(message["1"][0]["1"], str)
                and "@goofish" in message["1"][0]["1"]
            )
        except Exception:
            return False

    async def handle_message(self, message_data, websocket):
        """处理所有类型的消息"""
        try:

            try:
                message = message_data
                ack = {
                    "code": 200,
                    "headers": {
                        "mid": message["headers"]["mid"] if "mid" in message["headers"] else generate_mid(),
                        "sid": message["headers"]["sid"] if "sid" in message["headers"] else '',
                    }
                }
                if 'app-key' in message["headers"]:
                    ack["headers"]["app-key"] = message["headers"]["app-key"]
                if 'ua' in message["headers"]:
                    ack["headers"]["ua"] = message["headers"]["ua"]
                if 'dt' in message["headers"]:
                    ack["headers"]["dt"] = message["headers"]["dt"]
                await websocket.send(json.dumps(ack))
            except Exception as e:
                pass

            # 如果不是同步包消息，直接返回
            if not self.is_sync_package(message_data):
                return

            # 获取并解密数据
            sync_data = message_data["body"]["syncPushPackage"]["data"][0]
            
            # 检查是否有必要的字段
            if "data" not in sync_data:
                logger.debug("同步包中无data字段")
                return

            # 解密数据
            try:
                data = sync_data["data"]
                try:
                    data = base64.b64decode(data).decode("utf-8")
                    data = json.loads(data)
                    # logger.info(f"无需解密 message: {data}")
                    return
                except Exception as e:
                    # logger.info(f'加密数据: {data}')
                    decrypted_data = decrypt(data)
                    message = json.loads(decrypted_data)
            except Exception as e:
                logger.error(f"消息解密失败: {e}")
                return

            try:
                # 判断是否为订单消息,需要自行编写付款后的逻辑
                if message['3']['redReminder'] == '等待买家付款':
                    user_id = message['1'].split('@')[0]
                    user_url = f'https://www.goofish.com/personal?userId={user_id}'
                    logger.info(f'等待买家 {user_url} 付款')
                    return
                elif message['3']['redReminder'] == '交易关闭':
                    user_id = message['1'].split('@')[0]
                    user_url = f'https://www.goofish.com/personal?userId={user_id}'
                    logger.info(f'卖家 {user_url} 交易关闭')
                    return
                elif message['3']['redReminder'] == '等待卖家发货':
                    user_id = message['1'].split('@')[0]
                    user_url = f'https://www.goofish.com/personal?userId={user_id}'
                    logger.info(f'交易成功 {user_url} 等待卖家发货')
                    return

            except:
                pass

            # --- 修改开始：加强消息类型判断和处理 ---
            # 检查是否为空消息或无效消息内容
            if not message or not isinstance(message, dict):
                logger.debug("收到空消息或无效格式消息，忽略")
                return

            # 1. 判断是否为明确的非聊天系统指令/卡片 (根据之前分析的结构)
            # 例如，检查是否存在 '3' 键且其值包含 'redReminder' (订单状态) 或其他系统卡片特征
            # 注意：这里的判断条件需要根据实际收到的系统消息结构进行调整和完善
            if '3' in message and isinstance(message.get('3'), dict) and 'redReminder' in message['3']:
                logger.debug(f"识别到订单状态消息: {message['3']['redReminder']}，忽略")
                return
            # TODO: 根据需要添加更多对其他类型系统卡片消息的判断和 return

            # 2. 判断是否为用户正在输入状态
            if self.is_typing_status(message):
                logger.debug("用户正在输入")
                return

            # 3. 尝试提取聊天消息内容，并判断是否为图片或空文本
            try:
                content_type = message.get("1", {}).get("4", 0) # 尝试获取 contentType
                send_message_text = message.get("1", {}).get("10", {}).get("reminderContent", "")
            except AttributeError:
                logger.warning(f"无法解析消息内容结构，忽略: {message}")
                return

            if content_type == 2: # 假设 2 代表图片消息 (需要根据实际情况确认)
                logger.info("收到图片消息，发送固定引导回复")
                # 提取必要信息发送固定回复
                send_user_id = message.get("1", {}).get("10", {}).get("senderUserId")
                cid_part = message.get("1", {}).get("2", "").split('@')[0]
                if send_user_id and cid_part:
                    await self.send_msg(websocket, cid_part, send_user_id, "图片收到啦~ 不过我看不到图片内容哦😅 能麻烦您用文字简单说下问题吗？或者加我们售后群发图也行哈！")
                else:
                    logger.warning(f"无法从图片消息中提取必要信息发送引导回复: {message}")
                return
            elif not send_message_text or send_message_text.strip() == "":
                logger.debug("收到空文本消息，忽略")
                return

            # 4. 如果以上都不是，才认为是有效的文本聊天消息，继续处理
            logger.debug("识别为有效文本聊天消息，继续处理")
            send_message = send_message_text # 使用已提取的文本
            # --- 修改结束 ---

            # 处理聊天消息 (从这里开始是原有的逻辑, 但 send_message 已被提取)
            create_time = int(message["1"]["5"])
            send_user_name = message["1"]["10"]["reminderTitle"]
            send_user_id = message["1"]["10"]["senderUserId"]
            # send_message = message["1"]["10"]["reminderContent"] # 这行不再需要
            
            # 时效性验证（过滤5分钟前消息）
            if (time.time() * 1000 - create_time) > 300000:
                logger.debug("过期消息丢弃")
                return
                
            if send_user_id == self.myid:
                logger.debug("过滤自身消息")
                return
                
            url_info = message["1"]["10"]["reminderUrl"]
            item_id = url_info.split("itemId=")[1].split("&")[0] if "itemId=" in url_info else None
            
            if not item_id:
                logger.warning("无法从消息中获取商品ID")
                return
                
            # ---- 增加健壮性检查 ----
            item_description = "无法获取商品信息。" # 设置默认值
            try:
                # 调用 API 获取商品信息
                item_response = self.xianyu.get_item_info(self.cookies, item_id)

                # 检查 API 调用是否成功以及数据结构是否符合预期
                if item_response and isinstance(item_response, dict) and 'data' in item_response and isinstance(item_response['data'], dict) and 'itemDO' in item_response['data']:
                    item_info = item_response['data']['itemDO']
                    # 进一步检查 item_info 是否是字典以及包含所需字段
                    if isinstance(item_info, dict) and 'desc' in item_info and 'soldPrice' in item_info:
                         # 确保字段不为空
                         desc = item_info.get('desc', '')
                         price = item_info.get('soldPrice', '未知') 
                         item_description = f"{desc};当前商品售卖价格为:{str(price)}"
                    else:
                         logger.warning(f"获取到的 item_info 结构不完整或字段缺失, item_id: {item_id}, item_info: {item_info}")
                         item_description = "无法获取完整的商品描述信息。" # 使用备用描述
                else:
                    logger.warning(f"获取商品信息失败或返回结构异常, item_id: {item_id}, response: {item_response}")
                    # item_description 保留默认值 "无法获取商品信息。"

            except Exception as e:
                logger.error(f"调用 get_item_info 或处理商品信息时发生异常: {e}, item_id: {item_id}")
                # item_description 保留默认值 "无法获取商品信息。"
            # ---- 检查结束 ----
            
            logger.info(f"user: {send_user_name}, 发送消息: {send_message}")
            
            # 添加用户消息到上下文
            self.context_manager.add_message(send_user_id, item_id, "user", send_message)
            
            # 获取完整的对话上下文
            context = self.context_manager.get_context(send_user_id, item_id)
            
            # 生成回复
            try:
                raw_bot_reply = self.reply_bot.generate_reply(
                    send_message,
                    item_description,
                    context=context
                )
                
                # --- 修改开始：优化兜底回复和后处理 ---
                # 检查回复是否为空
                if not raw_bot_reply or raw_bot_reply.strip() == "":
                    logger.warning(f"检测到空回复，user_msg: {send_message}, intent: {self.reply_bot.last_intent}")
                    bot_reply = "嗯嗯，您的问题我看到了，让我整理下思路哈~"
                else:
                    # 进行回复后处理，例如去除特定标记
                    bot_reply = raw_bot_reply.replace("[右]", "").strip()
                # --- 修改结束 ---
                    
            except Exception as e:
                logger.error(f"生成回复时发生错误: {e}")
                # --- 修改开始：优化异常兜底回复 ---
                bot_reply = "哎呀，脑子有点短路😅 您刚才说的问题能再说一遍吗？或者稍等下再试试~"
                # --- 修改结束 ---
            
            # 检查是否为价格意图，如果是则增加议价次数
            if self.reply_bot.last_intent == "price":
                self.context_manager.increment_bargain_count(send_user_id, item_id)
                bargain_count = self.context_manager.get_bargain_count(send_user_id, item_id)
                logger.info(f"用户 {send_user_name} 对商品 {item_id} 的议价次数: {bargain_count}")
            
            # 添加机器人回复到上下文
            self.context_manager.add_message(send_user_id, item_id, "assistant", bot_reply)
            
            logger.info(f"机器人回复: {bot_reply}")
            cid = message["1"]["2"].split('@')[0]
            await self.send_msg(websocket, cid, send_user_id, bot_reply)
            
        except Exception as e:
            logger.error(f"处理消息时发生错误: {str(e)}")
            if hasattr(message, "__str__"):
                logger.debug(f"原始消息: {message}")

    async def send_heartbeat(self, ws):
        """发送心跳包并等待响应"""
        try:
            heartbeat_mid = generate_mid()
            heartbeat_msg = {
                "lwp": "/!",
                "headers": {
                    "mid": heartbeat_mid
                }
            }
            await ws.send(json.dumps(heartbeat_msg))
            self.last_heartbeat_time = time.time()
            logger.debug("心跳包已发送")
            return heartbeat_mid
        except Exception as e:
            logger.error(f"发送心跳包失败: {e}")
            raise

    async def heartbeat_loop(self, ws):
        """心跳维护循环"""
        while True:
            try:
                current_time = time.time()
                
                # 检查是否需要发送心跳
                if current_time - self.last_heartbeat_time >= self.heartbeat_interval:
                    await self.send_heartbeat(ws)
                
                # 检查上次心跳响应时间，如果超时则认为连接已断开
                if (current_time - self.last_heartbeat_response) > (self.heartbeat_interval + self.heartbeat_timeout):
                    logger.warning("心跳响应超时，可能连接已断开")
                    break
                
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"心跳循环出错: {e}")
                break

    async def handle_heartbeat_response(self, message_data):
        """处理心跳响应"""
        try:
            if (
                isinstance(message_data, dict)
                and "headers" in message_data
                and "mid" in message_data["headers"]
                and "code" in message_data
                and message_data["code"] == 200
            ):
                self.last_heartbeat_response = time.time()
                logger.debug("收到心跳响应")
                return True
        except Exception as e:
            logger.error(f"处理心跳响应出错: {e}")
        return False

    async def main(self):
        retry_count = 0
        max_retries = 10
        retry_delay = 5  # 初始重试延迟5秒
        
        while True:
            try:
                # 重置重试计数器
                if retry_count > 0:
                    logger.info(f"尝试第 {retry_count} 次重连...")
                
                headers = {
                    "Cookie": self.cookies_str,
                    "Host": "wss-goofish.dingtalk.com",
                    "Connection": "Upgrade",
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
                    "Origin": "https://www.goofish.com",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                }

                # 添加连接超时设置
                async with websockets.connect(
                    self.base_url, 
                    extra_headers=headers,
                    ping_interval=20,  # 更频繁的ping以保持连接
                    ping_timeout=10,
                    close_timeout=10
                ) as websocket:
                    # 连接成功，重置重试计数
                    retry_count = 0
                    retry_delay = 5
                    
                    self.ws = websocket
                    await self.init(websocket)
                    
                    # 初始化心跳时间
                    self.last_heartbeat_time = time.time()
                    self.last_heartbeat_response = time.time()
                    
                    # 启动心跳任务
                    self.heartbeat_task = asyncio.create_task(self.heartbeat_loop(websocket))
                    
                    async for message in websocket:
                        try:
                            message_data = json.loads(message)
                            
                            # 处理心跳响应
                            if await self.handle_heartbeat_response(message_data):
                                continue
                            
                            # 发送通用ACK响应
                            if "headers" in message_data and "mid" in message_data["headers"]:
                                ack = {
                                    "code": 200,
                                    "headers": {
                                        "mid": message_data["headers"]["mid"],
                                        "sid": message_data["headers"].get("sid", "")
                                    }
                                }
                                # 复制其他可能的header字段
                                for key in ["app-key", "ua", "dt"]:
                                    if key in message_data["headers"]:
                                        ack["headers"][key] = message_data["headers"][key]
                                await websocket.send(json.dumps(ack))
                            
                            # 处理其他消息
                            await self.handle_message(message_data, websocket)
                                
                        except json.JSONDecodeError:
                            logger.error("消息解析失败")
                        except Exception as e:
                            logger.error(f"处理消息时发生错误: {str(e)}")
                            if hasattr(message, "__str__"):
                                logger.debug(f"原始消息: {message}")

            except websockets.exceptions.ConnectionClosed as e:
                logger.warning(f"WebSocket连接已关闭: {e}")
                retry_count += 1
                
            except Exception as e:
                logger.error(f"连接发生错误: {e}")
                retry_count += 1
            
            finally:
                # 清理心跳任务
                if self.heartbeat_task:
                    self.heartbeat_task.cancel()
                    try:
                        await self.heartbeat_task
                    except asyncio.CancelledError:
                        pass
                
                # 指数退避重试
                wait_time = min(retry_delay * (2 ** (retry_count - 1)), 300)  # 最大等待5分钟
                logger.info(f"等待 {wait_time} 秒后重试连接...")
                await asyncio.sleep(wait_time)
                
                # 超过最大重试次数后，重新加载cookie
                if retry_count >= max_retries:
                    logger.warning("达到最大重试次数，尝试重新加载cookie")
                    load_dotenv(override=True)  # 重新加载环境变量
                    new_cookies = os.getenv("COOKIES_STR")
                    if new_cookies and new_cookies != self.cookies_str:
                        self.cookies_str = new_cookies
                        self.cookies = trans_cookies(new_cookies)
                        logger.info("成功重新加载cookie")
                    retry_count = 0  # 重置重试计数


if __name__ == '__main__':
    #加载环境变量 cookie
    load_dotenv()
    cookies_str = os.getenv("COOKIES_STR")
    xianyuLive = XianyuLive(cookies_str)
    # 常驻进程
    asyncio.run(xianyuLive.main())
